from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from sqlalchemy.orm import validates

db = SQLAlchemy()

pitches_users = db.Table('pitches_users',
    db.Column('pitch_id', db.Integer, db.ForeignKey('pitches.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('date', db.DateTime, nullable=False, default=datetime.utcnow)
)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    bookings = db.relationship('Booking', back_populates='user', lazy=True)
    ratings = db.relationship('Rating', back_populates='user', lazy=True)
    pitches = db.relationship('Pitch', secondary=pitches_users, lazy='subquery',
                              back_populates='users')

    @validates('email')
    def validate_email(self, key, email):
        if "@" not in email:
            raise ValueError("Invalid email")
        return email

class Pitch(db.Model, SerializerMixin):
    __tablename__ = 'pitches'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    
    bookings = db.relationship('Booking', back_populates='pitch', lazy=True)
    ratings = db.relationship('Rating', back_populates='pitch', lazy=True)
    users = db.relationship('User', secondary=pitches_users, lazy='subquery',
                            back_populates='pitches')

class Booking(db.Model, SerializerMixin):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship('User', back_populates='bookings')
    pitch = db.relationship('Pitch', back_populates='bookings')

class Rating(db.Model, SerializerMixin):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)

    user = db.relationship('User', back_populates='ratings')
    pitch = db.relationship('Pitch', back_populates='ratings')
