import atexit
import sqlite3
import csv
import sys

import Hat
import Supplier
import Order


class Repository:
    def __init__(self):
        self.conn = sqlite3.connect(sys.argv[4])
        self.hatDAO = Hat.Hats(self.conn)
        self.orderDAO = Order.Orders(self.conn)
        self.supplierDAO = Supplier.Suppliers(self.conn)
        self.summary = []

    def create_tables(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS hats (
                id INTEGER PRIMARY KEY, 
                topping TEXT NOT NULL, 
                supplier INTEGER, 
                quantity INTEGER NOT NULL, 
                FOREIGN KEY(id) REFERENCES suppliers(id)
             ); 
            CREATE TABLE IF NOT EXISTS suppliers(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL             
            );
            CREATE TABLE IF NOT EXISTS orders(
                id INTEGER PRIMARY KEY,
                location TEXT NOT NULL,
                hat INTEGER,
                FOREIGN KEY(hat) REFERENCES hats(id)
            );
        """)

    def read_config(self, config):
        with open('config.txt', 'r') as file:
            csv_config = csv.reader(file)
            data = [row for row in csv_config]
            entry = data[0]
            counter = 1
            number = entry[0]
            for x in range(int(number)):
                self.hatDAO.insert_mng(data[counter])
                counter += 1
            number = entry[1]
            for x in range(int(number)):
                self.supplierDAO.insert_mng(data[counter])
                counter += 1

    def write_output(self, answer):
        with open(answer, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=",")
            for i in range(len(self.summary)):
                writer.writerow(self.summary[i])



    def get_order(self, order):
        h = self.hatDAO.hat_by_topping(order[1])
        data = [row for row in h]
        big_list = []
        for row in data:
            list = []
            for index in row:
               list.append(index)
            big_list.append(list)

        min_supplier_id = big_list[0][1]
        min_hat_id = big_list[0][0]
        quantity = big_list[0][2]
        for i in range(len(big_list)):
            a = big_list[i][1]
            if a < min_supplier_id:
                min_hat_id = int(big_list[i][0])
                min_supplier_id = int(a)
                quantity = int(big_list[i][2])
        self.orderDAO.insert_mng([order[0], min_hat_id])
        self.hatDAO.update_quantity(min_hat_id)
        s = self.supplierDAO.get_supplier_by_id(min_supplier_id)
        self.summary.append([order[1], *s, order[0]])

    def read_orders(self, orders):
        with open(orders, 'r') as file:
            csv_orders = csv.reader(file)
            for order in csv_orders:
                self.get_order(order)

    def close(self):
        self.conn.commit()
        self.conn.close()


# the repository singleton
repo = Repository()
atexit.register(repo.close)
