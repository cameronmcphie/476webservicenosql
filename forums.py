from helper_funs import *
from cassandra.cluster import Cluster
from uuid import uuid4


def forum():
    #creating a new discussion forum
    if request.method == 'POST':
        # auth contains the username and Password
        auth = request.authorization

        if auth_check(auth) is False:
            return get_response(401)

        # Get and parse the forum name from the POST
        forum_submit = request.get_json()
        forum_name = forum_submit.get('name')

        cluster = Cluster(['172.17.0.1 ','172.17.0.2'])

        session = cluster.connect("discussion_forum")

        check_forum_title = session.execute("SELECT forumtitle FROM Forums where forumtitle = %s;", [forum_name])
        # Check if forum already exists
        forums = {}
        for forum_row in check_forum_title:
            forums['id'] = forum_row.forumtitle
        if(not bool(forums)):
            new_forum_id = uuid4()
            creator = auth['username']

            session.execute("INSERT INTO Forums (forumid, forumcreator, forumtitle) VALUES (%s, %s, %s);", [new_forum_id, creator, forum_name])

            return get_response(201, body=None, location=('/forums/'+str(new_forum_id)))
        else:
            return get_response(409)

    #request for all the present forums
    elif request.method == 'GET':        
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

