from marshmallow import Schema,fields,ValidationError,validate
from bson import ObjectId
from flask_bcrypt import bcrypt
from flask_login import UserMixin
from market import db
from market import login_manager

users=db.users
class ObjectIdField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if not isinstance(value, ObjectId):
            raise ValueError("Invalid ObjectId")
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return ObjectId(value)
        except:
            raise ValueError("Invalid ObjectId")

class ItemSchema(Schema):
   name=fields.String(required=True)
   price=fields.Integer(required=True,validate=validate.Range(min=10))
   barcode=fields.String(required=True)
   owner = ObjectIdField(required=True) 
#    description=fields.String(required=True)

@login_manager.user_loader
def load_user(user_id):
    from bson import ObjectId
    user_data = users.find_one({"_id": ObjectId(user_id)})

    if user_data:
        # Return an instance of UserModel instead of a dict
        return UserModel(
            username=user_data.get('username'),
            email=user_data.get('email'),
            password_hash=user_data.get('password_hash'),
            budget=user_data.get('budget', 1000),
            items=user_data.get('items', [])
        )
    return None


class User(Schema):
   username=fields.String(required=True)
   email=fields.Email(required=True)
   password_hash=fields.String(required=True)
   budget=fields.Integer(missing=1000)
   items = fields.List(ObjectIdField(),missing=[])  

#    @property
#    def password(self):
#        return self.password
#    @password.setter
#    def password(self,plain_test_password):
#        self.password_hash=bcrypt.generate_password_hash(plain_test_password).decode('utf-8')
class UserModel(UserMixin):
    def __init__(self, username, email, password_hash, budget=1000, items=None,_id=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.budget = budget
        self.items = items if items is not None else []
        self._id = _id  # Store the MongoDB ObjectId
    
    def get_id(self):
        return str(self._id)
    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"




    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)     




def handle_validation_error(err):
   return {'error':err.messages},400