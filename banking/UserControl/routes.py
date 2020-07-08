from flask import Blueprint, render_template, flash, redirect, session, url_for
from banking.forms import LoginForm, Register_employee
from banking import globvars as GAV
from banking.models import Employee, Sessions
from banking import bcrypt, db

usercontrol = Blueprint("usercontrol", __name__, template_folder="./templates")

@usercontrol.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = Employee.query.filter_by(name = form.Name.data).first()
        if bcrypt.check_password_hash(u.password, form.Password.data):
            token = u.generate_session_token()
            sess = Sessions(accessKey = token, userSession = u)
            db.session.add(sess)
            db.session.commit()
            session['token'] = token
            if form.Remember.data:
                GAV.time_out_req = 2100
            flash("Successful", "success")
            return redirect(url_for("usermgmt.dashboard"))
        else:
            flash("Bad Password, Try again", "warning")
    return render_template("login.html", form=form, url="usercontrol.login", title="Login")

@usercontrol.route('/app/register', methods=["POST", "GET"])
def register():
    form = Register_employee()
    if form.validate_on_submit() and 'token' not in session:
        password=bcrypt.generate_password_hash(form.Password.data).decode('utf-8')
        u = Employee(name=form.Name.data, email=form.Email.data, password=password, accType=form.Designation.data)
        db.session.add(u)
        db.session.commit()
        flash("Successfully created your account, please login", "success")
        return redirect(url_for("usercontrol.login"))
    return render_template("login.html", form=form, url="usercontrol.register", title="Register")

@usercontrol.route('/logout')
def logout():
    usersession = Sessions.query.filter_by(accessKey = session.get('token')).first()
    db.session.delete(usersession)
    db.session.commit()
    session.pop('token')
    flash("Successfully logged out", 'success')
    return redirect(url_for("usercontrol.login"))
