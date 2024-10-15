import os, sys

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

db_url = os.environ.get('DATABASE_URL')

if db_url is None:
    sys.exit("error db url")

connection = create_engine(db_url)
session = Session(connection)