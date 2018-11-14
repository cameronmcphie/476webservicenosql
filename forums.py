from helper_funs import *

def forum():
    #creating a new discussion forum
    if request.method == 'POST':
        # auth contains the username and Password
        auth = request.authorization

        if auth_check(auth) is False:
            return get_response(401)

        forum_submit = request.get_json()
        #parse the name from JSON
        forum_name = forum_submit.get('name')
        # If forumn name does't exist insert it into the db and return success
        if query_db('SELECT ForumsName from Forums where ForumsName = ?', [request.get_json().get('name')], one=True) is None:
            query = 'INSERT into Forums (CreatorId, ForumsName) Values ((Select UserId from Users where Username = ?), ?);'
            conn = get_db()
            cur = conn.cursor()
            cur.execute(query, (auth.username, str(forum_name)))
            forum = cur.execute('SELECT last_insert_rowid() as ForumId;').fetchall()
            forumid = dict(forum[0]).get('ForumId')
            conn.commit()
            conn.close()
            return get_response(201, body=None, location=('/forums/'+str(forumid)))
        else:
            return get_response(409)
    #request for all the present forums
    elif request.method == 'GET':
        query = 'SELECT Users.Username as creator, Forums.ForumId as id, Forums.ForumsName as name FROM Forums, Users where CreatorId = UserId;'
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        all_forums = cur.execute(query).fetchall()

        return jsonify(all_forums)
    else:
        return get_response(405)

