from helper_funs import *
from cassandra.cluster import Cluster


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
        
        # Possible implementation for GET and POST of forums
        # forums
        # POST
        # INSERT INTO discussion_forum.Content (forumid, forumcreator, forumtitle, postid, postauthor, posttimestamp, posttext)
        # VALUES (?, ?, ?, ?, ?, ?, ?)

        # forum_post_stmt = session.prepare("
        #                   INSERT INTO discussion_forum.Content (forumid, forumcreator, forumtitle, postid, postauthor, posttimestamp, posttext)
        #                   VALUES (?, ?, ?, ?, ?, ?, ?)
        #               ")

        # GET
        # SELECT 		forumid, forumcreator, forumtitle, posttimestamp 
        # FROM 		discussion_forum.Content 
        # WHERE 		forumid=?;

        # forum_get_stmt = session.prepare("SELECT forumid, forumcreator, forumtitle, posttimestamp FROM discussion_forum.Content where forumid=? ORDER BY posttimestamp DESC")

        
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
        
        # query = 'SELECT Users.Username as creator, Forums.ForumId as id, Forums.ForumsName as name FROM Forums, Users where CreatorId = UserId;'
        # conn = sqlite3.connect(DATABASE)
        # conn.row_factory = dict_factory
        # cur = conn.cursor()
        # all_forums = cur.execute(query).fetchall()
        
        cluster = Cluster(['172.17.0.1 ','172.17.0.2'])

        session = cluster.connect("discussion_forum")

        rows = session.execute("SELECT * FROM Forums;")
        
        forums = {}
        all_forums = []
        for forum_row in rows:
            forums['id'] = forum_row.forumid
            forums['name'] = forum_row.forumtitle
            forums['creator'] = forum_row.forumcreator
            all_forums.append(forums.copy())
        
        return jsonify(all_forums)
    else:
        return get_response(405)

