from app.extensions import db

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))
    level = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    users = db.relationship("User_tbl", back_populates="role")
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "level": self.level,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
