import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import mimetypes


# Contains all the environmental variables needed
def setConfig(app):
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/mercadata'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

    UPLOAD_FOLDER = 'public/user_images'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Initialize APP
app = Flask(__name__, template_folder='../templates', static_folder="../static")
CORS(app)
setConfig(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

# Initialize APP
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

