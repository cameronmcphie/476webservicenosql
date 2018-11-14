from helper_funs import *

def post(forum_id, thread_id):
    if request.method == 'POST':
        auth = request.authorization
        if auth_check(auth) is False:
            return get_response(401)

        if forum_id and thread_id:
            checkifforumexists = query_db('SELECT 1 from Forums where ForumId = ?;', [forum_id])
            checkifthreadexists = query_db('SELECT 1 from Threads where ThreadId = ?;', [thread_id])
            if (checkifforumexists == []) or (checkifthreadexists == []):
                return get_response(404)

            user = query_db('SELECT UserId from Users where Username = ?;', [auth.username])
            userid = dict(user[0]).get('UserId')
            requestJSON = request.get_json()
            timestamp = strftime('%a, %d %b %Y %H:%M:%S', gmtime()) + ' GMT'
            conn = get_db()
            cur = conn.cursor()
            cur.execute('INSERT into Posts (`AuthorId`, `ThreadBelongsTo`, `PostsTimestamp`, `Message`) values (?,?,?,?);', (userid, thread_id, timestamp, requestJSON.get('text')))
            conn.commit()
            conn.close()

            return get_response(201)
        else:
            return get_response(404)


    elif request.method == 'GET':
        # check if the forum exists
        checkifforumexists = query_db('SELECT 1 from Forums where ForumId = ?;', [forum_id])
        if checkifforumexists == []:
            return get_response(404)
        # Get all posts from specified thread
        query = 'SELECT Username as author, Message as text, PostsTimestamp as timestamp from Posts join Users on AuthorId = UserId and ThreadBelongsTo = ?;'
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        # all_threads = cur.execute(query).fetchall()
        allPosts = cur.execute(query, [thread_id]).fetchall()
        conn.close()
        if allPosts == []:
            return get_response(404)
        else:
            return get_response(200, body=allPosts)

    else:
        return get_response(405)
