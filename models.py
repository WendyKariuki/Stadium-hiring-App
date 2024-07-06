from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime

db = SQLAlchemy()

# Association table for the many-to-many relationship between Pitches and Users through Bookings
pitches_users = db.Table('pitches_users',
    db.Column('pitch_id', db.Integer, db.ForeignKey('pitch.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('date', db.DateTime, nullable=False, default=datetime.utcnow)
)

class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    bookings = db.relationship('Booking', backref='user', lazy=True)
    ratings = db.relationship('Rating', backref='user', lazy=True)
    pitches = db.relationship('Pitch', secondary=pitches_users, lazy='subquery',
                              backref=db.backref('users', lazy=True))

    @validates('email')
    def validate_email(self, key, email):
        if "@" not in email:
            raise ValueError("Invalid email")
        return email

class Pitch(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)

    bookings = db.relationship('Booking', backref='pitch', lazy=True)
    ratings = db.relationship('Rating', backref='pitch', lazy=True)

class Booking(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitch.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Rating(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitch.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
