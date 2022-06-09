from flask_sqlalchemy import SQLAlchemy

USER_DB = 'postgres'
PASS_DB = 'floky'
URL_DB = 'localhost'
NAME_DB = 'data_beitech'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

db = SQLAlchemy()