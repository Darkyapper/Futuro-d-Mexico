import time
import random

class User:
    @staticmethod
    def Main():
        Autovend = Snack_Machine()

class Snack_Machine:
    def __init__(self):
        self.snacksList = []
        self.Autovend_Box = Product_Box()
        self.Autovend_Coin_Box = Coin_Collection_Box()
        
        self.snacksList.append(Product("ABC", "Coca-Cola", 2, 17))
        self.snacksList.append(Product("DEF", "Chocolate Coockie", 10, 14))
        self.snacksList.append(Product("GHI", "Salt Chips", 10, 22))

        print("Welcome to the Snacks Machine")
        time.sleep(1)
        print("---PRODUCT LIST---")
        print("ABC - Coca-Cola - $ 17")
        print("DEF - Chocolate Coockie - $ 14")
        print("GHI - Salt Chips - $ 22")
        print("")

        while True:
            print("Please insert a code:")
            int_code = input()
            time.sleep(2)

            self.Autovend_Box.Analyze_Product_Existence(int_code, self.snacksList)

            if not self.Autovend_Box.Product_Found or not self.Autovend_Box.Still_Exist:
                continue

            time.sleep(1)
            self.Autovend_Coin_Box.Enter_Credits(self.Autovend_Box.Product_Cost)
            time.sleep(2)
            self.Autovend_Box.Drop_Selected_Product()
            time.sleep(3.5)
            self.Autovend_Coin_Box.Check_Exchange()
            time.sleep(2.5)
            print("Have a nice day!")
            time.sleep(2)
            print("")

class Coin_Collection_Box:
    def __init__(self):
        self.User_Credits = 0
        self.To_Pay = 0
        self.Exchange = 0
        self.Exchange_Returned = 0
        self.currency = [1, 2, 5, 10]

    def Enter_Credits(self, cost):
        self.To_Pay = cost
        while self.User_Credits < self.To_Pay:
            print("Please insert coins:")
            e = int(input())
            time.sleep(1)
            if e < 1:
                print("ERROR x0004: That isn't a real currency value! Please try again.")
            else:
                self.User_Credits += e
                print("You have: $", self.User_Credits)
                time.sleep(0.5)
                print("You need: $", self.To_Pay)
                time.sleep(2)
                
    def Check_Exchange(self):
        print("Checking your exchange, wait a moment...")
        self.Exchange = self.User_Credits - self.To_Pay
        if self.Exchange <= 0:
            time.sleep(0.5)
            print("Done!")
        else:
            self.Return_Exchange()

    def Return_Exchange(self):
        print("Dropping your exchange:")
        while self.Exchange_Returned < self.Exchange:
            Random_number = random.choice(self.currency)
            if self.Exchange_Returned + Random_number <= self.Exchange:
                self.Exchange_Returned += Random_number
                print("Exchange Amount: $", self.Exchange)
                print("Current Exchange Returned: $", Random_number)
                print("Exchange Amount Returned: $", self.Exchange_Returned)
                time.sleep(0.8)
        self.Exchange_Returned = 0
        print("Done!")

class Product_Box:
    def Analyze_Product_Existence(self, code, snacksList):
        self.product_found = False
        for product in snacksList:
            if product.P_Code == code:
                iint_code = code
                finded_product = self.Get_Product_Details(iint_code, snacksList)
                if finded_product:
                    self.product_name = finded_product.P_Name
                    self.product_cost = finded_product.P_Cost
                    self.product_amount = finded_product.P_Amount

                    if self.product_amount == 0:
                        print("ERROR x001: The selection that you did is already sold out! Please choose another product.")
                        self.still_exist = False
                    else:
                        print("You have selected", self.product_name)
                        print("$", self.product_cost)
                        finded_product.P_Amount -= 1
                        self.still_exist = True
                self.product_found = True
                break
        if not self.product_found:
            print("ERROR x0002: The selection that you did isn't real! Please enter another code.")

    @staticmethod
    def Get_Product_Details(code, snacksList):
        for product in snacksList:
            if product.P_Code == code:
                return product
        return None
    
    def Drop_Selected_Product(self):
        print("Dropping the select snack, wait a moment...")
        time.sleep(2)
        print("Your product has been delivered correctly")

class Product:
    def __init__(self, code, name, amount, cost):
        self.p_code = code
        self.p_name = name
        self.p_amount = amount
        self.p_cost = cost

# Main
User.Main()
