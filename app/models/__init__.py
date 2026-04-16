from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .fortune import FortuneRecord
from .donation import Donation
