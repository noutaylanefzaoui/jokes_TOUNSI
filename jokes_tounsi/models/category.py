from ..extensions import db

class Category(db.Model):
    """Category model for grouping jokes."""
    
    __tablename__ = "categories"
    
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=True)
    
    # Relationship to jokes
    jokes = db.relationship("Joke", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"

    def to_dict(self):
        return {
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description
        }
