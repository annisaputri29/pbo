from werkzeug.security import generate_password_hash

class User:
    def __init__(self, full_name, email, username, password, role):
        self.full_name = full_name
        self.email = email
        self.username = username
        self.password = password
        self.role = role

    def hash(self):
        self.hashed_password = generate_password_hash(self.password) 

    def save(self, db):
        # Save the user to the database
        conn = db.connect()
        cursor =conn.cursor()

        # Insert the new user into the database  
        cursor.execute("INSERT INTO users (full_name, email, username, password, role) VALUES (%s, %s, %s, %s, %s)",  
                       (self.full_name, self.email, self.username, self.hashed_password, self.role))
        conn.commit()  
  
        # Close the connection  
        cursor.close()  
        conn.close()  
