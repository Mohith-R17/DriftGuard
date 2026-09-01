import uuid
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """
    User model containing authentication and GitHub OAuth metadata.
    """
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    org = Column(String(100), nullable=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    token = Column(Text, nullable=True)
    api_key = Column(String(100), nullable=True, index=True)
    
    # GitHub OAuth Info
    github_id = Column(String(50), nullable=True)
    github_token = Column(Text, nullable=True)
    github_username = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<User {self.email}>"
