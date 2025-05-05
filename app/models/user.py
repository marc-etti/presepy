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

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    def get_id(self):
        return str(self.id)