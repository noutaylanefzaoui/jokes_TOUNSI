from ..extensions import db

class Favorite(db.Model):
    """Favorite model for user saved jokes."""
    
    __tablename__ = "favorites"
    
    favorite_id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    joke_id = db.Column(db.Integer, db.ForeignKey("jokes.id"), nullable=False)
    
    # Ensure a user can only favorite a joke once
    __table_args__ = (db.UniqueConstraint('user_id', 'joke_id', name='_user_joke_uc'),)
    
    def add(self):
        """Add to favorites."""
        db.session.add(self)
        db.session.commit()
        
    def remove(self):
        """Remove from favorites."""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<Favorite User {self.user_id} - Joke {self.joke_id}>"
