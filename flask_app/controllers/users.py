from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect("/")
        
    user_in = User.create_user(request.form)
    one_user= User.one_user(user_in)
    session['user_id'] = one_user.id
    print("___USER IN VAR___",user_in)
    print("___One USER IN VAR___", one_user)
    return redirect("/dashboard")


@app.route("/login", methods=['POST'])
def login():
    user_in_db = User.validate_login(request.form)

    if not user_in_db:
        return redirect("/")

    print("___THIS USER LOGIN___",user_in_db)   

    user = User.select_by_email(request.form)
    print("___THIS USER ID___", user.id)
    session['user_id'] = user.id

    return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():
    if not "user_id" in session:
        return redirect("/")
        
    user_id = {
        "id":session['user_id']
    }

    user = User.one_user(user_id) 
    return render_template("/dashboard.html", user=user)

    
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")