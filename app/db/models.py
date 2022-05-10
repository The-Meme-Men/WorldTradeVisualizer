from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, Float, UniqueConstraint, LargeBinary, \
    Table, DateTime, Date, Text, Enum, null, JSON
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relation, relationship
import datetime
import enum

Base = declarative_base()


class PrimaryKeyBase:
    id = Column(Integer, primary_key=True, autoincrement=True)


class Country(Base, PrimaryKeyBase):
    __tablename__ = 'country'
    # Country IDs from comtrade
    country_id = Column(Integer, unique=True, index=True)
    name = Column(String(length=64), unique=True, nullable=False, index=True)
    iso = Column(String(length=16), unique=True, nullable=False, index=True)


class Commodity(Base, PrimaryKeyBase):
    __tablename__ = 'commodity'
    description = Column(String(length=256), unique=True, index=True)
    # This has to be added separately and handled as a string because of the stupid comtrade API
    comtrade_code = Column(String(length=32), unique=True, index=True)


class RGCode(Base, PrimaryKeyBase):
    __tablename__ = 'rg_code'
    # Uses primary incrementing primary key since the ones supplied by comtrade are kinda fucky
    # This code is supplied straight from the trade stats
    code = Column(Integer, unique=True, nullable=False, index=True)
    description = Column(String(64), unique=True, nullable=False)
    # Flow code supplied by excel sheet
    flow_code = Column(String(length=4), unique=True)


class QuantityCode(Base, PrimaryKeyBase):
    __tablename__ = 'quantity_code'
    # Uses primary incrementing primary key since the ones supplied by comtrade are kinda fucky
    # This code is supplied straight from the trade stats
    code = Column(Integer, unique=True, nullable=False, index=True)
    description = Column(String(64), unique=True, nullable=False)


class TradeStat(Base, PrimaryKeyBase):
    __tablename__ = 'trade_stat'

    pf_code = Column(String(length=32))
    year = Column(Integer, index=True, nullable=False)
    period = Column(Integer)
    period_desc = Column(String)
    aggregation_level = Column(Integer)
    is_leaf = Column(Boolean)

    # Is it import/export
    rg_id = Column(Integer, ForeignKey('rg_code.id'), index=True)
    rg = relationship(RGCode)

    reporter_id = Column(Integer, ForeignKey('country.id'), index=True)
    reporter = relationship(Country)

    partner_id = Column(Integer, ForeignKey('country.id'), index=True)
    partner = relationship(Country)

    partner_2_id = Column(Integer, ForeignKey('country.id'), nullable=True, index=True)
    partner_2 = relationship(Country)

    # TODO: Change customs to a separate table
    customs_code = Column(String(), nullable=True)
    customs_desc = Column(String(), nullable=True)

    # TODO: Figure out wtf mot is
    # TODO: Change mot to a separate table
    mot_code = Column(String(), nullable=True)
    mot_desc = Column(String(), nullable=True)

    commodity_id = Column(Integer, ForeignKey('commodity.id'), index=True)
    commodity = relationship(Commodity)

    # Information about the quantity
    quantity_desc_id = Column(Integer, ForeignKey('quantity_code.id'), nullable=True)
    quantity_desc = relationship(QuantityCode)

    # Apparently there's also an alt of this???
    alt_quantity_desc_id = Column(Integer, ForeignKey('quantity_code.id'), nullable=True)
    alt_quantity_desc = relationship(QuantityCode)

    quantity = Column(Integer, nullable=True)
    alt_quantity = Column(Integer, nullable=True)

    net_weight = Column(Integer, nullable=True)
    gross_weight = Column(Integer, nullable=True)

    # Value in dollars
    trade_value = Column(Integer)

    cif_value = Column(Integer, nullable=True)
    fob_value = Column(Integer, nullable=True)

    est_code = Column(Integer, nullable=True)

