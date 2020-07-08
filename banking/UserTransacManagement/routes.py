from flask import Blueprint, render_template, flash, redirect, request, jsonify, url_for
from banking.forms import Deposit
from banking.models import Customer, Account, Transaction
from banking import db
from datetime import datetime
from banking import helpers

usertrmgmt = Blueprint("usertrmgmt", __name__, template_folder="templates")


@usertrmgmt.route('/view/account', methods=["POST", "GET"])
def view_account_info():
    user = helpers.is_authenticated()
    if user[1].accType == "CT":
        return render_template("transactionCRUD.html", type="view", user=user[1].name, userdesg=user[1].accType)
    else:
        flash("Not allowed in this view", "danger")
        return redirect(url_for("usermgmt.dashboard"))

@usertrmgmt.route('/api/get/accounts', methods=["POST"])
def api_accounts():
    id = request.get_json()["id"]
    if Customer.query.filter_by(customerid=int(id)).first():
        cust = Customer.query.filter_by(customerid=int(id)).first()
    elif Customer.query.filter_by(ssnid=int(id)).first():
        cust = Customer.query.filter_by(ssnid=int(id)).first()
    json = {'data':list()}
    for i in list(cust.accounts.all()):
        json['data'].append(i.accountid)
    return jsonify(json)
@usertrmgmt.route('/api/info/account', methods=["POST"])
def get_acc_info():
    id = request.get_json()["id"]
    acc = Account.query.filter_by(accountid = int(id)).first()
    return jsonify({
        'cid': acc.customerid,
        'aid': acc.accountid,
        'atype': acc.accType,
        'bal': acc.amount
    })
@usertrmgmt.route('/deposit/account', methods=["POST", "GET"])
def deposit_account():
    user = helpers.is_authenticated()
    if user[1].accType == "CT":
        return render_template("transactionCRUD.html", type="deposit", user=user[1].name, userdesg=user[1].accType)
@usertrmgmt.route('/api/deposit/account', methods=["POST"])
def deposit_api_account():
    id = int(request.get_json()['id'])
    amt = int(request.get_json()['amt'])
    account = Account.query.filter_by(accountid=id).first()
    if account and account.status == "active":
        pb = account.amount
        cust = Customer.query.filter_by(customerid=account.customerid).first()
        cust.message = "Withdrwan money from the linked account"
        account.message = "Money withdrawn from the account"
        account.last_update = datetime.now().strftime("%d-%m-%Y, %H:%M:%S %p")
        cust.last_update = datetime.now().strftime("%d-%m-%Y, %H:%M:%S %p")
        account.amount = pb + amt
        transac = Transaction(customerid=account.customerid, accountid=account.accountid,
                                sourceAccType=account.accType, targetAccType=account.accType, destAccNum=str(id), amount=amt)
        db.session.add(transac)
        db.session.commit()
        return jsonify({
            'aid': id,
            'cid': account.customerid,
            'pb': pb,
            'cb': account.amount
        })
    else:
        return jsonify({'error': "Account might not be created or it is pending to be activated"})
@usertrmgmt.route('/withdraw/account')
def withdraw_account():
    user = helpers.is_authenticated()
    if user[1].accType == "CT":
        return render_template("transactionCRUD.html", type="withdraw", user=user[1].name, userdesg=user[1].accType)

@usertrmgmt.route('/api/withdraw/account', methods=["POST"])
def api_withdraw_account():
    data = request.get_json()
    acc = Account.query.filter_by(accountid=data['id']).first()
    if data['id'] and not data['withdraw'] and acc and acc.status == 'active':
        return jsonify({
            'balance': acc.amount
        })
    elif (data['id'] and not data['withdraw'] and (acc is None or acc.status != 'active')) or (data['id'] and data['withdraw'] and not acc):
        return jsonify({
            'error': "The account cannot be recognized in our database or still the account must be accepted"
        })
    elif data['id'] and data['withdraw'] and acc and acc.status == 'active':
        json = dict()
        json['pb'] = acc.amount
        transac = Transaction(customerid=acc.customerid, accountid=acc.accountid,message="Money withdrawn",
                                sourceAccType=acc.accType, targetAccType=acc.accType, destAccNum=acc.accountid, amount=acc.amount - int(data['amount']))
        print(acc.customerid)
        cust = Customer.query.filter_by(customerid=acc.customerid).first()
        cust.message = "Withdrwan money from the linked account"
        acc.message = "Money withdrawn from the account"
        acc.last_update = datetime.now().strftime("%d-%m-%Y, %H:%M:%S %p")
        cust.last_update = datetime.now().strftime("%d-%m-%Y, %H:%M:%S %p")
        acc.amount = acc.amount - int(data['amount'])
        db.session.add(transac)
        db.session.commit()
        json['aid'] = acc.accountid
        json['cbal'] = acc.amount

        return jsonify(json)

