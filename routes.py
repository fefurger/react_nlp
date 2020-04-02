from flask import request
from flask_restplus import Resource
from context import searchLocation
import glob
import os
import do_concord

from rest import app, api, upload_parser, parser, ns_graphs, ns_nlp, ns_texts

TEXT_FORMATS = ["txt"]
GRAPH_FORMATS = ["grf"]

@ns_texts.route("/")
class TextsList(Resource):
    def get(self): # get the list of stored texts
        data = []
        for f in glob.glob('./files/*.txt'): # read txt files in static folder
            data.append(f.split('/')[-1].split('\\')[-1])
        return {"response": data}, 200


    @api.expect(upload_parser)
    def post(self): # add a new text
        uploaded_file = request.files['file']
        if uploaded_file.filename[-3:] in TEXT_FORMATS:
            for f in glob.glob('./files/*.txt'):
                if f.split('/')[-1].split('\\')[-1] == uploaded_file.filename:
                    return {"reponse": "'" + uploaded_file.filename + "' already exists"}, 403
            uploaded_file.save(os.path.join('./files/', uploaded_file.filename))
            return {"response": "'" + uploaded_file.filename + "' has been added"}, 200
        else: 
            return {"reponse": "wrong format: text file expected"}, 403




@ns_texts.route("/<string:filename>")
class Text(Resource):
    @api.expect(upload_parser)
    def put(self, filename): # update a text
        uploaded_file = request.files['file']
        if uploaded_file.filename[-3:] in TEXT_FORMATS:
            target = False
            for f in glob.glob('./files/*.txt'):
                if f.split('/')[-1].split('\\')[-1] == uploaded_file.filename:
                    return {"reponse": "'" + uploaded_file.filename + "' already exists"}, 403
                if f.split('/')[-1].split('\\')[-1] == filename:
                    target = True
            if target == False:
                return {"response": "target '" + filename + "' has not been found"}, 403
            try:
                os.remove(os.path.join('./files/', filename))
                uploaded_file.save(os.path.join('./files/', uploaded_file.filename))
                return {"response": "text updated"}, 200
            except:
                return {"response": "something went wrong, text has not been updated"}
        else: 
            return {"reponse": "wrong format: text file expected"}, 403


    def delete(self, filename): # delete a text
        target = False
        for f in glob.glob('./files/*.txt'):
            if f.split('/')[-1].split('\\')[-1] == filename:
                target = True
        if target == False:
            return {"response": "target '" + filename + "' has not been found"}, 403
        try:
            os.remove(os.path.join('./files/', filename))
            return {"response": "text deleted"}, 200
        except:
            return {"response": "something went wrong, text has not been deleted"}




@ns_graphs.route("/")
class GraphsList(Resource):
    def get(self): # get the list of stored texts
        data = []
        for f in glob.glob('./files/*.grf'): # read txt files in static folder
            data.append(f.split('/')[-1].split('\\')[-1])
        return {"response": data}, 200


    @api.expect(upload_parser)
    def post(self): # add a new text
        uploaded_file = request.files['file']
        if uploaded_file.filename[-3:] in GRAPH_FORMATS:
            for f in glob.glob('./files/*.grf'):
                if f.split('/')[-1].split('\\')[-1] == uploaded_file.filename:
                    return {"reponse": "'" + uploaded_file.filename + "' already exists"}, 403
            uploaded_file.save(os.path.join('./files/', uploaded_file.filename))
            return {"response": "'" + uploaded_file.filename + "' has been added"}, 200
        else: 
            return {"reponse": "wrong format: graph file expected"}, 403




@ns_graphs.route("/<string:filename>")
class Graph(Resource):
    @api.expect(upload_parser)
    def put(self, filename): # update a text
        uploaded_file = request.files['file']
        if uploaded_file.filename[-3:] in GRAPH_FORMATS:
            target = False
            for f in glob.glob('./files/*.grf'):
                if f.split('/')[-1].split('\\')[-1] == uploaded_file.filename:
                    return {"reponse": "'" + uploaded_file.filename + "' already exists"}, 403
                if f.split('/')[-1].split('\\')[-1] == filename:
                    target = True
            if target == False:
                return {"response": "target '" + filename + "' has not been found"}, 403
            try:
                os.remove(os.path.join('./files/', filename))
                uploaded_file.save(os.path.join('./files/', uploaded_file.filename))
                return {"response": "graph updated"}, 200
            except:
                return {"response": "something went wrong, graph has not been updated"}
        else: 
            return {"reponse": "wrong format: graph file expected"}, 403

    
    def delete(self, filename): # delete a text
        target = False
        for f in glob.glob('./files/*.grf'):
            if f.split('/')[-1].split('\\')[-1] == filename:
                target = True
        if target == False:
            return {"response": "target '" + filename + "' has not been found"}, 403
        try:
            os.remove(os.path.join('./files/', filename))
            return {"response": "graph deleted"}, 200
        except:
            return {"response": "something went wrong, graph has not been deleted"}



@ns_nlp.route("/<string:graph>&<string:text>")
class PerformNLP(Resource):
    def get(self, graph, text): # get the anaphoras
        
        #GET GRAPH
        target_g = False
        for f in glob.glob('./files/*.grf'):
            if f.split('/')[-1].split('\\')[-1] == graph:
                target_g = True
        if target_g == False:
            return {"response": "target '" + graph + "' has not been found"}, 403
        
        #GET TEXT
        target_t = False
        for f in glob.glob('./files/*.txt'):
            if f.split('/')[-1].split('\\')[-1] == text:
                target_t = True
        if target_t == False:
            return {"response": "target '" + text + "' has not been found"}, 403
        
        ##APPLY GRAPH ON TEXT
        
        #INIT PATHS
        outpath = 'output/'+'_processed.'.join(text.split('.'))
        graph = 'files/' + graph
        text = 'files/' + text
        outputPath = 'files/tmp.txt'
            
        try: # GET PRONOUNS - NLP
            pronouns = do_concord.performNLP(graph, text) 
        except :
            return {"response": "Error while applying graph on text : do_concord.performNLP(graph, text)"}  
         
        try: # READ TEXT
            with open(text, 'r') as tmp: 
                text = tmp.read().replace('\r', '')
        except IOError:
            return {"response": "There was an error while running NLP services"}
            
        try: #GET TAGS & COUPLES - SPARQL
            taggedText, couples = searchLocation(pronouns, text) 
        except:
            return {"response": "Error while applying graph on text : sparql.searchLocation(prounous, text)"} 
            
        try: #WRITE TAGGED_TEXT
            with open(outpath, 'w') as f : 
                f.write(taggedText)
        except IOError:
            return {"response": "Error while writing "}
        
        return {"reponse": couples}, 200