from flask.ext.sqlalchemy import SQLAlchemy
import sys,os

def setup(app):
    global db
    db = SQLAlchemy(app)

    import server.models.user
    import server.models.meeting

    db.create_all()
