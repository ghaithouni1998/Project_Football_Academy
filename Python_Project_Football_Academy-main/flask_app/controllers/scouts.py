from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.scout import Scout
from flask_app.models.offer import Offer
from flask_app.models.trainer import Trainer
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/index")
def index():
    return render_template("index.html", d_login="d-none", d_reg="")


@app.route("/login")
def login():
    return render_template("index.html", d_login="", d_reg="d-none")


@app.route("/scouts/register", methods=["POST"])
def scout_register():
    user_one = Scout.validate(request.form)
    if not user_one:
        return redirect("/")
    # 1 . hash the password
    pw_hashed = bcrypt.generate_password_hash(request.form["password"])
    # 2 . get the data dict ready with the new hashe pw to create a User
    # data = {
    #     "first_name": request.form["first_name"],
    #     "last_name": request.form["last_name"],
    #     "email": request.form["email"],
    #     "confirm": request.form["confirm_password"],
    #     "password": pw_hashed,
    # }

    data = {**request.form, "password": pw_hashed}
    # save user in DB
    user_id = Scout.create(data)

    session["user_id"] = user_id
    data = {"id": user_id}
    loggedin_user = Scout.get_user_by_id(data)
    return redirect("/scouts/dashboard")


@app.route("/scouts/login", methods=["POST"])
def scout_login():
    # data = {"type": request.form["type"], "email": request.form["email"]}
    user_in_db = Scout.get_by_email({"email": request.form["email"]})
    # if email not found
    if not user_in_db:
        flash("invalid credentials", "log")
        return redirect("/scouts/login")
    # now check the password
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("invalid credentials", "log")
        return redirect("/scouts/login")

    # * if all is good
    print(f"===> id = {user_in_db.id}")
    session["user_id"] = user_in_db.id
    data = {"id": session["user_id"]}
    loggedin_user = Scout.get_user_by_id(data)
    return redirect("/scouts/dashboard")


@app.route("/scouts/dashboard")
def scout_dash():
    # ! Route Guard
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggedin_user = Scout.get_user_by_id(data)
    return render_template(
        "scouts_dashboard.html",
        my_offers=Offer.get_offer_by_scout({"scout_id": session["user_id"]}),
        loggedin_user=loggedin_user,
        get_trainer=Trainer.get_user_by_id,
    )


@app.route("/scouts/logout")
def scout_logout():
    session.clear()
    return redirect("/")


@app.route("/scouts/new")
def scout_form():
    if "user_id" not in session:
        return redirect("/")
    return render_template("scouts_dashboard.html")


# @app.route('/scouts/create', methods=['post'])
# def create_recipe():
#     if (scout.validate_scout(request.form)):
#         data = {
#             **request.form, 'user_id':session['user_id']
#         }
#         scout.save_recipe(data)
#         return redirect('/scouts')
#     return redirect('/scouts')

# @app.route('/scouts/show/<int:scout_id>')
# def show_scout(scout_id):
#     if 'user_id' not in session:#if he has not an id redirect to the register page
#         return redirect('/')
#     scout=Scout.get_user_by_id({'id':scout_id})
#     user = User.get_by_id({'id':session['user_id']})
#     return render_template('show_offers.html',scout=scout,user=user)

# @app.route('/scouts/edit/<int:scouts_id>')
# def edit_scout(scout_id):
#     if 'user_id' not in session:
#         return redirect('/')
#     scout= scout.get_by_id_scout({'id': recipe_id})
#     session['recipe_id']= scout_id
#     return render_template('edit_scout.html',recipe=recipe)

# @app.route('/scouts/edit', methods=['post'])
# def edit():
#     scout_data= {
#         **request.form,
#         'id': session['scout_id']
#     }
#     scout.update_scout(scout_data)
#     return redirect('/scouts')

# @app.route('/scouts/delete/<int:scout_id>')
# def delete(scout_id):
#     scout.delete_scout({'id':scout_id})
#     return redirect('/scouts')
