import banking
from flask import flash, url_for, session, redirect, request
from banking import helpers
from banking.models import Sessions

app = banking.create_app()
with app.app_context():
    banking.db.init_app(app)
    banking.bcrypt.init_app(app)
    banking.mail.init_app(app)

@app.before_request
def require_login():
    allowed_routes = ['usercontrol.login',
                      'usercontrol.register', 'static']
    if 'token' not in session and request.endpoint not in allowed_routes:
        flash("Please login or Register to enter this view", 'warning')
        return redirect(url_for("usercontrol.login", next=request.endpoint))
    elif 'token' in session.keys():
        if not helpers.check_session_data(session.get('token')):
            usersession = Sessions.query.filter_by(
                accessKey=session.get('token')).first()
            try:
                banking.db.session.delete(usersession)
            except AttributeError:
                pass
            banking.db.session.commit()
            session.pop('token')
            flash("Please login again, session Expired", "danger")
            return redirect(url_for("usercontrol.login"))
        else:
            pass
    elif request.endpoint == 'usercontrol.logout' and 'token' not in session:
        flash("Entered into wrong realm without valid token", 'error')
        return redirect(url_for("usercontrol.login"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
