from flask import Flask, request, jsonify, g, Response
from flask_basicauth import BasicAuth
import sqlite3
import json
from datetime import datetime
from time import gmtime, strftime

# Global db variable
DATABASE = 'forum.db'

app = Flask(__name__)

# From http://flask.pocoo.org/docs/1.0/patterns/sqlite3/
# Connects to and returns the db used in init_db() and query_db()
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = dict_factory
    return db

# From http://flask.pocoo.org/docs/1.0/patterns/sqlite3/
# Closes the db at the end of each rquest for get_db()
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# From http://flask.pocoo.org/docs/1.0/patterns/sqlite3/
# query: query as string; e.g. 'Select * from Users'
# args: query arguments, leave empty if no args; e.g. ['user', 'password']
# one: Set to true if only 1 row is required for query else keep false
# returns results of the query
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# dictionary function taken from programminghistorian for placement purposes
def dict_factory(cursor, row):
    d={}
    for idx, col in enumerate(cursor.description):
        d[col[0]]= row[idx]
    return d

#subclass of BasicAuth (based off Flask-BasicAuth extension)
class NewAuth(BasicAuth):
    #override of check_credentials
    # returns true if the username and password matches else returns false
    def check_credentials(self, username, password):
        user = query_db('SELECT Username, Password from Users where Username = ? and password = ?', [username, password], one=True)
        if user is not None:
            return True
        else:
            return False

#function to check the auth object for present authorization
def auth_check(auth):
    #auth = request.authorization
    if (auth) == None:
        return False
    else:
        # check_auth returns True or False depending on the credentials
        check_auth = NewAuth().check_credentials(auth.username, auth.password)
        if check_auth is False:
            return False

# returns a JSON response with status code and optional body and location
def get_response(status, body=None, location=None):
    if body != None:
        response = jsonify(body)
    else:
        response = jsonify()
    response.status_code = status
    if location != None:
        response.headers['Location'] = location
    return response

# from http://blog.luisrei.com/articles/flaskrest.html
@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp
