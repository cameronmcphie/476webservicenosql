from helper_funs import *
from cassandra.cluster import Cluster

def user_auth():
    if request.method == 'POST':
        # curl -X POST -H "Content-Type: application/json" -d '{"username": "tuvwxyz", "password": "123" }' http://localhost:5000/users
        data = request.get_json()
        username = data['username']
        password = data['password']
        #query = 'SELECT Username FROM discussion_forum.Users WHERE Username=?'
        query = "SELECT Username FROM discussion_forum.Users WHERE Username=%s"
        # conn = sqlite3.connect(DATABASE)
        # cur = conn.cursor()

        cluster = Cluster(['172.17.0.1 ','172.17.0.2'])
        conn = cluster.connect()



        # https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta
        # Was running into an issue regarding the execute statement and needed to include a ',' after data['username'] in order for the query
        # to be ran
        # user = cur.execute(query, (username,)).fetchall()

        print(username)

        user = conn.execute(query, (data['username'], ))



        if user == []:
            # query = 'INSERT INTO Users (Username, Password) VALUES (?, ?);'
            # conn = sqlite3.connect(DATABASE)
            # cur = conn.cursor()
            query = 'INSERT INTO discussion_forum.Users (Username, Password) VALUES (%s, %s);'
            conn.execute(query, ((data['username'], data['password'])))

            # Need to use parameterised queries so API can insert values for username and
            # password into the query at the places with a ?
            # sources:
            # https://stackoverflow.com/questions/32945910/python-3-sqlite3-incorrect-number-of-bindings
            # https://stackoverflow.com/questions/32240718/dict-object-has-no-attribute-id
            # cur.execute(query, (data['username'], data['password']))
            # conn.commit()
            return get_response(201)
        else:
            return get_response(409)

    else:
        return get_response(405)

def change_pass(username):
    if request.method == 'PUT':
        # auth contains the username and Password
        auth = request.authorization

        # check_auth returns True or False depending on the credentials
        #check_auth = NewAuth().check_credentials(auth.username, auth.password)
        if auth_check(auth) is False:
            return get_response(401)

        # password contain the value of the new password after getting it from data with the appropriate key
        data = request.get_json()
        password = data.get('password')

        # Query the db to determine if the username has an account
        query = "SELECT Username FROM Users WHERE Username=?"
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        # https://stackoverflow.com/questions/14861162/cursor-fetchall-returns-extra-characters-using-mysqldb-and-python
        # If using fetchall() there is a potential error because it returns a list of tuples rather than just one tuple
        user = cur.execute(query, [data.get('username')]).fetchone()

        if user == None:
            #print ("hah not found")
            return get_response(404)
        # elif auth is False or auth_check(auth) is False:
        #     #print ("wrong password dummy")
        #     return get_response(401)
        elif auth.username != username or auth.username != data.get('username'):
            #print ("hey you, stop it")
            return get_response(409)
        else:
            query = "UPDATE Users SET Password=? WHERE Username=?"
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute(query, (password, username))
            conn.commit()

            return get_response(200)

    else:
        return get_response(405)
