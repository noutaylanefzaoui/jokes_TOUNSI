from ..extensions import db

class Rating(db.Model):
    """Rating model for jokes."""
    
    __tablename__ = "ratings"
    
    rating_id = db.Column(db.Integer, primary_key=True)
    rating_value = db.Column(db.Integer, nullable=False)
    
    # Foreign Key to Joke
    joke_id = db.Column(db.Integer, db.ForeignKey("jokes.id"), nullable=False)
    
    def submit(self):
        """Submit the rating to the database."""
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Rating {self.rating_value} for Joke {self.joke_id}>"
