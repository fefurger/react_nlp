from flask import request
from flask_restplus import Resource


from rest import app, api, upload_parser, parser, ns_graphs, ns_nlp, ns_texts

@ns_texts.route("/")
class TextsList(Resource):
    def get(self): # get the list of stored texts
        # TO_DO
        return {"response": []}, 200

    @api.expect(upload_parser)
    def post(self): # add a new text
        uploaded_file = args['file']
        # TO_DO
        return {"response": "text added"}, 204




@ns_texts.route("/<string:filename>")
class Text(Resource):
    @api.expect(upload_parser)
    def put(self, filename): # update a text
        uploaded_file = args['file']
        # TO_DO
        return {"response": "text updated"}, 204

    def delete(self, filename): # delete a text
        # TO_DO
        return {"reponse": "text deleted"}, 200




@ns_graphs.route("/")
class GraphsList(Resource):
    def get(self): # get the list of stored graphs
        # TO_DO
        return {"response": []}, 200

    @api.expect(upload_parser)
    def post(self): # add a new graph
        uploaded_file = args['file']
        # TO_DO
        return {"response": "graph added"}, 204




@ns_graphs.route("/<string:filename>")
class Text(Resource):
    @api.expect(upload_parser)
    def put(self, filename): # update a graph
        uploaded_file = args['file']
        # TO_DO
        return {"response": "graph updated"}, 204

    def delete(self, filename): # delete a graph
        # TO_DO
        return {"reponse": "graph deleted"}, 200



@ns_nlp.route("/")
class PerformNLP(Resource):
    def get(self): # get the anaphoras
        args = parser.parse_args()
        nlp_to_use = args['nlp']
        # TO_DO
        return {"reponse": []}, 200