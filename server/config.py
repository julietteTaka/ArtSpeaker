import os
import pymongo
import ConfigParser
from flask import Flask

APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 

config =  ConfigParser.ConfigParser()
config.read(os.path.join(APP_ROOT, 'server.cfg'))

serverPort = config.getint('APP_SERVER', 'port')
client = pymongo.MongoClient(config.get('MONGODB', 'hostname'), config.getint('MONGODB', 'port'))
db = client.__getattr__(config.get('MONGODB', 'dbName'))
portfolioTable = db.__getattr__(config.get('MONGODB', 'portfolioTable'))
userTable = db.__getattr__(config.get('MONGODB', 'userTable'))
offerTable = db.__getattr__(config.get('MONGODB', 'offerTable'))

g_app = Flask(__name__)