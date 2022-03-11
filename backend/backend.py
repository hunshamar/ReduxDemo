
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)


connection = "sqlite:///db.db"
app.config['SQLALCHEMY_DATABASE_URI'] = connection
db = SQLAlchemy(app)

db.create_all()



    


class Handlekurv(db.Model):
    __tablename__ = "handlekurv"
    id = db.Column(db.Integer, primary_key=True)
    varer_i_handlekurv = db.relationship("Vare", backref="handlekurv")
    
    def as_dict(self):
        return [v.as_dict() for v in varer_i_handlekurv]    

class Vare(db.Model):
    __tablename__ = "vare"
    id = db.Column(db.Integer, primary_key=True)
    beskrivelse = db.Column(db.String(2048))
    pris = db.Column(db.Integer)

    def as_dict(self):
        return {
            "id": self.id,
            "text": self.text
        }

    def __init__(self, beskrivelse, pris):
        self.text = text
        self.pris = pris
   

def legg_til_vare(beskrivelse, pris):
    ny_vare = Vare(beskrivelse, pris)
    db.session.add(ny_vare)
    db.session.commit()
    return ny_vare.as_dict()

def hent_alle_varer():
    alle_varer = Vare.query.all()
    return [v.as_dict() for p in alle_varer]

    
def slett_vare(id):
    vare_som_skal_slettes = Vare.query.get(id)
    db.session.delete(vare_som_skal_slettes)
    db.session.commit()




@app.route("/api/varer", methods=["POST", "GET", "DELETE"])
def varer():
    try:   
        if (request.method == "POST"):
            beskrivelse = request.json["text"]
            pris = request.json["beskrivelse"]
            lagt_til_vare = legg_til_vare(text)
            return jsonify(lagt_til_vare)
        
        if (request.method == "GET"):
            alle_varer = hent_alle_varer()
            return jsonify(alle_varer)
            
        if (request.method == "DELETE"):
            id = request.json["id"]
            slett_vare(id)
            return id

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/api/handlekurv/varer", methods=["POST", "GET", "DELETE"])
def handlekurv():
    try:   
        if (request.method == "POST"):
            beskrivelse = request.json["text"]
            pris = request.json["beskrivelse"]
            lagt_til_vare = legg_til_vare(text)
            return jsonify(lagt_til_vare)
        
        if (request.method == "GET"):
            handlekurv = Handlekurv()
            db.session.add(handlekurv)
            db.session.commit()
            return jsonify(handlekurv.as_dict())
            
        if (request.method == "DELETE"):
            id = request.json["id"]
            slett_vare(id)
            return id

    except Exception as e:
        return jsonify({"error": str(e)})



# # lag en halvekurv hvis ingen eksisterer
# handlekurv = Handlekurv.query.all().first()
# if (not handlekurv):
#     handlekurs = Handlekurv()
#     db.session.add(handlekurv)
#     db.session.commit()

# handlekurv2 = Handlekurv.query.all().first()

# print(handlekurv2)

# print("init asdsds")