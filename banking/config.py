pu = "127.0.0.1:5432"
puser = "haresh"
ppass = "password"
pdb = "webchat"

class Config:
    SECRET_KEY = "df08a08850e82b6cd9874c58523283ab2d24a2fe0b4daa2017d058111259aa0e"
    SQLALCHEMY_DATABASE_URI = f'postgresql://{puser}:{ppass}@{pu}/{pdb}'
    # 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TEMPLATE_AUTO_RELOAD = True
    DEBUG = True
