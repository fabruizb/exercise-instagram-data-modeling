import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er



Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    profile_image_url = Column(String(250), nullable=True)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False)
    
    
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")
    stories = relationship("Story", back_populates="user")
    followers = relationship("Follower", foreign_keys='Follower.follower_id', back_populates="follower")
    following = relationship("Follower", foreign_keys='Follower.following_id', back_populates="following")

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    image_url = Column(String(250), nullable=False)
    caption = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False)

   
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    likes = relationship("Like", back_populates="post")

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)

    
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, nullable=False)

    
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

class Story(Base):
    __tablename__ = 'story'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    image_url = Column(String(250), nullable=False)
    caption = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

    
    user = relationship("User", back_populates="stories")

class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('user.id'))
    following_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, nullable=False)

   
    follower = relationship("User", foreign_keys=[follower_id], back_populates="followers")
    following = relationship("User", foreign_keys=[following_id], back_populates="following")



try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e


