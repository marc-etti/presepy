from app import db
from flask_login import UserMixin
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    def __init__(self, 
                 username, 
                 password, 
                 is_admin=False,
                 is_active=True) -> None:
        self.username = username
        self.password = generate_password_hash(password)
        self.is_admin = is_admin
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

            

