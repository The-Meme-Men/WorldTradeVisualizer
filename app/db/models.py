from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, Float, UniqueConstraint, LargeBinary, \
    Table, DateTime, Date, Text, Enum, null, JSON
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relation, relationship
import datetime
import enum

Base = declarative_base()