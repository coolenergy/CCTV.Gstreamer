from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from dotenv import load_dotenv

import os

# LOAD ENV VALUES
load_dotenv()
ROOT_PATH = os.getenv("ROOT_PATH")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_IP = os.getenv("DB_IP")
DB_NAME = os.getenv("DB_NAME")
DATABASE_URL = "postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, DB_IP, DB_NAME)

# CREATE APP OBJECT
app = Flask(__name__, static_folder=".{}".format(ROOT_PATH))

# SET DATABASE URI IN CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

db = SQLAlchemy(app)

# DEFINE SCHEMA TABLE OF CAMER LIST
class Camera(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  ipaddress = db.Column(db.String(200), nullable=False)
  location = db.Column(db.String(120), nullable=False)
  thumbnail = db.Column(db.String(200))
  online = db.Column(db.String(4))
  timezone = db.Column(db.String(40), nullable=False)
  flag = db.Column(db.String(4))

  thumbnails = db.relationship("Thumbnail", backref=backref("camera", lazy=True))
  videos = db.relationship("Video", backref=backref("camera", lazy=True))
  polygons = db.relationship("Polygon", backref=backref("camera", lazy=True))

  def __init__(self, name, ipaddress, location, thumbnail, online, timezone, flag):
    self.name = name
    self.ipaddress = ipaddress
    self.location = location
    self.thumbnail = thumbnail
    self.online = online
    self.timezone = timezone
    self.flag = flag

# DEFINE SHCEMA TABLE OF VIDEO LIST
class Video(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  path = db.Column(db.String(80), nullable=False)
  time = db.Column(db.DateTime, nullable=False)
  time2str = db.Column(db.String(20), nullable=False)
  duration = db.Column(db.Float, nullable=False)
  camera_id = db.Column(db.Integer, db.ForeignKey('camera.id'))

  def __init__(self, path, time,time2str, duration, camera_id):
    self.path = path
    self.time = time
    self.time2str = time2str
    self.duration = duration
    self.camera_id = camera_id
    
# DEFINE SCHEMA Table OF THUMBNAIL LIST
class Thumbnail(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  path = db.Column(db.String(80), nullable=False)
  time = db.Column(db.DateTime, nullable=False)
  time2str = db.Column(db.String(20), nullable=False)
  camera_id = db.Column(db.Integer, db.ForeignKey('camera.id'))

  def __init__(self, path, time, time2str, camera_id):
    self.path = path
    self.time = time
    self.time2str = time2str
    self.camera_id = camera_id


# DEFINE SCHEMA Table OF Polygon LIST
class Polygon(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(20), nullable=False)
  desc = db.Column(db.String(20), nullable=False)
  position = db.Column(db.String(1000), nullable=False)
  color = db.Column(db.String(500), nullable=False)

  camera_id = db.Column(db.Integer, db.ForeignKey('camera.id'))

  def __init__(self, name, desc, position, color , camera_id):
    self.name = name
    self.desc = desc
    self.position = position
    self.color = color
    self.camera_id = camera_id
    

