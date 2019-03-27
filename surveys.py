from flask import Flask ,abort,Response
from flask_mail import Mail, Message
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt
import csv

import requests
import json
from functools import wraps

app =Flask(__name__)
mail=Mail(app)

bcrypt = Bcrypt(app)


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'eng.ahmad.abobakr@gmail.com'
app.config['MAIL_PASSWORD'] = '*********'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/mail'
db = SQLAlchemy(app)

class survey(db.Model):
   id = db.Column('survey_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   email = db.Column(db.String(100))
   ip = db.Column(db.String(100))
   answer = db.Column(db.String(100))




def __init__(self, name,  email, ip , answer ):
   self.name = name

   self.email = email
   self.ip = ip
   self.answer =answer

