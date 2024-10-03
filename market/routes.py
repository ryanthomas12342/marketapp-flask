from market import app
from flask import Flask,render_template,redirect,url_for,request,jsonify,flash,get_flashed_messages
from .schemas import ItemSchema,handle_validation_error,User,UserModel
from marshmallow import ValidationError
from market import db
from werkzeug.security import generate_password_hash,check_password_hash

from .forms import RegisterForm,LoginForm,PurchaseForm

from flask_login import login_user,logout_user,login_required,current_user



market_collection=db.market
users=db.users
items = [
    { 
        'id': 1,
        'name': 'Phone', 
        'barcode': '893212299897', 
        'price': 500,
        'description': 'A smartphone with a 6.5-inch display, 128GB storage, and 4GB RAM.'
    },
    { 
        'id': 2,
        'name': 'Laptop', 
        'barcode': '123985473165', 
        'price': 900,
        'description': 'A high-performance laptop with a 15.6-inch screen, 512GB SSD, and 16GB RAM.'
    },
    { 
        'id': 3,
        'name': 'Keyboard', 
        'barcode': '231985128446',
        'price': 40,
        'description': 'A mechanical keyboard with RGB backlighting and customizable keys.'
    }]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")



@app.route("/look")
def market_page():

    # data=request.json

    item_schema=ItemSchema()
    items = [
    { 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
    { 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
    {'name': 'Keyboard', 'barcode': '231985128446','price':4}
    ]

    try:
        validated_data=item_schema.load(items,many=True)
    except ValidationError as err:
        return handle_validation_error(err)
    result=market_collection.insert_many(items).inserted_ids

    return jsonify({"message":"Author created ","ids":str(result)}),201


    # return render_template("market.html",items=items)


@app.route("/market",methods=['GET','POST'])
@login_required
def view():

    purchase=PurchaseForm()
    
    global items
    if request.method=='POST':
        p_item=request.form.get('purchased_item')

    return render_template("market.html",items=items,purchase=purchase)
    


@app.route("/register",methods=['GET','POST'])
def register():
    form=RegisterForm()

    userSchema=User()

    if form.validate_on_submit():
        existing_user = users.find_one({"username": form.username.data})
        if existing_user:
            flash(f'Username "{form.username.data}" is already taken. Please choose another one.', category='danger')
            return redirect(url_for('register'))  # Reload the form with the flash message
        
        try:
            validated=userSchema.load({
                "username":form.username.data,
             "email":form.email.data,
             "password_hash":generate_password_hash(form.pass1.data)  
            })
        except ValidationError as err:
            return handle_validation_error(err)
        print(validated)
        inserted=users.insert_one(
            validated
        ).inserted_id
        print(inserted)
        user = UserModel(
                     username=form.username.data,
            email=form.email.data,
            password_hash=validated.get('password_hash'),
            budget=validated.get('budget', 1000),
            items=validated.get('items', []),
            _id=inserted  # Pass the ObjectId
                    
                    )

        login_user(user)
        flash("User Sucessfully signedup in ",category='success')
        return redirect(url_for('view'))
    if form.errors!={}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user:{err_msg},',category='danger')


    return render_template('register.html',form=form)



@app.route("/login",methods=['GET','POST'])
def login_page():

    form=LoginForm()

    if form.validate_on_submit():

        user_data=users.find_one({"username":form.username.data})

        if not user_data:
            flash("This user has not been registered .Enter a valid register or signup ",category='danger')
        else:
          if(check_password_hash(user_data['password_hash'],form.password.data)):
            user = UserModel(
                     username=user_data.get('username'),
            email=user_data.get('email'),
            password_hash=user_data.get('password_hash'),
            budget=user_data.get('budget', 1000),
            items=user_data.get('items', []),
            _id=user_data.get('_id')  # Pass the ObjectId
                    
                    )
            
            login_user(user)
            flash(f"User Sucessfully logged in {user_data.get('username')} ",category='success')
            return redirect(url_for('view'))
          else:
              flash("Please provide a correct password or username",category='danger')


    
    return render_template('login.html',form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash(f"You have been logged out ",category='info')

    return redirect(url_for("login_page"))


@app.route("/purchase/<id>",methods=["POST"])
def purchase(id):
    global items

    print("this is current user")
    print(current_user._id)
    for item in items:

        print("hello") 
        print(type(item['id']))
        if str(item['id'])==id:
            print("yes")
            if current_user.budget>item['price']:
                current_user.items.append(item)
                current_user.budget-=(item['price'])
            
                items.remove(item)
                print(current_user._id)
                users.update_one(
                    {"_id": current_user._id},
                    {
                        "$set": {
                            "budget": current_user.budget,
                            "items": current_user.items
                        }
                    }
                )
                flash(f"Sucessfully bought {item['name']} for ${item['price']}")
                break
            else:
                flash("Insufficient budget to make this purchase", category="danger")
                break
                
    return redirect(url_for('view'))
                


    