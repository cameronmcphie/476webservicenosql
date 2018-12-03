from flask import Flask
from helper_funs import get_db

from cassandra.cluster import Cluster

app = Flask(__name__)
app.config["DEBUG"] = True




@app.cli.command('init_db')
def init_db():
    with app.app_context():


        cluster = Cluster(['172.17.0.1 ','172.17.0.2'])

        session = cluster.connect() #keyspace optional

        # db = get_db()

        # with app.open_resource('init.sql', mode='r') as f:
        #     #db.cursor().executescript(f.read())
        #
        # #db.commit()

        with app.open_resource('test.cql', mode='r') as f: #untested
            session.execute(f.read())





    print ('Database Initilaized')

if __name__ == "__main__":
    app.run()
