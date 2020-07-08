from banking import db, globvars as GAV
from sqlalchemy.schema import Sequence
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from flask import current_app as app, g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, TimestampSigner, SignatureExpired
from datetime import datetime

class UserSessionExpired(Exception):
    def __init__(self):
        pass


class Employee(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(1000), nullable=False)
    accType = Column(String(50), nullable=False)
    sessions = db.relationship(
        'Sessions', backref="userSession", lazy="dynamic")

    def generate_session_token(self):
        timer = TimestampSigner(app.config["SECRET_KEY"])
        token = Serializer(app.config["SECRET_KEY"])
        return timer.sign(token.dumps({'userId': int(self.id)}).decode('utf-8')).decode('utf-8')

    @staticmethod
    def verify_session_token(token):
        timer = TimestampSigner(app.config["SECRET_KEY"])
        serial = Serializer(app.config["SECRET_KEY"])
        global user_dict
        exp = GAV.time_out_req
        try:
            sess_token = timer.unsign(token, max_age=exp)
            userid = serial.loads(sess_token)["userId"]
        except Exception as e:
            raise SignatureExpired("Entered signature Expired")
        return Employee.query.get(userid)

    def get_dict(self):
        u = {
            "id": self.id,
            "Username": self.name,
            "email": self.email,
            "sessions": Sessions.get_active_user_sessions(self.id)
        }
        return u

    def __repr__(self):
        return f"{self.name}==>{self.email},{self.accType}"


class Sessions(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    accessKey = Column(String(1000), nullable=False)
    sessionStartTime = Column(DateTime, default=datetime.now)
    sessionActive = Column(Boolean, unique=False, default=True)
    userId = Column(Integer, ForeignKey('employee.id'))

    @staticmethod
    def get_active_sessions():
        active_sessions = Sessions.query.filter_by(sessionActive=True).all()
        if active_sessions is None:
            return None
        else:
            for i in range(len(active_sessions)):
                active_sessions[i] = active_sessions[i].accessKey
            return active_sessions

    @staticmethod
    def get_active_user_sessions(id):
        active_sessions = Sessions.query.filter_by(
            userId=id, sessionActive=True).all()
        if active_sessions is None:
            return None
        else:
            for i in range(len(active_sessions)):
                active_sessions[i] = active_sessions[i].accessKey
            return active_sessions

class Customer(db.Model):
    customerid = Column(Integer, Sequence('customer_cid_seq', start=100000001, increment=1), primary_key=True)
    ssnid = Column(Integer, nullable=False, unique=True)
    name = Column(String(200), nullable=False)
    status = Column(String(40), nullable=False)
    message = Column(String(300), nullable=True, default="Account creation processs started")
    last_update = Column(String(50), nullable=True, default=datetime.now().strftime("%d-%m-%Y %H:%M:%S %p"))
    age = Column(Integer, nullable=False)
    address = Column(String(500), nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)
    accounts = db.relationship("Account", backref="userAccounts", lazy="dynamic")
    def __repr__(self):
        return(f"Customer -- name:{self.name}, customerId:{self.customerid}, status:{self.status}")

class Account(db.Model):
    accountid = Column(Integer, Sequence('account_aid_seq', start=200000001, increment=1), primary_key=True, nullable=False)
    customerid = Column(Integer, ForeignKey("customer.customerid"))
    accType = Column(String(20), nullable=False, default="savings")
    status = Column(String(30), default="pending", nullable=False)
    message = Column(String(50), nullable=False, default="Account created")
    amount = Column(Integer, nullable=False, default=0)
    deleted = Column(Boolean, nullable=False, default=False)
    last_update = Column(String(50), nullable=False, default=datetime.now().strftime("%d-%m-%Y %H:%M:%S %p"))
    transacid = db.relationship("Transaction", backref="transactions", lazy="dynamic")

class Transaction(db.Model):
    transacid = Column(Integer, Sequence('transac_tid_seq', start=300000001, increment=1), primary_key=True, nullable=False)
    customerid = Column(Integer, ForeignKey("customer.customerid"))
    accountid = Column(Integer, ForeignKey("account.accountid"))
    message = Column(String(200), nullable=False, default="Trasaction Done")
    transacDate = Column(String(50), nullable=False, default=datetime.now().strftime("%d-%m-%Y %H:%M:%S %p"))
    sourceAccType = Column(String(20), nullable=False)
    targetAccType = Column(String(20), nullable=False)
    destAccNum = Column(String(20), nullable=False)
    amount = Column(Integer, nullable=False, default=0)
