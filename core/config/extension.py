from sqlalchemy import create_engine

server = 'DBDEV'
database = 'db_autotest'
driver = 'ODBC Driver 17 for SQL Server'
database_connection_string = f'mssql://@{server}/{database}?driver={driver}'
engine = create_engine(database_connection_string)
db = engine.connect()


