from flask_wtf import FlaskForm
from banking.models import Employee, Customer, Account, Transaction
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.fields.html5 import EmailField, SearchField, DecimalField
from wtforms.validators import InputRequired, EqualTo, ValidationError, DataRequired, Length, Email

class LoginForm(FlaskForm):
    Name = StringField('Name', validators=[DataRequired()])
    Password = PasswordField('Password', validators=[DataRequired()])
    Remember = BooleanField('remember me for 2hrs?')
    Submit = SubmitField('Login')
    def validate_Name(self, Name):
        user = Employee.query.filter_by(name=Name.data).first()
        if not user:
            raise ValidationError('Entered Name does not exist in database, Please check with your higher officials')

class Register_employee(FlaskForm):
    Name = StringField('Name', validators=[DataRequired(), Length(max=25)])
    Email = EmailField("Email", validators=[DataRequired(), Email()])
    Designation = SelectField('Your Designation', validators=[DataRequired()],
                            choices = [('', '----select----'),
                                        ('NCE', 'New Customer Executive'),
                                        ('CT', 'Cashier/Teller')
                                        ]
                        )
    Password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=16, message="Please enter a password with min 6 letters")])
    Confirm_Password = PasswordField('Confirm_Pass', validators=[DataRequired(), EqualTo('Password', message="Passwords don't match")])
    Submit = SubmitField('Submit')
    def validate_Name(self, Name):
        user = Employee.query.filter_by(name=Name.data).first()
        if user:
            raise ValidationError('Please login, Username existed')

class NewCustomer(FlaskForm):
    Ssnid = StringField("SSNID", validators=[DataRequired(), Length(min=9, max=9)])
    Name = StringField("Name", validators=[DataRequired()])
    Age = DecimalField("Age", validators=[DataRequired()])
    Address = StringField("Address", validators=[DataRequired()])
    City = StringField("City", validators=[DataRequired()])
    State = StringField("State", validators=[DataRequired()])
    Submit = SubmitField('Submit')
    def validate_Ssnid(self, Ssnid):
        user = Customer.query.filter_by(ssnid=Ssnid.data).first()
        if user:
            raise ValidationError('A Customer already exists with the given SSNID please check again or update the account')

class NewAccount(FlaskForm):
    Cid = StringField("Customer ID", validators=[DataRequired(), Length(min=9, max=9)])
    account = SelectField('Type of Account',
                            choices = [('', 'select type of account'),
                                        ('savings', 'Savings Account'),
                                        ('current', 'Current Account')
                                        ]
                        )
    deposit = DecimalField("Deposit Amount", validators=[DataRequired()])
    Submit = SubmitField('Submit')
    def validate_Cid(self, Cid):
        cust = Customer.query.filter_by(customerid=Cid.data).first()
        if not cust:
            raise ValidationError("Sorry, entered customer id doesnt match with our records please verify")
    def validate_deposit(self, deposit):
        if int(deposit.data) < deposit.data:
            raise ValidationError("Enter a valid Amount without decimal points")
    def validate_account(self, account):
        if account.data == '':
            raise ValidationError("Please select a valid type of Account")

class Deposit(FlaskForm):
    Accountid = StringField("Account ID", validators=[DataRequired(), Length(min=9, max=9)])
    Amount = DecimalField("Deposit Amount", validators=[DataRequired()])
    Submit = SubmitField('Submit')
    def validate_deposit(self, deposit):
        if int(deposit.data) < deposit.data:
            raise ValidationError("Enter a valid Amount without decimal points")
