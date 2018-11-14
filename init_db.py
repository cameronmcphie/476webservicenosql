from flask import Flask
from helper_funs import get_db

app = Flask(__name__)
app.config["DEBUG"] = True

@app.cli.command('init_db')
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('init.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    print ('Database Initilaized')

if __name__ == "__main__":
    app.run()