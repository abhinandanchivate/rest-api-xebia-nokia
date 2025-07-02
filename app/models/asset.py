from app.extensions import db

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(100))
    value = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    purchase_date = db.Column(db.Date)

    user = db.relationship("User", backref="assets")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
