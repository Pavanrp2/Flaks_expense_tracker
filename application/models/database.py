from application import db

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    amount = db.Column(db.Float, nullable = False)
    category = db.Column(db.String(100), nullable = False)
    date = db.Column(db.Date, nullable = False)
    
    def details(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "amount" : self.amount,
            "category" : self.category,
            "date" : self.date.strftime("%d-%m-%Y")
        }
        