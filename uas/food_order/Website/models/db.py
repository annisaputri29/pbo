from werkzeug.security import check_password_hash

class DB:
    def __init__(self, db, app):
        self.db = db
        self.app = app
        self.app.config['MYSQL_DATABASE_USER'] = 'root'
        self.app.config['MYSQL_DATABASE_PASSWORD'] = ''
        self.app.config['MYSQL_DATABASE_DB'] = 'food_order'
        self.app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        self.db.init_app(app)

    def fetch_all(self, table):
        # Fetch all menu items from the database
        conn = self.db.connect()  
        cursor = conn.cursor()    

        cursor.execute(f"SELECT * FROM {table}")  
        result = cursor.fetchall() 

        cursor.close()
        conn.close()

        return result
    
    def fetch_all_filtered(self, table, column, value):
        # Fetch all menu items from the database
        conn = self.db.connect()  
        cursor = conn.cursor()  

        cursor.execute(f"SELECT * FROM {table} WHERE {column} = '{value}'")  
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result

    
    def fetch_one(self, table, id):
        # Fetch all menu items from the database
        conn = self.db.connect()  
        cursor = conn.cursor()    

        cursor.execute(f"SELECT * FROM {table} WHERE id = {id}")   
        result = cursor.fetchone() 

        cursor.close()
        conn.close()

        return result
    
    def delete_one(self, table, id):
        # Delete a menu item from the database
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table} WHERE id = {id}")
        conn.commit()
        cursor.close()
        conn.close()
    
    def login(self, username, password, session):
        # Fetch all menu items from the database
        conn = self.db.connect()  
        cursor = conn.cursor()    

        # Query to find the user by username  
        cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")  
        user = cursor.fetchone() 

        cursor.close()
        conn.close()

        # Check if user exists  
        if user:  
            hashed_password = user[4]  
            # Verify the password  
            if check_password_hash(hashed_password, password):  
                # Set session variable  
                session['login'] = True 
                session['user_id'] = user[0]
                session['full_name'] = user[1]
                session['email'] = user[2]
                session['username'] = user[3]
                session['password'] = user[4]
                session['role'] = user[5] # Optionally store the user in the session  

                return user
            
        return None
    
    def fetch_mean(self, table, column, filter_column, filter_value):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT ROUND(AVG({column}),1) FROM {table} WHERE {filter_column} = '{filter_value}'")  
        result = cursor.fetchone() 
        cursor.close()
        conn.close()

        return result