import os
print('cwd:', os.path.abspath('.'))
import app as m
print('app.config[SQLALCHEMY_DATABASE_URI]=', m.app.config.get('SQLALCHEMY_DATABASE_URI'))
from models import db
with m.app.app_context():
    print('db.engine.url:', db.engine.url)
    try:
        from sqlalchemy import inspect
        insp = inspect(db.engine)
        print('tables via inspector:', insp.get_table_names())
    except Exception as e:
        print('inspector error', e)
