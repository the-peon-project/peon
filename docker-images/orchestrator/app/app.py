from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, marshal, fields

# Initialize Flask
app = Flask(__name__)
api = Api(app)