from banking import db, globvars as GAV
from banking.models import Employee, Sessions, UserSessionExpired
from flask import session
from itsdangerous import SignatureExpired

class UserSessionNotExisted(Exception):
    def __init__(self, args):
        self.args = args

def check_session_data(token):
    try:
        Employee.verify_session_token(token)
    except Exception as e:
        return False
    return True

def is_authenticated():
    token = session.get("token")
    try:
        if token in Sessions.get_active_sessions():
            return (True, Employee.verify_session_token(token))
    except SignatureExpired:
        return False
    return None
