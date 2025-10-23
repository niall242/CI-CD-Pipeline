


class InvoicePrinter:
    def print_invoice(self, invoice):
        print(f"Printing invoice for {invoice}")

class InvoiceSaver:
    def save_to_db(self, invoice):
        print(f"Saving {invoice} to database")



class Discount:
    def get_discount(self, price):
        return price

class PercentageDiscount(Discount):
    def get_discount(self, price):
        return price * 0.9

class FixedDiscount(Discount):
    def get_discount(self, price):
        return price - 5

def calculate_price(discount_obj, price):
    return discount_obj.get_discount(price)

print(calculate_price(PercentageDiscount(), 100))  # Output: 90.0




class Bird:
    def fly(self):
        return "Flying high"

class Sparrow(Bird):
    def fly(self):
        return "Sparrow flying low"

def let_it_fly(bird):
    print(bird.fly())

let_it_fly(Sparrow())  # Output: "Sparrow flying low"




class BasicPrinter:
    def print_doc(self):
        print("Printing document...")

class AllInOne:
    def print_doc(self):
        print("Printing document...")
    def scan_doc(self):
        print("Scanning document...")

hp = BasicPrinter()
hp.print_doc()  # Output: "Printing document..."

canon = AllInOne()
canon.print_doc()  # Output: "Printing document..."
canon.scan_doc()  # Output: "Scanning document..."




class Engine:  # abstract class
    def start(self):
        pass

class DieselEngine(Engine):
    def start(self):
        print("Diesel engine starting...")

class ElectricEngine(Engine):
    def start(self):
        print("Electric motor powering up...")

class Car:
    def __init__(self, engine):  # no type hint
        self.engine = engine

    def start(self):
        self.engine.start()

# Use any engine without changing Car
car1 = Car(DieselEngine())
car1.start()  # Output: "Diesel engine starting..."

car2 = Car(ElectricEngine())
car2.start()  # Output: "Electric motor powering up..."



