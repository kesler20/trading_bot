from datetime import timedelta
from flask import Flask, redirect, url_for, render_template, request, session, send_from_directory, flash
import os
from os import path as ps
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import BaseQuery, SQLAlchemy
import datetime
import rsa

# to make the mobile user interface go to https://github.com/alpacahq/alpaca-rn-mobile for inspiration 

create_engine("mysql+pymysql://isokoin:pw@host/db", pool_pre_ping=True)
ROOT_DIR = os.path.dirname(os.getcwd())
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///isokoin.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'top secret!'
app.secret_key = 'password'
app.permanent_session_lifetime = timedelta(minutes=50)
db = SQLAlchemy(app)

#------------------------------ BACKEND FUNCTIONALITY-----------------------------------------------

# this is for index and block 
def textfile_i_o(filename, text, write):
    try:
        file = open(filename, 'r+')
    except FileNotFoundError:
        file = open(filename, 'w')
        file.close()
    file = open(filename, 'r+')
    content = file.read()
    if write:
        file.write(text)
    else:
        pass
    file.close()
    return content

def get_specific_file_extensions_in_cwd(file_extension):
    _dir = os.path.curdir
    files = os.listdir(f'{_dir}')
    specific_files = []
    for file in files:
        if file.endswith(f'{file_extension}'):
            specific_files.append(file)
    return specific_files

def create_transaction_data(transactions, password):
     
    encrypted_password, private_key, public_key = generate_key(password)
    found_user = check_if_registered(encrypted_password)
    if found_user == False:
        return None
    else:
        db.create_all()

        session_data = Transactions(
            session_id=increment_id(Transactions), 
            user_id= found_user.participant_id,
            content = transactions.hash
        )
        db.session.add(session_data)
        db.session.commit()
        return session_data

def update_user_balance(password, ammount):
    db.create_all()
    encrypted_password, private_key, public_key = generate_key(password)
    user = db.session.query(UserAccount).filter_by(password=encrypted_password).first()
    user.balance -= ammount
    db.session.commit()
    return public_key, private_key

def generate_block_number():
    _index = textfile_i_o('block_index.txt','', False)
    _index += 1
    _index = textfile_i_o('block_index.txt',f'{_index}', True)
    return _index

def update_receiver_balance(receiver_username, ammount):
    db.create_all()
    receiver = db.session.query(UserAccount).filter_by(username=receiver_username).first()
    receiver.balance += ammount
    db.session.commit()
    return None

def create_user_data(username, password, public_key):
    
    encrypted_password, private_key, public_key = generate_key(password)
    
    db.create_all()
    session_data = UserAccount(
        participant_id=increment_id(UserAccount),
        username=username, 
        password=encrypted_password,
        public_key=public_key,
        private_key = private_key
    )
    db.session.add(session_data)
    db.session.commit()
    return session_data

def reset(reset_all_users=False, reset_all_posts=False):
    if 'username' in session:
        print('          loading reset .....')
        db.create_all()
        all_users = db.session.query(UserAccount).all()
        all_posts = db.session.query(Transactions).all()
        if reset_all_users:
            for user in all_users:
                users_to_delete = UserAccount.query.filter_by(username=user.participant_id).first()
                db.session.delete(users_to_delete)
                db.session.commit()
        else:
            pass
        if reset_all_posts:
            for post in all_posts:
                posts_to_delete = users_to_delete = Transactions.query.filter_by(session_id=post.session_id).first()
                db.session.delete(posts_to_delete)
                db.session.commit()
        else:
            pass
        print(all_users)
        session.pop('username', None) 
        session.pop('password', None) 
        session.pop('date', None) 
    else:
        pass  
    
def increment_id(column_objct):
    db.create_all()
    users = db.session.query(column_objct).all()
    return len(users) + 1
        
def init_session_(*args):
    for attribute_values in args:
        session[attribute_values] = request.form[attribute_values]     

def check_database_column(column_objct):
    db.create_all()
    datasess = db.session.query(column_objct).all() 
    print(datasess)

def check_if_registered(password):
    encrypted_password, private_key, public_key = generate_key(password)
    db.create_all()
    found_user = db.session.query(UserAccount).filter_by(password=encrypted_password)
    if type(found_user) == BaseQuery:
        return None
    else:
        return found_user

# -------------------------------- DATABASE MODEL OBJECTS----------------------------------------------
class StrategyPerformnce(db.Model):
    default_password, default_key, public_key = generate_key('password')
    __tablename__ = 'user_account'
    participant_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(80), nullable=False, default=f'username{participant_id}')
    password = Column(String(80), nullable=False, default=f'{default_password}', unique=True)
    balance = Column(Integer, nullable=False, default=10000)
    public_key = Column(String(80), nullable=False, default=f'{public_key}', unique=True)
    private_key = Column(String(80), nullable=False, default=f'{default_key}', unique=True)
    transactions = relationship('Transactions', backref='author', lazy=True)
    address =  Column(String(80), nullable=False, default='127.0.0.1:5500')

    def __repr__(self):
        return f'''
        UserAccount(
                username : {self.username},
                participant id : {self.participant_id},
                transactions completed: {self.transactions}
            )
        '''
    
class _PortfolioHistory(db.Model):
    session_id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String(80), nullable=False, default='start session')
    user_id = Column(Integer, ForeignKey('user_account.participant_id'), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())

    def __repr__(self):
        return f'''
            Transactions(
                date : {self.date},
                session id : {self.session_id},
                content: {self.content},
                author : {self.user_id}
            )
        '''
