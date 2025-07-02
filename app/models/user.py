from app.extensions import db

import bcrypt
class User_tbl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    role = db.relationship('Role', back_populates='users') 
    def set_password(self, password: str):
        print('inside set_password')
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Method to check if the password matches the stored hash
    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    