import database_template
import pandas as pd
import inspect

class DatabaseInserter(object):
    def __init__(self, database_object: database_template):
        self.database_object = database_object
    

    def insert_to_db(self, data:dict, session, bulk_insert=False):
    
        session.add(self.database_object(**data))
        if not bulk_insert:
            session.commit()
        
    def select_last_row(self, session, key = "UID"):
        return session.query(self.database_object).order_by(getattr(self.database_object, key).desc()).first()

class TableInserter(object):
    """
    
    To be overloaded by each specific table method for insertion (ie Promotion table, ....)

    """
    def __init__(self, database_object, name = None):
        self.name = name

        self.db_object =  database_object

        self.desired_variables = inspect.getfullargspec(self.db_object)

        self.db_insert = DatabaseInserter(self.db_object)

    def process_data(self, data:pd.DataFrame):
        """
        To be overloaded if needed
        """
        return data

    def insert_df_to_db(self, df, session):
        for index, row in df.iterrows():
            self.db_insert.insert_to_db(data = row, session=session, bulk_insert=True)
        
        session.commit()

    def get_uid_from_table(self, session, key = "UID"):
        data = self.db_insert.select_last_row(session=session)
        return getattr(data, key)


    def insert_data(self, data:pd.DataFrame | dict, session):
        
        if isinstance(data, dict):
            if isinstance(data.get(list(data.keys())[0]), list):
                data = pd.DataFrame(data.copy()) 
            else:
                data = pd.DataFrame(data.copy(), index = [0])
        
        if isinstance(data, pd.DataFrame):
            if len(data.columns) < len(self.desired_variables):
                print(f"Not enough var found")
                return -2
            
            data = self.process_data(data)

            try:
                self.insert_df_to_db(df = data, session = session)
                return 0
            
            except Exception as e:
                print(f"Exception encounter while inserting data: {e}")
                return -1
        else:
            
            raise ValueError("Type not supported")
