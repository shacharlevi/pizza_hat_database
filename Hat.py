class Hat:
    def __init__(self, hat_id, topping, supplier, quantity):
        self.hat_id = hat_id
        self.topping = topping
        self.supplier = supplier
        self.quantity = quantity


class Hats:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, hat):
        self.conn.execute("""
        INSERT OR REPLACE INTO hats (id, topping, supplier, quantity) VALUES (?, ?, ?, ?)
        """, [hat.hat_id, hat.topping, hat.supplier, hat.quantity])

    def insert_mng(self, line):
        h = Hat(int(line[0]), line[1], int(line[2]), int(line[3]))
        self.insert(h)

    def hat_by_topping(self, topping):
        cur = self.conn.cursor()
        return cur.execute("""
        SELECT hats.id, hats.supplier, hats.quantity, suppliers.name 
        FROM hats 
        JOIN suppliers ON suppliers.id = hats.supplier
        WHERE topping=?
        """, [topping]).fetchall()

    def update_quantity(self, hat_id):
        my_hat = Hats.find(self, hat_id)
        if my_hat.quantity != 1:
            self.conn.execute("""
            UPDATE hats 
            SET quantity=quantity-1 
            WHERE id=?
            """, [hat_id])
        else:
            self.conn.execute("""
                    DELETE FROM hats 
                    WHERE id=?
                    """, [hat_id])

    def find(self, hat_id):
        curr = self.conn.cursor()
        curr.execute("""
            SELECT * FROM hats WHERE id=?
            """, [hat_id])
        return Hat(*curr.fetchone())
