"""Flask app for Cupcakes"""

from flask import Flask, render_template, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

def serialize_cupcake(cupcake):
    """Serialize a cupcake SQLAlchemy obj to dictionary."""
    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image,
    }


@app.route('/')
def index_page():
    """Renders html template that includes JS"""
    return render_template("index.html")

# *****************************
# RESTFUL CUPCAKE JSON API
# *****************************    

@app.route("/api/cupcakes")
def list_cupcakes():
    """Return JSON {'cupcakes': [{id, flavor, size}, ...]}"""
    cupcakes = Cupcake.query.all()

    serialized = [serialize_cupcake(cupcake) for cupcake in cupcakes]
    return jsonify(cupcakes=serialized)
    # end list_cupcakes

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Return JSON {'cupcake': {id, flavor, size}, ...}"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    serialized = serialize_cupcake(cupcake)
    return jsonify(cupcake=serialized)
    # end get_cupcake

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Create cupcake from form data & return it.

    Returns JSON {'cupcake': {id, name, calories}}
    """

    req = request.json
    new_cupcake = Cupcake(
        flavor=req["flavor"], 
        size=req["size"], 
        rating=req["rating"], 
        image=req["image"] or None)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)

    # Return w/status code 201 --- return tuple (json, status)
    return ( jsonify(cupcake=serialized), 201 )
    # end create_cupcake

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update cupcake from form data & return it.

    Returns JSON {'cupcake': {id, name, calories}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    req = request.json

    cupcake.flavor = req.get("flavor", cupcake.flavor)
    cupcake.size = req.get("size", cupcake.size)
    cupcake.rating = req.get("rating", cupcake.rating)
    cupcake.image = req.get("image", cupcake.image)

    db.session.commit()

    serialized = serialize_cupcake(cupcake)
    return jsonify(cupcake=serialized)
    # end update_cupcake

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete cupcake by cupcake_id & return json response.

    Returns JSON {message: "Deleted"}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message='Deleted') 
    # end delete_cupcake
