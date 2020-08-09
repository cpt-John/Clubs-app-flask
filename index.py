from flask import Flask, request, Response, render_template
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DBURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Clubs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'categories.id'), nullable=False)
    category = db.relationship('Categories', foreign_keys=[category_id])
    public = db.Column(db.Boolean, nullable=False)


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


def add_club(clubName, category=1, public=0):
    try:
        club = Clubs(
            name=clubName, category_id=category, public=public
        )
        db.session.add(club)
        db.session.commit()
        return 'added'
    except:
        return 'error in adding'


def update_club(club_id, clubName, category, public):
    try:
        club = Clubs.query.get(club_id)
        club.name = clubName
        club.category_id = category
        club.public = public
        db.session.commit()
        return 'updated'
    except:
        return 'error in updating'


def delete_club(club_id):
    try:
        club = Clubs.query.get(club_id)
        db.session.delete(club)
        db.session.commit()
        return 'deleted'
    except:
        return 'error in deleting'


def get_categories():
    array_categories = []
    try:
        categories = Categories.query.all()
        for category in categories:
            array_categories.append({'id': category.id, 'name': category.name})
    except:
        array_categories = []
    finally:
        return array_categories


def get_clubs():
    array_clubs = []
    try:
        clubs = Clubs.query\
            .join(Categories, Clubs.category_id == Categories.id).all()

        for club in clubs:
            array_clubs.append({'id': club.id, 'name': club.name,
                                'category': club.category.name, 'category_id': club.category.id, 'public': club.public, 'public_id': int(club.public)})
    except:
        array_clubs = []
    finally:
        return array_clubs


@app.route("/", methods=['GET'])
def clubs():
    return render_template('dash.html', clubs=get_clubs(), categories=get_categories())


@app.route("/addClub", methods=['POST'])
def addclub():
    if not request.json['clubName']:
        return Response({'message': 'bad request'}, status=400, mimetype='application/json')
    return add_club(request.json['clubName'], int(request.json['category']), int(request.json['public']))


@app.route("/updateClub", methods=['POST'])
def updateclub():
    if not request.json['club_id']:
        return Response({'message': 'bad request'}, status=400, mimetype='application/json')
    return update_club(int(request.json['club_id']), request.json['clubName'], int(request.json['category']), int(request.json['public']))


@app.route("/deleteClub", methods=['DELETE'])
def deleteclub():
    club_id = request.headers.get('club_id')
    if not club_id:
        return Response({'message': 'bad request'}, status=400, mimetype='application/json')
    return delete_club(int(club_id))


if __name__ == '__main__':
    app.run()
