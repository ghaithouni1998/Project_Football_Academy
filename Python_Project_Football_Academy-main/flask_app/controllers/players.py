from ast import Return
from flask_app import app
from datetime import datetime
from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.offer import Offer
from flask_app.models.player import Player
from flask_app.models.trainer import Trainer
bcrypt = Bcrypt(app)





# REGISTER - method - ACTION
@app.route("/players/register", methods=["POST"])
def player_register():
    user_one= Player.validate(request.form)
    if not user_one  :

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

    
    data = {**request.form,"password": pw_hashed}
    # save user in DB
    user_id = Player.create(data)
    player = Player.get_user_by_id({"id" : user_id})    
    session["page"] = player.page
    session["user_id"] = user_id

    return redirect(f"/players/{user_id}/dashboard")


# Login - method - ACTION
@app.route("/players/login", methods=["POST"])
def player_login():
    # data = {"type": request.form["type"], "email": request.form["email"]}
    user_in_db = Player.get_by_email({"email" : request.form["email"]})
    # if email not found
    if not user_in_db:
        flash("invalid credentials", "log")
        return redirect("/players/login")
    # now check the password
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("invalid credentials", "log")
        return redirect("/players/login")

    # * if all is good
    print(f"===> id = {user_in_db.id}")
    session["user_id"] = user_in_db.id
    player = Player.get_user_by_id({"id" : user_in_db.id})

    if not "page" in session:
        session["page"] = player.page
    return redirect(f"/players/{session["user_id"]}/dashboard")
    
    
    
    
    
    
    # Display Route - Dashboard
@app.route("/players/<int:id>/dashboard")
def player_dash(id):
    # ! Route Guard
    if "user_id" not in session:
        return redirect("/")
    data = {"id": id}
    if session["page"] > 4:
        session["page"] = 4
    player = Player.get_user_by_id(data)
    if session["page"]== 1:
        return redirect(f"/players/{id}/create_player1")
    if session["page"]== 2:
        return redirect(f"/players/{id}/create_player2")
    if session["page"]== 3:
        return redirect(f"/players/{id}/create_player3")
    if session["page"]== 4:
        return render_template("players_dashboard.html", loggedin_user=player,get_trainer=Trainer.get_user_by_id, offers = Offer.offers_one_player(data))

    



# ! ------- LOGOUT -------- action
@app.route("/players/logout")
def logout():
    session.clear()
    return redirect("/")



@app.route("/players/<int:id>/create_player1")
def stats(id):
    player = Player.get_user_by_id({"id":id})
    arr =player.test_skills_insert()
    Player.update_page({"id":id})
    return render_template("create_player.html", loggedin_user=player ,arr = arr, show = [0,"block","none","none"])

@app.route("/players/<int:id>/create_player2")
def stats2(id):
    player = Player.get_user_by_id({"id":id})
    arr =player.test_skills_insert() 
    Player.update_page({"id":id})
    return render_template("create_player.html", loggedin_user=player ,arr = arr, show = [0,"none","block","none"])

@app.route("/players/<int:id>/create_player3")
def stats3(id):
    player = Player.get_user_by_id({"id":id})
    arr =player.test_skills_insert() 
    Player.update_page({"id":id})
    return render_template("create_player.html", loggedin_user=player , arr = arr, show = [0,"none","none","block"])

@app.route('/players/<int:id>/add_stats', methods=['POST'])
def add_stats(id):
    date =  datetime.strptime((request.form)["birthdate"],"%Y-%m-%d").date()
    data = {**request.form, "age": Player.calculate_age(date), "id": id}
    Player.add_stats(data)
    player = Player.get_user_by_id({"id":id})
    return redirect(f"/players/{id}/create_player2")


# @app.route('/offers/<int:id>')
# def one(id):
#     if 'player_id' in session:
#         offer = Offer.get_by_id({'id' : id})
#         player = Player.get_player_by_id({'id':session['player_id']})
#         return render_template('/view_offer.html', offer=offer,player=player)
#     return redirect('/')
