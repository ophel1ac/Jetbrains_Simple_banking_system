import random
import sqlite3


class BankingSystem:
    # All users
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS card 
                    (id INTEGER,
                     number TEXT,
                     pin TEXT,
                     balance INTEGER DEFAULT 0);
                     """)
    conn.commit()
    IIN = 4 * 10 ** 15
    logged_card = None

    def __init__(self):
        self.card_number = BankingSystem.luhn()
        self.pin = BankingSystem.create_pin()
        # Add current user to db
        BankingSystem.cur.execute(f"""INSERT INTO card (number, pin)
                    VALUES ({self.card_number}, {self.pin})""")
        BankingSystem.conn.commit()

    @staticmethod
    def create_account(self):
        print(f"Your card has been created\nYour card number:\n{str(self.card_number)}\n\
                         Your card PIN:\n{self.pin}")

    def auth(self):
        card = input("Enter your card number:")
        pin = input("Enter your PIN:")
        BankingSystem.cur.execute(f"SELECT number FROM card WHERE number LIKE {card}")
        auth_card = BankingSystem.cur.fetchone()
        BankingSystem.cur.execute(f"SELECT pin FROM card WHERE number LIKE {card}")
        auth_pin = BankingSystem.cur.fetchone()
        if auth_card is not None:
            if card == auth_card[0] and pin == auth_pin[0]:
                print("You have successfully logged in!")
                BankingSystem.logged_card = card
                self.account_menu()
            else:
                print("Wrong card number or PIN!")
        else:
            print("Wrong card number or PIN!")

    @staticmethod
    def balance():
        BankingSystem.cur.execute(f"SELECT balance FROM card WHERE number='{BankingSystem.logged_card}'")
        return BankingSystem.cur.fetchone()[0]

    def account_menu(self):
        while True:
            div1 = input("1. Balance \n\
                        2. Add income \n\
                        3. Do transfer \n\
                        4. Close account \n\
                        5. Log out \n\
                        0. Exit")
            if div1 == "1":
                print(f"Balance: {self.balance()}")
            elif div1 == "2":
                self.add_income()
            elif div1 == "3":
                self.do_transfer()
            elif div1 == "4":
                self.close_account()
            elif div1 == "5":
                self.logout()
                exit()
            else:
                exit()
                self.logout()

    @staticmethod
    def create_pin():
        return '{:04d}'.format(random.randrange(1000, 9999))

    @staticmethod
    def create_card_number():
        card = BankingSystem.IIN + random.randint(10 ** 9, 9 * 10 ** 9)
        return str(card)

    def luhn(number=None, action="gen"):
        if number is None:
            number = BankingSystem.create_card_number()
        card = [int(_) for _ in number[::-1]]
        check_digit = int(card[0])
        for i in range(1, len(card), 2):
            card[i] *= 2
            if card[i] > 9:
                card[i] = card[i] - 9
        checksum = sum(card[1::]) * 9 % 10
        if action == "check":
            return checksum == check_digit
        else:
            number = number[:15] + str(checksum)
            return number

    @staticmethod
    def add_income():
        income = int(input("Enter income:"))
        BankingSystem.cur.execute(f"UPDATE card SET balance=balance + {income} \
                                    WHERE number = {BankingSystem.logged_card}")
        BankingSystem.conn.commit()
        print("Income was added!")

    def do_transfer(self):
        where_to_transfer = input("Transfer \nEnter card number:\n")
        BankingSystem.cur.execute(f"SELECT number FROM card WHERE number={where_to_transfer}")
        to_card = BankingSystem.cur.fetchone()
        if where_to_transfer == BankingSystem.logged_card:
            print("You can't transfer money to the same account!")
        elif BankingSystem.luhn(where_to_transfer, "check") is False:
            print("Probably you made mistake in the card number. Please try again!\n")
        elif to_card is None:
            print("Such a card does not exist.")
        else:
            transfer_amount = int(input('Enter how much money you want to transfer:\n'))
            if transfer_amount > self.balance():
                print('Not enough money!')
            else:
                self.make_transaction(where_to_transfer, transfer_amount)

    @staticmethod
    def card_exists(number):
        BankingSystem.cur.execute(f"SELECT number FROM card WHERE number={str(number)}")
        if BankingSystem.cur.fetchone() is not None:
            return True

    @staticmethod
    def make_transaction(number_to, amount):
        BankingSystem.cur.execute(f"UPDATE card SET balance = balance - {amount} \
                                    WHERE number = {BankingSystem.logged_card}")
        BankingSystem.cur.execute(f"UPDATE card SET balance = balance + {amount} WHERE number = {number_to}")
        BankingSystem.conn.commit()
        print("Success!\n")

    def close_account(self):
        BankingSystem.cur.execute(f"DELETE FROM card WHERE number = {self.card_number}")
        BankingSystem.conn.commit()
        print("The account has been closed!")

    @staticmethod
    def logout():
        BankingSystem.logged_card = None
        print("You have successfully logged out!")


while True:
    div = input("1. Create an account \n \
                2. Log into account \n \
                0. Exit")
    if div == "1":
        user1 = BankingSystem()
        BankingSystem.create_account(user1)
    elif div == "2":
        user1.auth()
    else:
        print("Bye!")
        BankingSystem.conn.close()
        exit()
