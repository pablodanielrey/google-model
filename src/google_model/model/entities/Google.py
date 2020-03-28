
"""

import pytz
import uuid
from datetime import datetime, time, timedelta
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, func, or_, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship

from enum import Enum

from . import Base


class GoogleLogTypes(Enum):
    CREATE_USER = 'CREATE_USER'
    UPDATE_USER = 'UPDATE_USER'
    DELETE_USER = 'DELETE_USER'
    CREATE_MAIL = 'CREATE_MAIL'
    UPDATE_MAIL = 'UPDATE_MAIL'
    DELETE_MAIL = 'DELETE_MAIL'

class GoogleLog(Base):

    __tablename__ = 'google_logs'

    type = Column(SQLEnum(GoogleLogTypes))
    authorizer_id = Column(String)
    data = Column(String)

"""