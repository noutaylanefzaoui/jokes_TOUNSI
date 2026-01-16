from datetime import datetime
from ..extensions import db


class Joke(db.Model):
    """Joke model storing Tunisian jokes with metadata."""
    
    __tablename__ = "jokes"
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Joke text (primary language is Tunisian dialect)
    text_tn = db.Column(db.Text, nullable=False)  # Tunisian text
    text_fr = db.Column(db.Text, nullable=True)   # French translation
    text_en = db.Column(db.Text, nullable=True)   # English translation
    
    # Classification (metadata about the joke)
    age_group = db.Column(db.String(50), nullable=True)  # e.g., "Kids", "Adults"
    era = db.Column(db.String(50), nullable=True)        # e.g., "Pre-2011", "Post-2011"
    region = db.Column(db.String(50), nullable=True)     # e.g., "Tunis", "Sfax"
    acceptability = db.Column(db.String(50), nullable=True)  # e.g., "Safe", "Sensitive"
    delivery_type = db.Column(db.String(50), nullable=True)  # e.g., "Radio", "TV"
    
    # Acoustic/delivery properties
    tone = db.Column(db.String(50), nullable=True)   # e.g., "Sarcastic", "Funny"
    rhythm = db.Column(db.String(50), nullable=True) # e.g., "Fast", "Slow"
    
    # Publishing status
    is_published = db.Column(db.Boolean, default=False, index=True)
    
    # Foreign key to user (who created the joke)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    def __repr__(self):
        return f"<Joke {self.id}>"
    
    def to_dict(self):
        """Convert joke to dictionary for JSON responses."""
        return {
            "id": self.id,
            "text_tn": self.text_tn,
            "text_fr": self.text_fr,
            "text_en": self.text_en,
            "age_group": self.age_group,
            "era": self.era,
            "region": self.region,
            "acceptability": self.acceptability,
            "delivery_type": self.delivery_type,
            "tone": self.tone,
            "rhythm": self.rhythm,
            "is_published": self.is_published,
            "author_id": self.author_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }