from helper_funs import *

def thread(forum_id):
    #creating a new thread in a specified forum
    if request.method == 'POST':
        # auth contains the username and Password
        auth = request.authorization

        if auth_check(auth) is False:
            return get_response(401)

        if forum_id:
            checkifforumexists = query_db('SELECT 1 from Forums where ForumId = ?;', [forum_id])
            if checkifforumexists == []:
                return get_response(404)
            user = query_db('SELECT UserId from Users where Username = ?;', [auth.username])
            userid = dict(user[0]).get('UserId')
            requestJSON = request.get_json()
            conn = get_db()
            cur = conn.cursor()
            cur.execute('INSERT Into Threads (`ForumId`, `ThreadsTitle`) Values (?,?);', (int(forum_id), requestJSON.get('title')))
            thread = cur.execute('SELECT last_insert_rowid() as ThreadId;').fetchall()
            threadid = dict(thread[0]).get('ThreadId')
            timestamp = strftime('%a, %d %b %Y %H:%M:%S', gmtime()) + ' GMT'
            cur.execute('INSERT into Posts (`AuthorId`, `ThreadBelongsTo`, `PostsTimestamp`, `Message`) values (?,?,?,?);', (userid, threadid, timestamp, requestJSON.get('text')))
            conn.commit()
            conn.close()

            return get_response(201, body={}, location=('/forums/'+forum_id+'/'+str(threadid)))
        else:
            return get_response(404)

    elif request.method == 'GET':
        query = 'SELECT id, title, Users.Username as creator, timestamp from (select id, AuthorId, timestamp, title from (select Threads.ThreadId as id, AuthorId, timestamp, Threads.ThreadsTitle as title, Threads.ForumId as Fid from (select ThreadBelongsTo, AuthorId, PostsTimestamp as timestamp, Posts.PostId from Posts) join Threads on ThreadBelongsTo = Threads.ThreadId group by Threads.ThreadId having max(PostId) order by PostId desc) join Forums on Fid = Forums.ForumId where Forums.ForumId = ?) join Users where AuthorId = Users.UserId'
        to_filter = []
        #return all the threads from the forum
        if forum_id:
            conn = sqlite3.connect(DATABASE)
            conn.row_factory = dict_factory
            cur = conn.cursor()
            all_threads = cur.execute(query, [str(forum_id)]).fetchall()
            # If the the quey returns an empty result
            # e.g. http://127.0.0.1:5000/forums/100
            if all_threads == []:
                return get_response(404)
            else:
                return jsonify(all_threads)
        # What is an example of this case?
        if not forum_id:
            return get_response(404)
    else:
        return get_response(405)