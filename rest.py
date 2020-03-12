from werkzeug.datastructures import FileStorage
from flask import Flask, request
from flask_restplus import Api, Resource, reqparse
from flask_restplus import reqparse


app = Flask(__name__)

api = Api(app=app, version='0.1', title='Reactive NLP', description='', validate=True)

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)

parser = reqparse.RequestParser()

ns_texts = api.namespace('texts', description = "Texts management")
ns_graphs = api.namespace('graphs', description = "Graphs management")
ns_nlp = api.namespace('nlp', description = "NLP services")

import routes