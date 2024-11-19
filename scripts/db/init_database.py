from configparser import ConfigParser
import os
import pathlib
import psycopg2
import pandas as pd
import numpy as np

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

def df_processing_absence(df:pd.DataFrame):
    "bilan-social-d-edf-sa-absenteisme.csv"
    cols = ["Perimètre juridique", "Année", "Type of contract", "Employee category", "Gender", "Indicator", "Valeur"]
    df = df[cols]
    df.columns = ["ENTERPRISE", "YEAR", "CONTRACT_TYPE", "JOB_TYPE", "GENDER", "ABSENCE_INFO", "ABSENCE_HOURS"]
    df["UID"] = np.arange(0, len(df))
    return df
    
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

def df_processing_handicap(df:pd.DataFrame):
    "../../data/bilan-social-d-edf-sa-salaries-en-situation-de-handicap.csv"
    cols = ["Perimètre juridique", "Année", "Type of contract", "Employee category", "Gender", "Indicator", "Valeur"]
    df = df[cols]
    df.columns = ["ENTERPRISE", "YEAR", "CONTRACT_TYPE", "JOB_TYPE", "GENDER", "HANDICAP_INFO", "HANDICAP_NUMBER"]
    return df

class PromotionTable(Base):
    
    __tablename__ = 'promotion_table'
    __table_args__ = {'schema': 'raw'}    
    ENTERPRISE = Column(String, primary_key=True)
    YEAR = Column(String, primary_key=True)
    CONTRACT_TYPE = Column(String, primary_key=True)
    JOB_TYPE = Column(String, primary_key=True)
    GENDER = Column(String, primary_key=True)
    
    

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
    VALUE = Column(Integer)
    UID = Column(Integer, primary_key = True)

def df_processing_othercond(df:pd.DataFrame):
    "bilan-social-d-edf-sa-autres-conditions-de-travail.csv"
    cols = ["Perimètre juridique", "Année", "Type of contract", "Employee category", "Gender", "Indicator", "Time range", "Valeur"]
    df = df[cols]
    df.columns = ["ENTERPRISE", "YEAR", "CONTRACT_TYPE", "JOB_TYPE", "GENDER", "INFO", "TIME_RANGE", "VALUE"]
    df["UID"] = np.arange(0, len(df))
    return df

class ExtWorkerTable(Base):
    
    __tablename__ = 'exterior_worker_table'
    __table_args__ = {'schema': 'raw'}    
    ENTERPRISE = Column(String, primary_key=True)
    YEAR = Column(String, primary_key=True)
    JOB_TYPE = Column(String, primary_key=True)
    GENDER = Column(String, primary_key=True)
    INFO = Column(String, primary_key = True)
    VALUE = Column(Integer)


def df_processing_extworker(df:pd.DataFrame):
    'bilan-social-d-edf-sa-travailleurs-exterieurs.csv'
    cols = ["Perimètre juridique", "Année", "Employee category", "Gender", "Indicator", "Valeur"]
    df = df[cols]
    df.columns = ["ENTERPRISE", "YEAR", "JOB_TYPE", "GENDER", "INFO", "VALUE"]
    return df




class Age_RangeTable(Base):
    
    __tablename__ = 'age_range_table'
    __table_args__ = {'schema': 'raw'}    
    ENTERPRISE = Column(String)
    YEAR = Column(String)
    CONTRACT_TYPE = Column(String)
    JOB_TYPE = Column(String)
    GENDER = Column(String)
    INFO = Column(String)
    AGE_RANGE = Column(String)
    VALUE = Column(Integer)
    UID = Column(Integer, primary_key = True)


class SeniorityTable(Base):
    
    __tablename__ = 'Seniority_table'
    __table_args__ = {'schema': 'raw'}    
    ENTERPRISE = Column(String)
    YEAR = Column(String)
    CONTRACT_TYPE = Column(String)
    JOB_TYPE = Column(String)
    GENDER = Column(String)
    INFO = Column(String)
    SENIORITY = Column(String)
    VALUE = Column(Integer)
    UID = Column(Integer, primary_key = True)


class NationalityTable(Base):
    
    __tablename__ = 'Nationality_table'
    __table_args__ = {'schema': 'raw'}    
    ENTERPRISE = Column(String)
    YEAR = Column(String)
    CONTRACT_TYPE = Column(String)
    JOB_TYPE = Column(String)
    GENDER = Column(String)
    INFO = Column(String)
    NATIONALITY = Column(String)
    VALUE = Column(Integer)
    UID = Column(Integer, primary_key = True)

