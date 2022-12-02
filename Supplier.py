class Supplier:
    def __init__(self, supplier_id, name):
        self.supplier_id = supplier_id
        self.name = name


class Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
        INSERT OR REPLACE INTO suppliers (id, name) VALUES (?, ?) """, [supplier.supplier_id, supplier.name])

    def insert_mng(self, line):
        s = Supplier(line[0], line[1])
        self.insert(s)

    def get_supplier_by_id(self, supplier_id):
        cur = self._conn.cursor()
        a = cur.execute('SELECT name FROM suppliers WHERE id=?', [supplier_id])
        return a.fetchone()


def name():
    return name()