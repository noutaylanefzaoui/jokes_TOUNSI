from datetime import datetime
from ..extensions import db


class Joke(db.Model):
    __tablename__ = "jokes"

    id = db.Column(db.Integer, primary_key=True)

    # main Tunisian text (required)
    text_tn = db.Column(db.Text, nullable=False)

    # literal translations (can be null at first)
    text_fr = db.Column(db.Text, nullable=True)
    text_en = db.Column(db.Text, nullable=True)

    # simple classification for now (we will later normalize to separate tables)
    age_group = db.Column(db.String(50), nullable=True)          # e.g. "kids", "adults"
    era = db.Column(db.String(100), nullable=True)               # e.g. "pre-2011"
    region = db.Column(db.String(100), nullable=True)            # e.g. "Sfax"
    acceptability = db.Column(db.String(50), nullable=True)      # "safe", "sensitive", "taboo"
    delivery_type = db.Column(db.String(100), nullable=True)     # "radio", "tv", "standup"

    tone = db.Column(db.String(100), nullable=True)              # e.g. "sarcastic"
    rhythm = db.Column(db.String(100), nullable=True)            # e.g. "fast"

    is_published = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    author = db.relationship("User", back_populates="jokes")
