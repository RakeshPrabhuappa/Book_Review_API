import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, User_Credentials

# Load environment variables
load_dotenv()

# Get the database configuration from environment variables
db_name=os.getenv("DB_NAME")
db_user=os.getenv("DB_USER")
db_password=os.getenv("DB_PASSWORD")
db_host=os.getenv("DB_HOST")
db_port=os.getenv("DB_PORT")

# Construct the database URL
url=f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Create the engine and bind it to the Base class
engine=create_engine(url)
Base.metadata.create_all(engine)

# Create a session
Session=sessionmaker(bind=engine)
session=Session()