from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Date, Integer, ForeignKey, String, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import relation, relationship
import datetime
import enum

Base = declarative_base()


class PrimaryKeyBase:
    id = Column(Integer, primary_key=True, autoincrement=True)


class CommClassCode(Base):
    __tablename__ = 'comm_class_code'
    code_class = Column(String(length=16), nullable=False, primary_key=True)
    class_name = Column(String(length=32), nullable=False)


class Country(Base):
    __tablename__ = 'country'
    # Country IDs from comtrade
    country_id = Column(String(length=8), unique=True, primary_key=True)
    name = Column(String(length=64), unique=True, nullable=False, index=True)
    iso = Column(String(length=16), unique=True, nullable=True, index=True)
    reporter = Column(Boolean, default=False)
    partner = Column(Boolean, default=False)


class Commodity(Base, PrimaryKeyBase):
    __tablename__ = 'commodity'
    description = Column(String(length=1024), index=True)
    comtrade_code = Column(String(length=32), index=True)
    comm_class_code_id = Column(String, ForeignKey('comm_class_code.code_class'), nullable=False)
    comm_class_code = relationship(CommClassCode)

    UniqueConstraint(description, comm_class_code_id, comtrade_code)


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
    abbreviation = Column(String(16), index=True)


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
    __tablename__ = 'flow_code'
    code = Column(Integer, unique=True, nullable=False, primary_key=True)
    description = Column(String(64), unique=True, nullable=False)


class TradeStat(Base, PrimaryKeyBase):
    __tablename__ = 'trade_stat'

    year = Column(Integer, index=True, nullable=False)
    period = Column(Integer)
    aggregation_level = Column(Integer)
    is_leaf = Column(Boolean)

    # Is it import/export
    rg_id = Column(Integer, ForeignKey('rg_code.code'), index=True)
    rg = relationship(RGCode)

    reporter_id = Column(String, ForeignKey('country.country_id'), index=True)
    reporter = relationship(Country, foreign_keys=[reporter_id])

    partner_id = Column(String, ForeignKey('country.country_id'), index=True)
    partner = relationship(Country, foreign_keys=[partner_id])

    partner_2_id = Column(String, ForeignKey('country.country_id'), nullable=True, index=True)
    partner_2 = relationship(Country, foreign_keys=[partner_2_id])

    commodity_id = Column(Integer, ForeignKey('commodity.id'), index=True)
    commodity = relationship(Commodity)

    # Information about the quantity
    quantity_desc_id = Column(Integer, ForeignKey('quantity_code.code'), nullable=True)
    quantity_desc = relationship(QuantityCode, foreign_keys=[quantity_desc_id])

    # Apparently there's also an alt of this???
    alt_quantity_desc_id = Column(Integer, ForeignKey('quantity_code.code'), nullable=True)
    alt_quantity_desc = relationship(QuantityCode, foreign_keys=[alt_quantity_desc_id])

    mot_code_id = Column(Integer, ForeignKey('mot_code.code'), nullable=True)
    mot_code = relationship(MOTCode)

    mos_code_id = Column(Integer, ForeignKey('mos_code.code'), nullable=True)
    mos_code = relationship(MOSCode)

    cst_code_id = Column(Integer, ForeignKey('cst_code.code'), nullable=True)
    cst_code = relationship(CSTCode)

    flow_code_id = Column(Integer, ForeignKey('flow_code.code'), nullable=True)
    flow_code = relationship(FlowCode)

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


### TODO: Check data model against this example result:
'''
{'type': 'COMMODITIES', 'freq': 'ANNUAL', 'px': 'HS', 'r': '12', 'rDesc': 'Algeria', 'ps': '1992', 'TotalRecords': 43628, 'isOriginal': 0, 'publicationDate': '2002-09-01T00:00:00', 'isPartnerDetail': 1}

type Ignored (can infer from px)
freq => Stored as A/M
px => FK to comm_class_code
r  => FK to country
rDesc Ignored
ps => Stored as Integer
TotalRecords => Stored as Integer
isOriginal => Stored as Bool
publicationDate => Stored as Date
isPartnerDetail => Stored as Bool

ADDED
inserted => Bool (Marks whether this set of records has been inserted into the DB or not)
'''
class AvailabilityRecord(Base, PrimaryKeyBase):
    __tablename__ = 'availability_record'

    frequency = Column(String(length=1), index=True) #Maybe think of a better way to do this

    com_class_code_id = Column(String(length=16), ForeignKey('comm_class_code.code_class'), index=True)
    com_class_code = relationship(CommClassCode)

    reporter_id = Column(String, ForeignKey('country.country_id'), index=True)
    reporter = relationship(Country, foreign_keys=[reporter_id])

    period = Column(Integer, index=True) 

    total_records = Column(Integer)

    is_original = Column(Boolean)

    publication_date = Column(Date)

    is_partner_detail = Column(Boolean)

    inserted = Column(Boolean, index=True)