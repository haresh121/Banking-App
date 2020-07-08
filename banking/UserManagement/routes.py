from flask import Blueprint, render_template, flash, redirect, request, jsonify, url_for
from banking.forms import NewCustomer, NewAccount
from banking.models import Customer, Account
from banking import db
from datetime import datetime
from banking import helpers

usermgmt = Blueprint("usermgmt", __name__, template_folder="templates")


@usermgmt.route("/")
def dashboard():
    user = helpers.is_authenticated()
    if user[1].accType == "NCE":
        inactiveusers = list(Customer.query.filter_by(
            status='inactive')) + list(Account.query.filter_by(status='inactive'))
        inactiveaccounts = list(db.engine.execute("""select account.customerid, name, ssnid, account.status, account.accountid from customer, account
                                                  where customer.customerid=account.customerid and account.status='pending'"""
                                                  ))
        return render_template("dashboard.html", title="Dashboard", user=user[1].name, userdesg=user[1].accType,
                               inactiveusers=inactiveusers, inactiveaccounts=inactiveaccounts)
    elif user[1].accType == "CT":
        return render_template("dashboard.html", title="Dashboard", user=user[1].name, userdesg=user[1].accType)

@usermgmt.route('/new/customer', methods=["POST", "GET"])
def newcustomer():
    user = helpers.is_authenticated()
    if user[1].accType == "NCE":
        form = NewCustomer()
        if form.validate_on_submit():
            print("entering Done")
            addr = form.Address.data + ", " + form.City.data + ", " + form.State.data
            u = Customer(ssnid=int(form.Ssnid.data), name=form.Name.data,
                         status="inactive", age=int(form.Age.data), address=addr)
            db.session.add(u)
            db.session.commit()
            flash("New Customer created successfully, please wait to get verified", "success")
        return render_template("customerCRUD.html", form=form, title="New Customer", type="create", user=user[1].name, userdesg=user[1].accType)
    else:
        flash("You are not allowed to enter this view, contact your supervisor", "danger")
        return redirect(url_for("usermgmt.dashboard"))


@usermgmt.route('/update/customer', methods=["POST", "GET"])
def update_customer():
    user = helpers.is_authenticated()
    if user[1].accType == "NCE":
        if request.method == "POST":
            customer_details = Customer.query.filter_by(customerid=int(
                request.get_json()["cid"]), status="active").first()
            customer_details.name = request.get_json()["name"]
            customer_details.ssnid = int(request.get_json()["ssnid"])
            customer_details.age = int(request.get_json()["age"])
            customer_details.address = request.get_json()["addr"]
            customer_details.message = "Account Updated"
            customer_details.last_update = datetime.now().strftime("%d-%m-%Y, %H:%M:%S %p")
            db.session.commit()
            flash("Successfully Updated", "success")
        return render_template("customerCRUD.html", title="Update Customer", type="update", user=user[1].name, userdesg=user[1].accType)
    else:
        flash("You are not allowed to enter this view, contact your supervisor", "danger")
        return redirect(url_for("usermgmt.dashboard"))


@usermgmt.route('/api/customer', methods=["POST"])
def get_customer():
    if 'cid' in request.get_json():
        cid = int(request.get_json()['cid'])
        customer_details = Customer.query.filter_by(
            customerid=cid, status="active").first()
        if customer_details:
            cdict = {
                'name': customer_details.name,
                'cid': customer_details.customerid,
                'ssnid': customer_details.ssnid,
                'age': customer_details.age,
                'address': customer_details.address
            }
        else:
            cdict = {"Error": "No user with given Customer ID"}
    elif 'ssnid' in request.get_json():
        ssnid = int(request.get_json()['ssnid'])
        customer_details = Customer.query.filter_by(
            ssnid=ssnid, status="active").first()
        if customer_details:
            cdict = {
                'name': customer_details.name,
                'cid': customer_details.customerid,
                'ssnid': customer_details.ssnid,
                'age': customer_details.age,
                'address': customer_details.address
            }
        else:
            cdict = {"Error": "No user with given SSN ID or might be inactive"}
    return jsonify(cdict)


@usermgmt.route('/api/activate/<type>')
def accept(type):
    if type == "customer":
        cid = int(request.args.get('id'))
        customer_details = Customer.query.filter_by(customerid=cid).first()
        customer_details.status = "active"
        customer_details.message = "User activated"
        customer_details.last_update = datetime.now().strftime("%d-%m-%Y, %H:%M:%S %p")
        db.session.commit()
    elif type == "account":
        aid = int(request.args.get('id'))
        account_details = Account.query.filter_by(accountid=aid).first()
        if Customer.query.filter_by(customerid=account_details.customerid, status="inactive").first():
            flash("Customer Not activated", "danger")
        else:
            account_details.status = "active"
            account_details.message = "Account activated"
            account_details.last_update = datetime.now().strftime("%d-%m-%Y, %H:%M:%S %p")
            db.session.commit()
    return redirect(url_for('usermgmt.dashboard'))


@usermgmt.route('/api/delete', methods=["POST"])
def delete_customer():
    id = request.get_json()
    if "cid" in id and "aid" not in id:
        cust = Customer.query.filter_by(customerid=id["cid"]).first()
        db.session.delete(cust)
        db.session.commit()
        return jsonify({"success": True})
    if "cid" in id and "aid" in id:
        acc = Account.query.filter_by(customerid=id["cid"], accountid=id["aid"]).first()
        db.session.delete(acc)
        db.session.commit()
        return jsonify({"success": True})


@usermgmt.route('/view/customers')
def view_customers():
    user = helpers.is_authenticated()
    if user[1].accType == "NCE":
        customers = Customer.query.all()
        accounts = list(db.engine.execute("""select account.customerid, accountid, customer.name, customer.ssnid, account.status,account.last_update, "accType", amount from customer, account
                                        where customer.customerid = account.customerid and account.status = 'active'"""))
        return render_template("customerCRUD.html", title="View All Customers", type="read", user=user[1].name, userdesg=user[1].accType, customers=customers, accounts=accounts)
    else:
        flash("You are not allowed to enter this view, contact your supervisor", "danger")
        return redirect(url_for("usermgmt.dashboard"))


@usermgmt.route('/new/account', methods=["POST", "GET"])
def new_account():
    user = helpers.is_authenticated()
    if user[1].accType == "NCE":
        form = NewAccount()
        if form.validate_on_submit():
            newAcc = Account(customerid=form.Cid.data,
                             accType=form.account.data, amount=form.deposit.data)
            db.session.add(newAcc)
            db.session.commit()
            flash("Account creation successful and is to be verified", category="success")
            return redirect(url_for('usermgmt.dashboard'))
        return render_template("accountCRUD.html", form=form, title="New Account",
                               type="read", user=user[1].name, userdesg=user[1].accType)
    else:
        flash("You are not allowed to enter this view, contact your supervisor", "danger")
        return redirect(url_for("usermgmt.dashboard"))
