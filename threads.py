from helper_funs import *
from cassandra.cluster import Cluster
from uuid import uuid4, UUID

def thread(forum_id):
    #creating a new thread in a specified forum
    if request.method == 'POST':
        # auth contains the username and Password
        auth = request.authorization

        if auth_check(auth) is False:
            return get_response(401)

        if forum_id:
            # checkifforumexists = query_db('SELECT 1 from Forums where ForumId = ?;', [forum_id])
            # if checkifforumexists == []:
            #     return get_response(404)
            # user = query_db('SELECT UserId from Users where Username = ?;', [auth.username])
            # userid = dict(user[0]).get('UserId')
            # requestJSON = request.get_json()
            # conn = get_db()
            # cur = conn.cursor()
            # cur.execute('INSERT Into Threads (`ForumId`, `ThreadsTitle`) Values (?,?);', (int(forum_id), requestJSON.get('title')))
            # thread = cur.execute('SELECT last_insert_rowid() as ThreadId;').fetchall()
            # threadid = dict(thread[0]).get('ThreadId')
            # timestamp = strftime('%a, %d %b %Y %H:%M:%S', gmtime()) + ' GMT'
            # cur.execute('INSERT into Posts (`AuthorId`, `ThreadBelongsTo`, `PostsTimestamp`, `Message`) values (?,?,?,?);', (userid, threadid, timestamp, requestJSON.get('text')))
            # conn.commit()
            # conn.close()

            cluster = Cluster(['172.17.0.1 ','172.17.0.2'])
            session = cluster.connect("discussion_forum")

            author = auth['username']

            # author = author.replace('"', "'")

            data = request.get_json()
            thread_title = data.get("title")
            post_text = data.get("text")
            # post_text = post_text.replace('"', "'")

            # for m in threadtitles:
            #     thread_title = m[0]
            #
            # print(thread_title)
            # thread_title = threadtitles[0]
            # print(theadtitles['threadtitle'])

            # thread_title = thread_title.replace('"', "'")

            post_id = uuid4()
            session.execute("INSERT INTO Content (postid, forumid, postauthor, posttext, posttimestamp, threadid, threadtitle, mostrecenttimestamp) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (post_id, UUID(forum_id), author, post_text, datetime.utcnow(), uuid4(), thread_title, datetime.utcnow()))
            
            
            thread_ids = session.execute("SELECT threadid from Content where postid=%s", [post_id])

            for tID in thread_ids:
                threadid = tID[0]

            return get_response(201, body={}, location=('/forums/'+forum_id+'/'+str(threadid)))
        else:
            return get_response(404)

    elif request.method == 'GET':
        if forum_id:
            cluster = Cluster(['172.17.0.1 ','172.17.0.2'])

            session = cluster.connect("discussion_forum")

            #TODO: Fix to only show threads and posts as well. May need to adjust scheme
            rows = session.execute("SELECT * FROM Content where forumid = %s;", [UUID(forum_id)])

            threads = {}
            all_threads = []
            for thread_row in rows:
                if (thread_row.threadtitle != None):
                    threads['id'] = thread_row.threadid
                    threads['title'] = thread_row.threadtitle
                    threads['creator'] = thread_row.postauthor
                    threads['timestamp'] = thread_row.mostrecenttimestamp
                    all_threads.append(threads.copy())

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
