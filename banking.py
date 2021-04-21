import random as rand
import sqlite3

conn = sqlite3.connect('card.s3db')


class Card:

    def __init__(self):
        self.cur = conn.cursor()
        self.balance = 0
        self.cur.execute('''CREATE TABLE IF NOT EXISTS card(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number TEXT UNIQUE,
        pin TEXT,
        balance INTEGER DEFAULT 0
        );''')
        conn.commit()

    def menu(self):
        print("""
        1. Create an account
        2. Log into account
        0. Exit
        """)
        act = int(input())
        self.action(act)

    def action(self, act):
        if act == 1:
            self.acc_creation()
        if act == 2:
            self.login()
        if act == 0:
            print("Bye!")
            exit()

    def acc_creation(self):
        self.card_checker()
        self.pins = ''.join(["{}".format(rand.randint(0, 9)) for i in range(0, 4)])
        self.accounts = dict()
        accupd = {self.acc_number: self.pins}
        self.accounts.update(accupd)
        print("Your card has been created")
        print("Your card number:", f"\n{self.acc_number}")
        print("Your card PIN:", f'\n{self.pins}')
        data_insert = (self.acc_number, self.pins, self.balance)
        self.cur.execute('''INSERT INTO card (number, pin, balance)
                                        VALUES (?, ?, ?);''', data_insert)
        conn.commit()
        self.menu()

    def card_checker(self):

        rand.seed()
        self.temp_acc_number = "400000" + ''.join("{}".format(rand.randint(0, 9)) for i in range(0, 10))
        self.cc_acc_num = [int(x) for x in self.temp_acc_number]
        self.checksum()
        if not self.checksum():
            self.card_checker()

    def checksum(self):

        cs = int(self.temp_acc_number[15:])
        # print(cs)
        for i in range(0, len(self.temp_acc_number) - 1, 2):
            self.cc_acc_num[i] = int(self.temp_acc_number[i]) * 2
        for j in range(len(self.cc_acc_num) - 1):
            if self.cc_acc_num[j] > 9:
                self.cc_acc_num[j] = self.cc_acc_num[j] - 9
        acc_cc = self.cc_acc_num[:15]
        acc_cc2 = sum(acc_cc) + cs
        if acc_cc2 % 10 == 0:
            self.acc_number = self.temp_acc_number
            return True
        else:
            return False

    def login_menu(self):
        print("""
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")
        operation = int(input())
        while operation != 0:
            if operation == 1:
                print("Balance:")
                self.cur.execute('''SELECT balance FROM card WHERE number = ? and pin = ?''', self.verified)
                conn.commit()
                rows = self.cur.fetchone()
                return rows

            if operation == 2:
                print("Enter income:")
                income_add = input()
                test = (income_add, self.card_no)
                self.cur.execute('''UPDATE card SET balance = (balance + ?) WHERE number = (?);''', test)
                conn.commit()
                print("Income was added!")
                self.login_menu()

            if operation == 3:
                print("Transfer")
                transfer_card_no = input("Enter card number:")

                self.temp_acc_number = transfer_card_no
                self.cc_acc_num = [int(x) for x in transfer_card_no]
                if transfer_card_no == self.card_no:
                    print("You can't transfer money to the same account!")
                    self.login_menu()

                if self.checksum():
                    if transfer_card_no not in self.accounts:
                        print("Such a card does not exist.")
                        self.login_menu()
                else:
                    print("Probably you made a mistake in the card number. Please try again!")
                    self.login_menu()

                transfer_amount = int(input("Enter how much money you want to transfer:"))
                self.cur.execute('''SELECT balance FROM card WHERE number = ? AND pin= ?''', self.verified)
                conn.commit()
                rows = self.cur.fetchone()
                print(rows[0])
                if transfer_amount >= rows[0]:
                    print("Not enough money!")
                    self.login_menu()
                else:
                    transfer = (transfer_amount, transfer_card_no)
                    transfer_deduct = (transfer_amount, self.card_no)
                    self.cur.execute('''UPDATE card SET balance = (balance + ?) WHERE number = (?);''', transfer)
                    self.cur.execute('''UPDATE card SET balance = (balance - ?) WHERE number = (?);''', transfer_deduct)
                    conn.commit()
                    print("Success!")
                    self.login_menu()

            if operation == 4:
                self.cur.execute('''DELETE FROM card WHERE number = ? and pin = ?''', self.verified)
                conn.commit()
                print("The account has been closed!")
                self.login_menu()

            if operation == 5:
                self.menu()
            print("Bye!")
            quit()

    def login(self):
        self.card_no = int(input("Enter your card no:"))
        self.pin_check = input("Enter your PIN:")
        self.verified = (self.card_no, self.pin_check)
        self.cur.execute('''SELECT number, pin FROM card WHERE number = ? and pin = ?''', self.verified)
        rows = self.cur.fetchall()
        conn.commit()
        if rows:
            print("You have successfully logged in!")
            self.login_menu()
        else:
            print("Wrong card number")
            self.menu()


card = Card()
card.menu()
