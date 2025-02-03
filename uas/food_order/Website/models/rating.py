class Rating:
    def __init__(self, user_id, menu_id, rating, feedback):
        self.user_id = user_id
        self.menu_id = menu_id
        self.rating = rating
        self.feedback = feedback

    def save(self, db):
        conn = db.connect()
        cursor =conn.cursor()  
        cursor.execute("INSERT INTO ratings (user_id, menu_id, rating, feedback) VALUES (%s, %s, %s, %s)",  
                       (self.user_id, self.menu_id, self.rating, self.feedback))
        conn.commit()
        cursor.close()  
        conn.close()