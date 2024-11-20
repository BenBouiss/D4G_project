from database_insertion import TableInserter, database_template
from init_database import load_config

import sqlalchemy
import pandas as pd

class AbsenceTableInsert(TableInserter):
    def __init__(self, name=None):
        super().__init__(database_object=database_template.AbsenceTable, name=name)

class NationalityTableInsert(TableInserter):
    def __init__(self, name=None):
        super().__init__(database_object=database_template.NationalityTable, name=name)

class SeniorityTableInsert(TableInserter):
    def __init__(self, name=None):
        super().__init__(database_object=database_template.SeniorityTable, name=name)

class AgeRangeTableInsert(TableInserter):
    def __init__(self, name=None):
        super().__init__(database_object=database_template.AgeRangeTable, name=name)

class ExteriorWorkerTableInsert(TableInserter):
    def __init__(self, name=None):
        super().__init__(database_object=database_template.ExtWorkerTable, name=name)

class HandicapTableInsert(TableInserter):
    def __init__(self, name=None):
        super().__init__(database_object=database_template.HandicapTable, name=name)

class OtherConditionTableInsert(TableInserter):
    def __init__(self, name=None):
        super().__init__(database_object=database_template.OtherConditionTable, name=name)

class PromotionTableInsert(TableInserter):
    def __init__(self, name=None):
        super().__init__(database_object=database_template.PromotionTable, name=name)


if __name__ == "__main__":
    print("Ben")
    config = load_config()

    DATABASE_URI = f'postgresql+psycopg2://{config.get("user")}:{config.get("password")}@{config.get("host")}:{config.get("port")}/{config.get("database")}'
    engine = sqlalchemy.create_engine(DATABASE_URI)

    session = sqlalchemy.orm.sessionmaker(bind = engine)()
    
    Test_data = {"ENTERPRISE": "BEN", "YEAR": 2024, "CONTRACT_TYPE": "BEN", "JOB_TYPE": "BEN", "GENDER": "BEN", "ABSENCE_INFO": "BEN",
                 "ABSENCE_HOURS": 1000, "UID": 9999}
    
    inserter = AbsenceTableInsert()

    inserter.insert_data(data=Test_data, session=session)