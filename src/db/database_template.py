
from sqlalchemy import Column, Integer, String, Double
from sqlalchemy.orm import declarative_base

Base = declarative_base()

def get_base():
    return Base


class AbsenceTable(Base):
    ""
    __tablename__ = 'absence_table'
    __table_args__ = {'schema': 'raw'}
    ENTERPRISE = Column(String)
    YEAR = Column(String)
    CONTRACT_TYPE = Column(String)
    JOB_TYPE = Column(String)
    GENDER = Column(String)
    ABSENCE_INFO = Column(String)
    ABSENCE_HOURS = Column(Integer)
    UID = Column(Integer, primary_key=True)

class HandicapTable(Base):
    
    __tablename__ = 'handicap_table'
    __table_args__ = {'schema': 'raw'}    
    ENTERPRISE = Column(String, primary_key=True)
    YEAR = Column(String, primary_key=True)
    CONTRACT_TYPE = Column(String, primary_key=True)
    JOB_TYPE = Column(String, primary_key=True)
    GENDER = Column(String, primary_key=True)
    HANDICAP_INFO = Column(String, primary_key=True)

    NBR_EMPLOYEE = Column(Integer)

class PromotionTable(Base):
    
    __tablename__ = 'promotion_table'
    __table_args__ = {'schema': 'raw'}    
    ENTERPRISE = Column(String, primary_key=True)
    YEAR = Column(String, primary_key=True)
    INDICATOR = Column(String, primary_key=True)
    CONTRACT_TYPE = Column(String, primary_key=True)
    JOB_TYPE = Column(String, primary_key=True)
    M3E_CLASS = Column(String, primary_key=True)
    GENDER = Column(String, primary_key=True)
    REMUNERATION = Column(Double)
    NBR_PROMOTION = Column(Double)

class OtherConditionTable(Base):
    
    __tablename__ = 'other_condition_table'
    __table_args__ = {'schema': 'raw'}    
    ENTERPRISE = Column(String)
    YEAR = Column(String)
    CONTRACT_TYPE = Column(String)
    JOB_TYPE = Column(String)
    GENDER = Column(String)
    
    INFO = Column(String)
    TIME_RANGE = Column(String)
    NBR_EMPLOYEE = Column(Integer)
    UID = Column(Integer, primary_key = True)

class ExtWorkerTable(Base):
    
    __tablename__ = 'exterior_worker_table'
    __table_args__ = {'schema': 'raw'}    
    ENTERPRISE = Column(String, primary_key=True)
    YEAR = Column(String, primary_key=True)
    JOB_TYPE = Column(String, primary_key=True)
    GENDER = Column(String, primary_key=True)
    INFO = Column(String, primary_key = True)
    NBR_EMPLOYEE = Column(Integer)

class AgeRangeTable(Base):
    
    __tablename__ = 'age_range_table'
    __table_args__ = {'schema': 'raw'}    
    ENTERPRISE = Column(String)
    YEAR = Column(String)
    CONTRACT_TYPE = Column(String)
    JOB_TYPE = Column(String)
    GENDER = Column(String)
    INFO = Column(String)
    AGE_RANGE = Column(String)
    NBR_EMPLOYEE = Column(Integer)
    UID = Column(Integer, primary_key = True)


class SeniorityTable(Base):
    
    __tablename__ = 'seniority_table'
    __table_args__ = {'schema': 'raw'}    
    ENTERPRISE = Column(String)
    YEAR = Column(String)
    CONTRACT_TYPE = Column(String)
    JOB_TYPE = Column(String)
    GENDER = Column(String)
    INFO = Column(String)
    SENIORITY = Column(String)
    NBR_EMPLOYEE = Column(Integer)
    UID = Column(Integer, primary_key = True)


class NationalityTable(Base):
    
    __tablename__ = 'nationality_table'
    __table_args__ = {'schema': 'raw'}    
    ENTERPRISE = Column(String)
    YEAR = Column(String)
    CONTRACT_TYPE = Column(String)
    JOB_TYPE = Column(String)
    GENDER = Column(String)
    INFO = Column(String)
    NATIONALITY = Column(String)
    NBR_EMPLOYEE = Column(Integer)
    UID = Column(Integer, primary_key = True)