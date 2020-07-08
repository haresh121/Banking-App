from banking import create_app
from banking import db
from flask_script import Manager

app = create_app()
manager = Manager(app)

@manager.command
def create_db():
    with app.app_context():
        db.init_app(app)
        db.create_all()
        db.session.commit()
@manager.command
def drop_db():
    with app.app_context():
        db.init_app(app)
        db.drop_all()
        db.session.commit()
@manager.command
def reinstate():
    with app.app_context():
        db.init_app(app)
        db.drop_all()
        db.create_all()
        db.session.commit()

if __name__ == "__main__":
    manager.run()
