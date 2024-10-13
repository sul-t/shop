import psycopg2
import os, sys

db_url = os.environ.get('DATABASE_URL')

if db_url is None:
    sys.exit("error db url")

connection = psycopg2.connect(db_url)