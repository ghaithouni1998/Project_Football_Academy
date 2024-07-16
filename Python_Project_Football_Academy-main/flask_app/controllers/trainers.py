from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.trainer import Trainer
from flask_app.models.offer import Offer

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/trainers/register", methods=["POST"])
def trainer_register():
    user_one = Trainer.validate(request.form)
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
    user_id = Trainer.create(data)
    data = {"id": user_id}
    loggedin_user = Trainer.get_user_by_id(data)

    session["user_id"] = user_id
    return redirect("/trainers/dashboard")


@app.route("/trainers/login", methods=["POST"])
def trainer_login():
    # data = {"type": request.form["type"], "email": request.form["email"]}
    user_in_db = Trainer.get_by_email({"email": request.form["email"]})
    # if email not found
    if not user_in_db:
        flash("invalid credentials", "log")
        return redirect("/trainers/login")
    # now check the password
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("invalid credentials", "log")
        return redirect("/trainers/login")

    # * if all is good
    print(f"===> id = {user_in_db.id}")
    session["user_id"] = user_in_db.id
    data = {"id": session["user_id"]}
    loggedin_user = Trainer.get_user_by_id(data)
    return redirect("/trainers/dashboard")


@app.route("/trainers/dashboard")
def trainer_dash():
    # ! Route Guard
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggedin_user = Trainer.get_user_by_id(data)
    return render_template(
        "trainers_dashboard.html",
        loggedin_user=loggedin_user,
        my_offers=Offer.get_offer_by_trainer({"trainer_id": session["user_id"]}),
    )


@app.route("/trainers/logout")
def trainer_logout():
    session.clear()
    return redirect("/")


@app.route("/trainers/new")
def trainer_form():
    if "user_id" not in session:
        return redirect("/")
    return render_template("trainers_dashboard.html")


# @app.route('/trainers/create', methods=['post'])
# def create_recipe():
#     if (Trainer.validate_trainer(request.form)):
#         data = {
#             **request.form, 'user_id':session['user_id']
#         }
#         Trainer.save_recipe(data)
#         return redirect('/trainers')
#     return redirect('/trainers')

# @app.route('/trainers/show/<int:trainer_id>')
# def show_trainer(trainer_id):
#     if 'user_id' not in session:#if he has not an id redirect to the register page
#         return redirect('/')
#     trainer=Trainer.get_user_by_id({'id':trainer_id})
#     user = User.get_by_id({'id':session['user_id']})
#     return render_template('show_offers.html',trainer=trainer,user=user)

# @app.route('/trainers/edit/<int:trainers_id>')
# def edit_trainer(trainer_id):
#     if 'user_id' not in session:
#         return redirect('/')
#     trainer= Trainer.get_by_id_trainer({'id': recipe_id})
#     session['recipe_id']= trainer_id
#     return render_template('edit_trainer.html',recipe=recipe)

# @app.route('/trainers/edit', methods=['post'])
# def edit():
#     trainer_data= {
#         **request.form,
#         'id': session['trainer_id']
#     }
#     Trainer.update_trainer(trainer_data)
#     return redirect('/trainers')

# @app.route('/trainers/delete/<int:trainer_id>')
# def delete(trainer_id):
#     Trainer.delete_trainer({'id':trainer_id})
#     return redirect('/trainers')
