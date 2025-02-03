class Order:
    def __init__(self, order_id, customer_id, menu_id, qty, total, address, status, date):
        self.order_id = order_id
        self.customer_id = customer_id
        self.menu_id = menu_id
        self.qty = qty
        self.total = total
        self.address = address
        self.status = status
        self.date = date

    def save(self, db):
        conn = db.connect()
        cursor =conn.cursor()  
        cursor.execute("INSERT INTO orders (customer_id, menu_id, qty, total, address) VALUES (%s, %s, %s, %s, %s)",  
                       (self.customer_id, self.menu_id, self.qty, self.total, self.address))
        conn.commit()
        cursor.close()  
        conn.close() 

    def update_status(self, db):
        # update status
        self.status = "Done"
        
        conn = db.connect()
        cursor =conn.cursor()  
        # Update the order status in the database  
        cursor.execute("UPDATE orders SET status = %s WHERE id = %s", (self.status, self.order_id))
        conn.commit()
        cursor.close()  
        conn.close() 