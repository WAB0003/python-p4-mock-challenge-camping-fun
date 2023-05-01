#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Activity, Signup, Camper

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''
#!CAMPERS
@app.route('/campers', methods = ['GET','POST'])
def campers():
    all_campers = Camper.query.all()
    
    if request.method == 'GET':
        camper_list = []
        for camper in all_campers:
            camper_dict = {
                "id":camper.id,
                "name":camper.name,
                "age":camper.age
            }
            camper_list.append(camper_dict)
        response = make_response(camper_list, 200)              #!check in jsonify is needed
        return response
    
    elif request.method == 'POST':
        data = request.get_json()
        try:
            new_camper = Camper(
                name=data.get('name'),
                age=data.get('age')
            )
            db.session.add(new_camper)
            db.session.commit()
            return new_camper.to_dict()
        except ValueError:
            return {'error': '400: Camper not found'}, 400
        

#!CAMPERS WITH ID
@app.route('/campers/<int:id>',methods=['GET'])
def campers_by_id(id):
    camper = Camper.query.filter(Camper.id == id).first()
    
    if request.method == 'GET':
        if camper:
            # camper_dict = camper.to_dict(rules=('-signups',))
            camper_dict = camper.to_dict()
            
        
            response=make_response(camper_dict, 200)
            return response
        else:
            return {'error': '404: Camper not found'}, 404
        
        
#!ACTIVITIES
@app.route('/activities', methods = ['GET'])
def activities():
    all_activities = Activity.query.all()
    
    if request.method == 'GET':
        activities_list = []
        for activity in all_activities:
            activity_dict = {
                "id":activity.id,
                "name":activity.name,
                "difficulty":activity.difficulty
            }
            activities_list.append(activity_dict)
        response = make_response(activities_list, 200)              #!check in jsonify is needed
        return response
    
#!ACTIVITY WITH ID
@app.route('/activities/<int:id>',methods=['DELETE'])
def activity_by_id(id):
    activity = Activity.query.filter(Activity.id == id).first()
    
    if request.method == 'DELETE':
        if activity:
            db.session.delete(activity)
            db.session.commit()
            response = make_response("",204)
            return response

        else:
            return {'error': '404: Activity not found'}, 404
    
#!SIGNUPS
@app.route('/signups', methods = ['POST'])
def signups():
  
    if request.method == 'POST':
        data = request.get_json()
        try:
            new_signup = Signup(
                camper_id=data.get('camper_id'),
                activity_id=data.get('activity_id'),
                time=data.get('time'),
            )
            db.session.add(new_signup)
            db.session.commit()
            return new_signup.to_dict()
        except ValueError:
            return {'error': '400: Camper not found'}, 400     

if __name__ == '__main__':
    app.run(port=5555, debug=True)
