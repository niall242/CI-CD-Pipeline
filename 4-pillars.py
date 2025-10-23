from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCardPayment(Payment):
    def pay(self, amount):
        print(f"Paid £{amount} using Credit Card.")

class PayPalPayment(Payment):
    def pay(self, amount):
        print(f"Paid £{amount} via PayPal.")

payment = CreditCardPayment()
payment.pay(100)  # Output: "Paid £100 using Credit Card"





class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance  # private attribute

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount

    def get_balance(self):
        return self.__balance

account = BankAccount("Alice", 100)
account.deposit(50)
print(account.get_balance())  # Output: 150




class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def move(self):
        print("Vehicle is moving")

class Car(Vehicle):
    def move(self):
        print(f"{self.brand} car is driving on the road")

class Boat(Vehicle):
    def move(self):
        print(f"{self.brand} boat is sailing on water")

# Demonstration
for v in [Car("Toyota"), Boat("Yamaha")]:
    v.move()  # Output: "Toyota car is driving on the road. 
              # Yamaha boat is sailing on water"




class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

def make_sound(animal):
    print(animal.speak())

# Both objects share the same interface
make_sound(Dog())  # Output: "Woof!"
make_sound(Cat())  # Output: "Meow!"
