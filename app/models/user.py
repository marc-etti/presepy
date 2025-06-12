from app import db
from flask_login import UserMixin
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

#####################################################################
# User Model
# This model represents a user in the system.
# id: Unique identifier for the user.
# username: Unique username for the user.
# password: Hashed password for the user.
# role: Role assigned to the user (e.g., admin, user, expert).
# is_active: Indicates if the user account is active.

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=True)
    role: Mapped[str] = mapped_column(String(80), default='user') 
    is_active: Mapped[bool] = mapped_column(default=True)

    def __init__(self, 
                 username, 
                 password, 
                 role='user',
                 is_active=True) -> None:
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role
        self.is_active = is_active

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    def set_password(self, password) -> None:
        self.password = generate_password_hash(password)
    
    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)
    
    def add(self) -> None:
        db.session.add(self)
        db.session.commit()
        
    def update(self) -> None:
        db.session.commit()
    
    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()