from configparser import ConfigParser
import os
import pathlib
import psycopg2

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    print('Loading config')
    Cur_path = pathlib.Path(__file__).parent.absolute()
    Target_file = os.path.join(Cur_path , filename)
    parser.read(Target_file)
    # get section, default to postgresql
    config = {} 
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config

# db
from sqlalchemy import create_engine, Column, Integer, String, Date, Time, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Mapped
from sqlalchemy.schema import CreateSchema
from typing import List, Optional

# csv to df
import locale

import os 
import glob

# Docker launched with
# sudo docker run --name postgres-db  -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -v database_mount:/var/lib/postgresql/data -d postgres

Base = declarative_base()

# Define the models with foreign keys and relationships

class AbsenceTable(Base):
    
    __tablename__ = 'absence_table'
    __table_args__ = {'schema': 'raw'}    
    ENTERPRISE = Column(String, primary_key=True)
    YEAR = Column(String, primary_key=True)
    CONTRACT_TYPE = Column(String, primary_key=True)
    JOB_TYPE = Column(String, primary_key=True)
    GENDER = Column(String, primary_key=True)
    ABSENCE_INFO = Column(String)
    ABSENCE_DAYS = Column(Integer)

    
class HandicapTable(Base):
    
    __tablename__ = 'handicap_table'
    __table_args__ = {'schema': 'raw'}    
    ENTERPRISE = Column(String, primary_key=True)
    YEAR = Column(String, primary_key=True)
    CONTRACT_TYPE = Column(String, primary_key=True)
    JOB_TYPE = Column(String, primary_key=True)
    GENDER = Column(String, primary_key=True)
    HANDICAP_INFO = Column(String, primary_key=True)

    HANDICAP_NUMBER = Column(Integer)
    
class PromotionTable(Base):
    
    __tablename__ = 'promotion_table'
    __table_args__ = {'schema': 'raw'}    
    ENTERPRISE = Column(String, primary_key=True)
    YEAR = Column(String, primary_key=True)
    CONTRACT_TYPE = Column(String, primary_key=True)
    JOB_TYPE = Column(String, primary_key=True)
    GENDER = Column(String, primary_key=True)
    

class FormationTable(Base):
    """
    
    Subtility found where
    
    """
    

class OtherConditionTable(Base):
    
    __tablename__ = 'other_condition_table'
    __table_args__ = {'schema': 'raw'}    
    ENTERPRISE = Column(String, primary_key=True)
    YEAR = Column(String, primary_key=True)
    CONTRACT_TYPE = Column(String, primary_key=True)
    JOB_TYPE = Column(String, primary_key=True)
    GENDER = Column(String, primary_key=True)
    
    INFO = Column(String, primary_key = True)
    TIME_RANGE = Column(String)
    VALUE = Column(Integer)

class ExtWorkerTable(Base):
    
    __tablename__ = 'exterior_worker_table'
    __table_args__ = {'schema': 'raw'}    
    ENTERPRISE = Column(String, primary_key=True)
    YEAR = Column(String, primary_key=True)
    CONTRACT_TYPE = Column(String, primary_key=True)
    JOB_TYPE = Column(String, primary_key=True)
    GENDER = Column(String, primary_key=True)
    INFO = Column(String, primary_key = True)
    VALUE = Column(Integer)

class AbsenteismeTable(Base):
    
    __tablename__ = 'exterior_worker_table'
    __table_args__ = {'schema': 'raw'}    
    ENTERPRISE = Column(String, primary_key=True)
    YEAR = Column(String, primary_key=True)
    CONTRACT_TYPE = Column(String, primary_key=True)
    JOB_TYPE = Column(String, primary_key=True)
    GENDER = Column(String, primary_key=True)
    INFO = Column(String, primary_key = True)
    VALUE = Column(Integer)


if __name__=="__main__":

    path_to_data_folder = "../../data"
    list_of_csv_path = glob.glob(path_to_data_folder + "/*.csv")
    # Extract the filenames from the paths
    csv_file_names = [os.path.basename(file) for file in list_of_csv_path]
    # Set the locale to the default locale (or specify a different one if needed)
    locale.setlocale(locale.LC_COLLATE, locale.getdefaultlocale())
    csv_file_names.sort(key=locale.strxfrm)

    # Define the database connection
    DATABASE_URI = 'postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres'
    engine = create_engine(DATABASE_URI)
    with engine.connect() as connection:
        connection.execute(CreateSchema("raw", if_not_exists=True))
        connection.commit()

    Base.metadata.drop_all(engine)
    # Create all tables
    Base.metadata.create_all(engine)

    # Load data from CSV files and insert into the database

    Session = sessionmaker(bind=engine)
    session = Session()

    # Define model mapping
    model_mapping = {
                    '../../data/bilan-social-d-edf-sa-salaries-en-situation-de-handicap.csv': HandicapTable,
                    'bilan-social-d-edf-sa-autres-conditions-de-travail.csv': OtherConditionTable,
                    'bilan-social-d-edf-sa-travailleurs-exterieurs.csv': ExtWorkerTable,
                    #'bilan-social-d-edf-sa-remuneration-et-promotions.csv': AbsenceTable,
                    'bilan-social-d-edf-sa-absenteisme.csv': AbsenceTable,
                    'bilan-social-d-edf-sa-effectifs-et-repartition-par-age-statut-et-sexe.csv': AbsenceTable,
    }

    labels = []
    df_list = []
    df_dict = {}
    nb=0
    for csv_file_name, table_name in model_mapping.items():
        csv_path = os.path.join(path_to_data_folder, csv_file_name)
        df = csv_to_df.csv_path_to_df(csv_path)
        # Insert data into tables
        for index, row in df.iterrows():
            record = table_name(**row.to_dict())
            session.add(record)
    session.commit()
    session.close()


if __name__ == '__main__':
    config = load_config()
    print(config)
    psycopg2.connect(**config)
