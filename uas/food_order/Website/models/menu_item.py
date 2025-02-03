class MenuItem:
    def __init__(self, item_id, name, price, description, image, stock):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.description = description
        self.image = image
        self.stock = stock

    def save(self, db):
        # Save the menu to the database
        conn = db.connect()
        cursor =conn.cursor()

        # Insert the new user into the database  
        cursor.execute("INSERT INTO menu_items(name, price, description, image, stock) VALUES (%s, %s, %s, %s, %s)",  
                       (self.name, self.price, self.description, self.image, self.stock))
        conn.commit()  
  
        # Close the connection  
        cursor.close()  
        conn.close()  

    def update(self, db, id):
        # Save the menu to the database
        conn = db.connect()
        cursor =conn.cursor()

        # Insert the new user into the database  
        cursor.execute("UPDATE menu_items SET name=%s,price=%s,description=%s,image=%s,stock=%s WHERE id=%s",  
                       (self.name, self.price, self.description, self.image, self.stock, id))
        conn.commit()  
  
        # Close the connection  
        cursor.close()  
        conn.close()  

    def check_stock(self, qty):
        if self.stock < qty:
            return False
        return True

    def update_stock(self, db, id, stock):
        self.stock = stock

        # Save the updated stock to the database
        conn = db.connect()
        cursor =conn.cursor()

        # Insert the new user into the database  
        cursor.execute("UPDATE menu_items SET stock=%s WHERE id=%s",  
                       (self.stock, id))
        conn.commit()  
  
        # Close the connection  
        cursor.close()  
        conn.close()  