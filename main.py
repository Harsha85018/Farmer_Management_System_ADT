from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
from sqlalchemy import text


# MY db connection
local_server= True
app = Flask(__name__)
app.secret_key='harsha'

# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databas_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/farmers'
db=SQLAlchemy(app)

# here we will create db models that is tables
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))

class Farming(db.Model):
    fid=db.Column(db.Integer,primary_key=True)
    farmingtype=db.Column(db.String(100))


class Addagroproducts(db.Model):
    username=db.Column(db.String(50))
    email=db.Column(db.String(50))
    pid=db.Column(db.Integer,primary_key=True)
    productname=db.Column(db.String(100))
    productdesc=db.Column(db.String(300))
    price=db.Column(db.Integer)



class Trig(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    fid=db.Column(db.String(100))
    action=db.Column(db.String(100))
    timestamp=db.Column(db.String(100))


class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))

class Register(db.Model):
    rid=db.Column(db.Integer,primary_key=True)
    farmername=db.Column(db.String(50))
    adharnumber=db.Column(db.String(50))
    age=db.Column(db.Integer)
    gender=db.Column(db.String(50))
    phonenumber=db.Column(db.String(50))
    address=db.Column(db.String(50))
    farming=db.Column(db.String(50))

    
@app.route('/testpage')
def testpage():
    print("🧪 Test Page Rendered")
    return render_template('test.html')


@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/farmerdetails')
@login_required
def farmerdetails():
    with db.engine.connect() as connection:
        # Execute the query using the connection
        result = connection.execute(text("SELECT * FROM register"))
        
        # Fetch all the rows from the query result
        query = result.fetchall()
     
    return render_template('farmerdetails.html',query=query)

@app.route('/agroproducts')
@login_required
def agroproducts():
    with db.engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM addagroproducts"))
        query = result.fetchall()
        print("✅ Agroproducts route hit!")  # Debug output
    return render_template('agroproducts.html', query=query)


@app.route('/addagroproduct',methods=['POST','GET'])
@login_required
def addagroproduct():
    if request.method=="POST":
        username=request.form.get('username')
        email=request.form.get('email')
        productname=request.form.get('productname')
        productdesc=request.form.get('productdesc')
        price=request.form.get('price')
        products=Addagroproducts(username=username,email=email,productname=productname,productdesc=productdesc,price=price)
        db.session.add(products)
        db.session.commit()
        flash("Product Added","info")
        return redirect('/agroproducts')
   
    return render_template('addagroproducts.html')

@app.route('/triggers')
@login_required
def triggers():
    with db.engine.connect() as connection:
        # Execute the query using the connection
        result = connection.execute(text("SELECT * FROM trig"))
        
        # Fetch all the rows from the query result
        query = result.fetchall() 
    return render_template('triggers.html',query=query)

@app.route('/addfarming',methods=['POST','GET'])
@login_required
def addfarming():
    if request.method=="POST":
        farmingtype=request.form.get('farming')
        query=Farming.query.filter_by(farmingtype=farmingtype).first()
        if query:
            flash("Farming Type Already Exist","warning")
            return redirect('/addfarming')
        dep=Farming(farmingtype=farmingtype)
        db.session.add(dep)
        db.session.commit()
        flash("Farming Added","success")
    return render_template('farming.html')




@app.route("/delete/<string:rid>",methods=['POST','GET'])
@login_required
def delete(rid):
    with db.engine.connect() as connection:
    # Safely execute the DELETE query using the connection and `text()`
        connection.execute(text(f"DELETE FROM register WHERE register.rid={rid}"))
    flash("Slot Deleted Successful","danger")
    return redirect('/farmerdetails')


@app.route("/edit/<string:rid>",methods=['POST','GET'])
@login_required
def edit(rid):
    with db.engine.connect() as connection:
    # Execute the query using the connection
        result = connection.execute(text("SELECT * FROM farming"))
    
    # Fetch all the rows from the query result
        farming = result.fetchall()
    posts=Register.query.filter_by(rid=rid).first()
    if request.method=="POST":
        farmername=request.form.get('farmername')
        adharnumber=request.form.get('adharnumber')
        age=request.form.get('age')
        gender=request.form.get('gender')
        phonenumber=request.form.get('phonenumber')
        address=request.form.get('address')
        farmingtype=request.form.get('farmingtype')     
        query=db.engine.execute(f"UPDATE register SET farmername='{farmername}',adharnumber='{adharnumber}',age='{age}',gender='{gender}',phonenumber='{phonenumber}',address='{address}',farming='{farmingtype}'")
        flash("Slot is Updates","success")
        return redirect('/farmerdetails')
    
    return render_template('edit.html',posts=posts,farming=farming)


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        print(username,email,password)
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)

        with db.engine.connect() as connection:
    # Use a parameterized query to safely insert data
            connection.execute(
                text("INSERT INTO user (username, email, password) VALUES (:username, :email, :password)"),
                {"username": username, "email": email, "password": encpassword}
            )

        # this is method 2 to save data in db
        newuser=User(username=username,email=email,password=encpassword)
        db.session.add(newuser)
        db.session.commit()
        flash("Signup Success Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')    

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))



@app.route('/register', methods=['POST', 'GET'])
@login_required
def register():
    with db.engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM farming"))
        farming = result.fetchall()

    if request.method == "POST":
        farmername = request.form.get('farmername')
        adharnumber = request.form.get('adharnumber')
        age = request.form.get('age')
        gender = request.form.get('gender')
        phonenumber = request.form.get('phonenumber')
        address = request.form.get('address')
        farmingtype = request.form.get('farmingtype')

        db.session.execute(text("""
            INSERT INTO register (farmername, adharnumber, age, gender, phonenumber, address, farming)
            VALUES (:farmername, :adharnumber, :age, :gender, :phonenumber, :address, :farmingtype)
        """), {
            "farmername": farmername,
            "adharnumber": adharnumber,
            "age": age,
            "gender": gender,
            "phonenumber": phonenumber,
            "address": address,
            "farmingtype": farmingtype
        })
        db.session.commit()

        flash("Your Record Has Been Saved", "success")
        return redirect('/farmerdetails')

    return render_template('farmer.html', farming=farming)

@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'


app.run(debug=True)
