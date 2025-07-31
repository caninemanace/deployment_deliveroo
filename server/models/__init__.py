from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .parcel import Parcel
from .location import Location
from .courier import Courier 
from .saved_address import SavedAddress