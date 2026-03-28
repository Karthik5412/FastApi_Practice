from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

url = 'mssql+pyodbc://@SPOONGBOB\\SQLEXPRESS/Fastapi?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=yes&Encrypt=no&TrustServerCertificate=yes'
engine = create_engine(url)

session = sessionmaker(bind= engine, autoflush= False, autocommit= False)