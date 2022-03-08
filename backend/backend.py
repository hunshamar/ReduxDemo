
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app, supports_credentials=True)


connection = "sqlite:///db.db"
app.config['SQLALCHEMY_DATABASE_URI'] = connection
db = SQLAlchemy(app)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(2048))

    def as_dict(self):
        return {
            "id": self.id,
            "text": self.text
        }

    def __init__(self, text):
        self.text = text
   

def add_post(text):
    post = Posts(text)
    db.session.add(post)
    db.session.commit()
    return post.as_dict()

def get_posts():
    posts = Posts.query.all()
    return [p.as_dict() for p in posts]

    
def delete_post(id):
    post = Posts.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return post.as_dict()


@app.route("/api/posts", methods=["POST", "GET", "DELETE"])
def posts_route():
    try:   
        if (request.method == "POST"):
            text = request.json["text"]
            post = add_post(text)
            print(jsonify(post))
            return jsonify(post)
        
        if (request.method == "GET"):
            posts = get_posts()
            return jsonify(posts)

            
        if (request.method == "DELETE"):
            id = request.json["id"]
            post = delete_post(id)
            return jsonify(post)

    except Exception as e:
        return jsonify({"error": str(e)})



