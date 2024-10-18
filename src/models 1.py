import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er



Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    full_name = Column(String(100))
    profile_picture = Column(String(200))
    bio = Column(String(300))
    is_verified = Column(Boolean, default=False)
    
    posts = relationship("Post", back_populates="usuario")
    followers = relationship("Seguidor", foreign_keys='Seguidor.usuario_id')
    following = relationship("Seguidor", foreign_keys='Seguidor.seguido_id')

class Post(Base):
    __tablename__ = 'post'
    
    id = Column(Integer, primary_key=True)
    caption = Column(String(500))
    image_url = Column(String(300), nullable=False)
    created_at = Column(DateTime)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    
    usuario = relationship("Usuario", back_populates="posts")
    comments = relationship("Comentario", back_populates="post")
    likes = relationship("Like", back_populates="post")

class Comentario(Base):
    __tablename__ = 'comentario'
    
    id = Column(Integer, primary_key=True)
    content = Column(String(300), nullable=False)
    created_at = Column(DateTime)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    
    post = relationship("Post", back_populates="comments")
    usuario = relationship("Usuario")

class Like(Base):
    __tablename__ = 'like'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    
    post = relationship("Post", back_populates="likes")
    usuario = relationship("Usuario")

class Seguidor(Base):
    __tablename__ = 'seguidor'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    seguido_id = Column(Integer, ForeignKey('usuario.id'))
    
    usuario = relationship("Usuario", foreign_keys=[usuario_id])
    seguido = relationship("Usuario", foreign_keys=[seguido_id])


class Address(Base):
    __tablename__ = 'address'
    
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship(Person)

    def to_dict(self):
        return {}


try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e


