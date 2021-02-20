from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class PortfolioItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=False)
    description = db.Column(db.String(1000), unique=False)
    url = db.Column(db.String(1000), unique=False)
    category = db.Column(db.String(1000), unique=False)
    position = db.Column(db.Integer, unique=False)

    def __init__(self, name, description, url, category, position):
        self.name = name
        self.description = description
        self.url = url
        self.category = category
        self.position = position

class PortfolioItemSchema(ma.Schema):
    class Meta:
        fields = ('name', 'description', 'url', 'category', 'position')

PortfolioItem_schema = PortfolioItemSchema()
PortfolioItems_schema = PortfolioItemSchema(many=True)

# Endpoint to create a new portfolio item
@app.route('/portfolioItem', methods=["POST"])
def add_portfolioItem():
    name = request.json['name']
    description = request.json['description']
    url = request.json['url']
    category = request.json['category']
    position = request.json['position']

    new_PortfolioItem = PortfolioItem(name, description, url, category, position)

    db.session.add(new_PortfolioItem)
    db.session.commit()

    portfolioItem = PortfolioItem.query.get(new_PortfolioItem.id)

    return PortfolioItem_schema.jsonify(portfolioItem)

#Endpoint to query all portfolio items
@app.route("/portfolioItems", methods=["GET"])
def get_portfolioItems():
    all_portfolioItems = PortfolioItem.query.all()
    result = PortfolioItems_schema.dump(all_portfolioItems)
    return jsonify(result)

# Endpoint for querying a single guide
@app.route("/portfolioItem/<id>", methods=["GET"])
def get_portfolioItem(id):
    portfolioItem = PortfolioItem.query.get(id)
    return PortfolioItem_schema.jsonify(portfolioItem)

# Endpoint for updating a guide
@app.route("/portfolioItem/<id>", methods=["PUT"])
def update_portfolioItems(id):
    portfolioItem = PortfolioItem.query.get(id)
    name = request.json['name']
    description = request.json['description']
    url = request.json['url']
    category = request.json['category']
    position = request.json['position']

    portfolioItem.name = name
    portfolioItem.description = description
    portfolioItem.url = url
    portfolioItem.category = category
    portfolioItem.position = position

    db.session.commit()
    return PortfolioItem_schema.jsonify(portfolioItem)

# Endpoint for deleting a record
@app.route("/portfolioItem/<id>", methods=["DELETE"])
def delete_portfolioItem(id):
    portfolioItem = PortfolioItem.query.get(id)
    db.session.delete(portfolioItem)
    db.session.commit()

    return "Portfolio record was successfully deleted"

if __name__ == '__main__':
    app.run(debug=True)