from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    #Relationships
    signups = db.relationship('Signup', back_populates='activities')
    #*Through Relationships
    campers = association_proxy('signups', "campers")                       #through relationship references backpopulate first and then whatever is needed
    
    #Serialization rules
    serialize_rules = ('-signups.activities', '-campers.activities','-created_at','-updated_at',)
    
    

class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    camper_id = db.Column(db.Integer, db.ForeignKey("campers.id"))          #foreign key points to table of desired relationship
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id"))     #foreign key points to table of desired relationship
    time = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    #Relationships
    activities = db.relationship('Activity', back_populates='signups')      
    campers = db.relationship('Camper', back_populates='signups')
    
    #Serialization rules
    serialize_rules = ('-activities.signups', '-campers.signups','-created_at','-updated_at',)
    
    #!Validations
    @validates('time')
    def validate_age(self, key, time):
        if not 0 <= int(time) <= 23:
            raise ValueError("Time must be between 0 & 23")
        return time
    

class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    #Relationships
    signups = db.relationship('Signup', back_populates='campers')
    #*Through Relationships
    activities = association_proxy('signups', "activities")
    
    #Serialization rules
    serialize_rules = ('-signups.campers', '-activities.campers','-created_at','-updated_at',)
    
    #!Validations
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Must have name entry")
        return name
    @validates('age')
    def validate_age(self, key, age):
        if not 8 <= int(age) <= 18:
            raise ValueError("age must be between 8 & 18")
        return age
            
        
    
    

# add any models you may need. 