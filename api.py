from flask import Flask, request, jsonify, g, Response
from flask_basicauth import BasicAuth
import sqlite3
import json
from datetime import datetime
from time import gmtime, strftime
from forums import forum
from threads import thread
from posts import post
from user import user_auth, change_pass
from helper_funs import *

app = Flask(__name__)
app.config["DEBUG"] = True

# Global db variable
DATABASE = 'forum.db'

#list available discussion forums GET
#TODO: get import working
@app.route('/forums', methods=['GET', 'POST'])
def process_forum_request():
     return forum()

#list threads in the specified forum GET
@app.route('/forums/<forum_id>', methods=['GET', 'POST'])
def process_thread_request(forum_id):
    return thread(forum_id)


#list posts to the specified thread GET
@app.route('/forums/<forum_id>/<thread_id>', methods=['GET', 'POST'])
def process_posts_request(forum_id, thread_id):
    return post(forum_id, thread_id)
    

@app.route('/users', methods=['POST'])
def process_user_login_request():
    return user_auth()

#changes a user's password PUT
@app.route('/users/<username>', methods=['PUT'])
def process_change_pw_request(username):
    return change_pass(username)

if __name__ == "__main__":
    app.run()
