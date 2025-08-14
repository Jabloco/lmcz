from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

lmcz_app = Flask(__name__)
lmcz_app.config.from_object(Config)
db = SQLAlchemy(lmcz_app)
migrate = Migrate(lmcz_app, db)

from webapp import routes, models
