from rich import print as rprint



# ============ Domain model ============

from abc import ABC, abstractmethod

# Abstraction – shared interface for all loanable items
class LoanItem(ABC):
    def __init__(self, title, max_days):
        self.title = title
        self.max_days = max_days

    @abstractmethod
    def late_fee_per_day(self):
        pass

# Inheritance – concrete item types extend the abstract base
class Book(LoanItem):
    def late_fee_per_day(self):
        return 0.25

class DVD(LoanItem):
    def late_fee_per_day(self):
        return 0.75


# Encapsulation – balance is private; controlled via methods
class MemberAccount:
    def __init__(self, name):
        self.name = name
        self.__balance = 0.0  # private

    def add_charge(self, amount):
        if amount > 0:
            self.__balance += amount

    def pay(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False

    def balance(self):
        return round(self.__balance, 2)


# ============ Policies & Ports (SOLID) ============

# OCP – strategy for fee calculation; extend with new policies without modifying Library
class LateFeePolicy(ABC):
    @abstractmethod
    def compute_fee(self, item: LoanItem, days_late: int) -> float:
        pass

class StandardPolicy(LateFeePolicy):
    def compute_fee(self, item, days_late):
        if days_late <= 0:
            return 0.0
        return days_late * item.late_fee_per_day()

class ChildrenPolicy(LateFeePolicy):
    # e.g., first 2 late days are free for children’s accounts
    def compute_fee(self, item, days_late):
        days = max(0, days_late - 2)
        return days * item.late_fee_per_day()


# ISP – small focused interfaces instead of one bloated service
class Notifier(ABC):
    @abstractmethod
    def notify(self, member: MemberAccount, message: str):
        pass

class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, member: MemberAccount, amount: float) -> bool:
        pass


# DIP – Library depends on abstractions (Notifier, PaymentGateway, LateFeePolicy)
class EmailNotifier(Notifier):
    def notify(self, member, message):
        rprint(f"[bold cyan][Email][/bold cyan] To {member.name}: {message}")

class ConsolePayment(PaymentGateway):
    def charge(self, member, amount):
        ok = member.pay(amount)
        rprint(f"[bold green][Payment][/bold green] {member.name} paid £{amount:.2f} – {'OK' if ok else 'FAILED'}")
        return ok


# ============ Application core ============

class Library:
    # DIP – inject abstractions
    def __init__(self, notifier: Notifier, payments: PaymentGateway, policy: LateFeePolicy):
        self.notifier = notifier
        self.payments = payments
        self.policy = policy
        self._loans = {}  # member.name -> list of LoanItem

    def checkout(self, member: MemberAccount, item: LoanItem):
        self._loans.setdefault(member.name, []).append(item)
        self.notifier.notify(member, f'Checked out "{item.title}" for up to {item.max_days} days.')

    # Polymorphism – uses item.late_fee_per_day() regardless of concrete type
    def return_item(self, member: MemberAccount, item: LoanItem, days_late: int):
        items = self._loans.get(member.name, [])
        if item in items:
            items.remove(item)
        fee = self.policy.compute_fee(item, days_late)
        if fee > 0:
            member.add_charge(fee)
            self.notifier.notify(member, f'Late fee for "{item.title}": £{fee:.2f}. Current balance £{member.balance():.2f}.')
        else:
            self.notifier.notify(member, f'Returned on time: "{item.title}". No fee.')

    def pay_balance(self, member: MemberAccount, amount: float):
        self.payments.charge(member, amount)
        self.notifier.notify(member, f'Balance now £{member.balance():.2f}.')

    def list_loans(self, member: MemberAccount):
        items = self._loans.get(member.name, [])
        return [i.title for i in items]


# ============ Demo scenario ============

if __name__ == "__main__":
    # Compose the app with chosen implementations (DIP)
    library = Library(
        notifier=EmailNotifier(),
        payments=ConsolePayment(),
        policy=StandardPolicy()  # Swap to ChildrenPolicy() without touching Library – OCP
    )

    alice = MemberAccount("Alice")
    moby = Book("Moby Dick", max_days=14)
    matrix = DVD("The Matrix", max_days=7)

    library.checkout(alice, moby)
    library.checkout(alice, matrix)
    print("Current loans:", library.list_loans(alice))

    # Return items with different lateness – polymorphism in fee via item type
    library.return_item(alice, moby, days_late=3)    # Book – cheaper per day
    library.return_item(alice, matrix, days_late=3)  # DVD – higher per day

    # Pay part of the balance
    library.pay_balance(alice, amount=1.00)
    library.pay_balance(alice, amount=10.00)

    # Swap fee policy at runtime – OCP illustrated without modifying Library
    library.policy = ChildrenPolicy()
    # Another late return under different policy
    library.return_item(alice, DVD("Spirited Away", max_days=7), days_late=2)
    library.return_item(alice, Book("Charlotte's Web", max_days=14), days_late=4)
    library.pay_balance(alice, amount=50.00)
