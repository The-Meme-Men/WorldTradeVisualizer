from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime
from sqlalchemy.orm import relation, relationship
import datetime
import enum

Base = declarative_base()


class PrimaryKeyBase:
    id = Column(Integer, primary_key=True, autoincrement=True)


class Country(Base):
    __tablename__ = 'country'
    # Country IDs from comtrade
    country_id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(length=64), unique=True, nullable=False, index=True)
    iso = Column(String(length=16), unique=True, nullable=True, index=True)


class Commodity(Base):
    __tablename__ = 'commodity'
    description = Column(String(length=256), unique=True, index=True)
    comtrade_code = Column(String(length=32), unique=True, primary_key=True)


class RGCode(Base):
    __tablename__ = 'rg_code'
    code = Column(Integer, unique=True, nullable=False, primary_key=True)
    description = Column(String(64), unique=True, nullable=False)
    # Flow code supplied by excel sheet
    flow_code = Column(String(length=4), unique=True)


class QuantityCode(Base):
    __tablename__ = 'quantity_code'
    code = Column(Integer, unique=True, nullable=False, primary_key=True)
    description = Column(String(64), unique=True, nullable=False)


class MOTCode(Base):
    __tablename__ = 'mot_code'
    code = Column(Integer, unique=True, nullable=False, primary_key=True)
    description = Column(String(64), unique=True, nullable=False)


class MOSCode(Base):
    __tablename__ = 'mos_code'
    code = Column(Integer, unique=True, nullable=False, primary_key=True)
    description = Column(String(64), unique=True, nullable=False)


class CSTCode(Base):
    __tablename__ = 'cst_code'
    code = Column(Integer, unique=True, nullable=False, primary_key=True)
    description = Column(String(64), unique=True, nullable=False)


class FlowCode(Base):
    __tablename__ = 'flow_coded'
    code = Column(Integer, unique=True, nullable=False, primary_key=True)
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
    reporter = relationship(Country, foreign_keys=[reporter_id])

    partner_id = Column(Integer, ForeignKey('country.id'), index=True)
    partner = relationship(Country, foreign_keys=[partner_id])

    partner_2_id = Column(Integer, ForeignKey('country.id'), nullable=True, index=True)
    partner_2 = relationship(Country, foreign_keys=[partner_2_id])

    commodity_id = Column(Integer, ForeignKey('commodity.id'), index=True)
    commodity = relationship(Commodity)

    # Information about the quantity
    quantity_desc_id = Column(Integer, ForeignKey('quantity_code.id'), nullable=True)
    quantity_desc = relationship(QuantityCode, foreign_keys=[quantity_desc_id])

    # Apparently there's also an alt of this???
    alt_quantity_desc_id = Column(Integer, ForeignKey('quantity_code.id'), nullable=True)
    alt_quantity_desc = relationship(QuantityCode, foreign_keys=[alt_quantity_desc_id])

    mot_code_id = Column(Integer, ForeignKey('mot_code.id'), nullable=True)
    mot_code = relationship(MOTCode)

    mos_code_id = Column(Integer, ForeignKey('mos_code.id'), nullable=True)
    mos_code = relationship(MOTCode)

    cst_code_id = Column(Integer, ForeignKey('cst_code.id'), nullable=True)
    cst_code = relationship(MOTCode)

    flow_code_id = Column(Integer, ForeignKey('flow_code.id'), nullable=True)
    flow_code = relationship(MOTCode)

    quantity = Column(Integer, nullable=True)
    alt_quantity = Column(Integer, nullable=True)

    net_weight = Column(Integer, nullable=True)
    gross_weight = Column(Integer, nullable=True)

    # Value in dollars
    trade_value = Column(Integer)

    cif_value = Column(Integer, nullable=True)
    fob_value = Column(Integer, nullable=True)

    est_code = Column(Integer, nullable=True)

    inserted = Column(DateTime, default=datetime.datetime.now())

