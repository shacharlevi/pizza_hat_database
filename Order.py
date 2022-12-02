class Order:
    def __init__(self, id, location, hat):
        self.id = id
        self.location = location
        self.hat = hat


class Orders:
    def __init__(self, conn):
        self._conn = conn
        self.order_id = 1

    def insert(self, order):
        self._conn.execute("""
        INSERT OR REPLACE INTO orders (id, location, hat) VALUES (?, ?, ?) """, [order.id, order.location, order.hat])

    def insert_mng(self, line):
        ord1 = Order(self.order_id, line[0], int(line[1]))
        self.order_id += 1
        self.insert(ord1)