def df_processing_effectif_repartition(df):
    'bilan-social-d-edf-sa-effectifs-et-repartition-par-age-statut-et-sexe.csv'
    common_cols = ["Perimètre juridique", "Année", "Type of contract", "Employee category", "Gender", "Indicator"]
    common_final_cols = ["ENTERPRISE", "YEAR", "CONTRACT_TYPE", "JOB_TYPE", "GENDER", "INFO"]

    df_age_range_cols = common_cols + ['Age bracket', 'Valeur']
    final_cols_age_range = common_final_cols + ["AGE_RANGE", "VALUE"]
    df_seniority_cols = common_cols + ['Seniority', 'Valeur']
    final_cols_seniority = common_final_cols + ["SENIORITY", "VALUE"]
    df_Nationality_cols = common_cols + ['Nationality', 'Valeur']
    final_cols_Nationality = common_final_cols + ["NATIONALITY", "VALUE"]

    df_1, df_2, df_3 = [df[df_age_range_cols], df[df_seniority_cols], df[df_Nationality_cols]]

    df_1.columns, df_2.columns, df_3.columns = final_cols_age_range, final_cols_seniority, final_cols_Nationality

    df_1, df_2, df_3 = [df_1[~df_1["AGE_RANGE"].isna()], df_2[~df_2["SENIORITY"].isna()], df_3[~df_3["NATIONALITY"].isna()]]

    df_1["UID"], df_2["UID"], df_3["UID"] = np.arange(0, len(df_1)), np.arange(0, len(df_2)), np.arange(0, len(df_3))

    return df_1, df_2, df_3

def populate_db(engine):

    path_to_data_folder = "data"
    list_of_csv_path = glob.glob(path_to_data_folder + "/*.csv")
    # Extract the filenames from the paths
    csv_file_names = [os.path.basename(file) for file in list_of_csv_path]
    # Set the locale to the default locale (or specify a different one if needed)
    locale.setlocale(locale.LC_COLLATE, locale.getdefaultlocale())
    csv_file_names.sort(key=locale.strxfrm)

    # Define the database connection

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
                    'bilan-social-d-edf-sa-salaries-en-situation-de-handicap.csv': HandicapTable,
                    'bilan-social-d-edf-sa-autres-conditions-de-travail.csv': OtherConditionTable,
                    'bilan-social-d-edf-sa-travailleurs-exterieurs.csv': ExtWorkerTable,
                    #'bilan-social-d-edf-sa-remuneration-et-promotions.csv': AbsenceTable,
                    'bilan-social-d-edf-sa-absenteisme.csv': AbsenceTable,
                    'bilan-social-d-edf-sa-effectifs-et-repartition-par-age-statut-et-sexe.csv': [Age_RangeTable, SeniorityTable, NationalityTable],
    }

    process_mapping = {
                    'data/bilan-social-d-edf-sa-salaries-en-situation-de-handicap.csv': df_processing_handicap,
                    'bilan-social-d-edf-sa-autres-conditions-de-travail.csv': df_processing_othercond,
                    'bilan-social-d-edf-sa-travailleurs-exterieurs.csv': df_processing_extworker,
                    #'bilan-social-d-edf-sa-remuneration-et-promotions.csv': AbsenceTable,
                    'bilan-social-d-edf-sa-absenteisme.csv': df_processing_absence,
                    'bilan-social-d-edf-sa-effectifs-et-repartition-par-age-statut-et-sexe.csv': df_processing_effectif_repartition
    }

    for csv_file_name, table_name in model_mapping.items():
        print(f"Processing: {csv_file_name}")
        csv_path = os.path.join(path_to_data_folder, csv_file_name)
        df = pd.read_csv(csv_path, sep=";")
        # Insert data into tables
        processing_to_apply = process_mapping.get(csv_file_name)
        if processing_to_apply is None:
            continue
        df_processed = processing_to_apply(df)
        if type(df_processed) != list and type(df_processed) != tuple:
            df_processed = [df_processed]
        if type(table_name) != list and type(table_name) != tuple:
            table_name = [table_name]
        for i, d in enumerate(df_processed):
            print(f"Writing to table: {table_name[i]}")
            if type(d) != pd.DataFrame:
                print(type(d), type(df_processed))
            for index, row in d.iterrows():
                record = table_name[i](**row.to_dict())
                session.add(record)
        session.commit()
    session.close()

def reset_table(engine):
    tables = [HandicapTable, OtherConditionTable, ExtWorkerTable, 
              AbsenceTable, Age_RangeTable, SeniorityTable, NationalityTable,
    ]
    for t in tables:
        t.__table__.drop(engine)

if __name__ == '__main__':
    config = load_config()
    print(config)
    DATABASE_URI = f'postgresql+psycopg2://{config.get("user")}:{config.get("password")}@{config.get("host")}:{config.get("port")}/{config.get("database")}'
    engine = create_engine(DATABASE_URI)
    reset_table(engine)
    populate_db(engine)
    # psycopg2.connect(**config)