@usertrmgmt.route('/transfer/account')
def transfer_account():
    user = helpers.is_authenticated()
    if user[1].accType == "CT":
        return render_template("transactionCRUD.html", type="transfer", user=user[1].name, userdesg=user[1].accType)

@usertrmgmt.route('/api/transfer/account', methods=['POST'])
def transfer_api_account():
    data = request.get_json()
    acc1 = Account.query.filter_by(accountid = int(data["baid"])).first()
    acc2 = Account.query.filter_by(accountid = int(data["daid"])).first()
    if acc2 and acc1.amount>=int(data["amount"]):
        pb1 = acc1.amount
        pb2 = acc2.amount
        acc1.amount -= int(data['amount'])
        acc2.amount += int(data['amount'])
        acc1.message = "Money debited and transferred from the account"
        acc1.last_update = datetime.now().strftime("%d-%m-%Y, %H:%M:%S %p")
        acc2.message = "Money credited to the account by transfer"
        acc2.last_update = datetime.now().strftime("%d-%m-%Y, %H:%M:%S %p")
        transac = Transaction(customerid=acc1.customerid, accountid=acc1.accountid,message=f"Transfer to account {acc2.accountid}",
                                sourceAccType=acc1.accType, targetAccType=acc2.accType, destAccNum=acc2.accountid, amount=int(data['amount']))
        cust1 = Customer.query.filter_by(customerid = acc1.customerid).first()
        cust2 = Customer.query.filter_by(customerid = acc2.customerid).first()
        cust1.message = "Money debited from the account "+ str(acc1.accountid)
        cust2.message = "Money credited to the account "+ str(acc2.accountid)
        cust1.last_update = datetime.now().strftime("%d-%m-%Y, %H:%M:%S %p")
        cust2.last_update = datetime.now().strftime("%d-%m-%Y, %H:%M:%S %p")
        db.session.add(transac)
        db.session.commit()
        return jsonify({
            'pb1': pb1,
            'pb2': pb2,
            'cb1': acc1.amount,
            'cb2': acc2.amount
        })
    elif acc1.amount<int(data["amount"]):
        return jsonify({
            'error': "Your Account doesnt have required funds to be transferred"
        })
    else:
        return jsonify({
            'error': "The recievers account has not either created or accepted yet"
        })

@usertrmgmt.route('/statement/account')
def account_statement():
    user = helpers.is_authenticated()
    if user[1].accType == "CT":
        return render_template("transactionCRUD.html", type="statement", user=user[1].name, userdesg=user[1].accType)

@usertrmgmt.route("/api/statement/account", methods=['POST'])
def api_statement_account():
    data = request.get_json()
    transacs = Transaction.query.filter_by(accountid=data['id']).all()
    if transacs and not data['bydate']:
        tr = []
        for i in range(len(transacs)):
            x = []
            x.append(i+1)
            x.append(transacs[i].transacDate)
            if transacs[i].accountid == int(transacs[i].destAccNum):
                x.append("credit")
            else:
                x.append('debit')
            x.append(transacs[i].amount)
            tr.append(x)
        if len(tr) >= int(data["transaction"]):
            tr = tr[:int(data["transaction"])]
        return jsonify(tr)
    elif transacs and data["bydate"]:
        transacs_date = db.query(Transaction).filter(Transaction.transacDate >= datetime(data["from"])).filter(Transaction.transacDate<= datetime(data["to"])).\
                                                filter(Transaction.query.filter_by(accountid=data['id'])).all()
        print(transacs_date)
        return {}
    else:
        return jsonify({'error': "Transactions regarding this account number hasnt been initiated yet"})
