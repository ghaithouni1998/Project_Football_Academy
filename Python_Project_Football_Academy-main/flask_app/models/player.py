from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash, session
from datetime import date
from random import randint
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class Player:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.age = data["age"]
        self.weight = data["weight"]
        self.height = data["height"]
        self.position = data["position"]
        self.foot = data["foot"]
        self.stamina = data["stamina"]
        self.kicking = data["kicking"]
        self.speed = data["speed"]
        self.physique = data["physique"]
        self.technique = data["technique"]
        self.reflex = data["reflex"]
        self.energy = data["energy"]
        self.injury = data["injury"]
        self.trainer_id = data["trainer_id"]
        self.page = data["page"]
        # self.poster = user.User.get_by_id({"id": self.user_id})

    @classmethod
    def create(cls, data):
        query = f"""
                INSERT INTO  players (first_name, last_name, email, password, page)
                VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s, 1);
                """

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def update_page(cls, data):
        query = f"""
                UPDATE players SET page = page + 1
                WHERE players.id = %(id)s;
                """

        connectToMySQL(DATABASE).query_db(query, data)
        player = cls.get_user_by_id(data)
        session["page"] = player.page
        return player.page

    @classmethod
    def get_user_by_id(cls, data):
        query = f"""
                    SELECT * FROM players 
                    WHERE  id = %(id)s;
                    
                """
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) < 1:  # type: ignore
            return []
        return cls(result[0])

    @classmethod
    def get_by_email(cls, data):
        query = f"""
                    SELECT * FROM players 
                    WHERE  email = %(email)s;
                    
                """

        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) < 1:
            return []

        return cls(result[0])  # type: ignore

    @classmethod
    def add_stats(cls, data):
        query = f"""
                UPDATE players SET age=%(age)s, weight=%(weight)s, height=%(height)s, foot=%(foot)s, position=%(position)s
                WHERE players.id = %(id)s;
                """

        return connectToMySQL(DATABASE).query_db(query, data)

    def test_skills_insert(self):
        arr = Player.skills_calc(self.position)
        query = f"""
                UPDATE players SET stamina={arr[0]}, kicking={arr[1]}, speed={arr[2]}, physique={arr[3]}, technique={arr[4]}, reflex={arr[5]}
                WHERE players.id ={self.id};
                """

        connectToMySQL(DATABASE).query_db(query)
        return arr

    @classmethod
    def get_all_players(cls):
        query = "SELECT * FROM players;"
        results = connectToMySQL(DATABASE).query_db(query)
        all_players = []
        for row in results:  # type: ignore
            all_players.append(cls(row))
        return all_players

    @staticmethod
    def calculate_age(birthdate):
        today = date.today()
        return (
            today.year
            - birthdate.year
            - ((today.month, today.day) < (birthdate.month, birthdate.day))
        )

    @classmethod
    def offer_accept(cls, data):
        query = f"""
                    UPDATE players SET trainer_id = %(trainer_id)s
                    WHERE players.id = %(id)s;
                    
                """

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def player_enroll(cls, data):
        query = f"""
                    INSERT INTO player_offers_selection (offer_id , player_id)
                    VALUES (%(offer_id)s , %(player_id)s);
                    
                """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def offer_liberate(cls, data):
        # query = f"""
        #             DELETE FROM player_offers_selection
        #             WHERE offer_id = %(offer_id)s and player_id = %(player_id)s;
        #         """
        query = """
                    DELETE player_offers_selection
                    FROM player_offers_selection
                    JOIN offers ON player_offers_selection.offer_id = offers.id
                    WHERE offers.id = %(offer_id)s AND player_offers_selection.player_id = %(player_id)s;
                    """
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def skills_calc(position):
        if position == "Forward":
            arr = [
                randint(40, 60),
                randint(70, 90),
                randint(70, 90),
                randint(50, 70),
                randint(70, 90),
                randint(10, 30),
            ]
        elif position == "Center":
            arr = [
                randint(70, 90),
                randint(60, 80),
                randint(50, 70),
                randint(60, 80),
                randint(60, 80),
                randint(10, 30),
            ]
        elif position == "Defense":
            arr = [
                randint(70, 90),
                randint(50, 70),
                randint(40, 60),
                randint(60, 80),
                randint(40, 60),
                randint(10, 30),
            ]
        elif position == "Goalkeeper":
            arr = [
                randint(40, 60),
                randint(50, 70),
                randint(30, 50),
                randint(50, 70),
                randint(30, 50),
                randint(70, 90),
            ]
        else:
            arr = [0, 0, 0, 0, 0, 0]

        return arr

    @staticmethod
    def validate(data):
        is_valid = True

        if len(data["first_name"]) < 3:
            is_valid = False
            flash("first_name Required !", "reg")
        if len(data["last_name"]) < 3:
            is_valid = False
            flash("last_name Required !", "reg")
        if len(data["email"]) < 3:
            flash("email Required !", "reg")
            is_valid = False
        elif not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email address", "reg")
            is_valid = False
        else:
            # data_for_email = {"email": data["email"]}
            potential_user = Player.get_by_email(data)
            if potential_user:
                is_valid = False
                flash("email already taken, hopefully by you! ", "reg")
        if len(data["password"]) < 8:
            is_valid = False
            flash("password Required", "reg")
        elif not data["password"] == data["confirm_password"]:
            is_valid = False
            flash("passwords don't match!", "reg")
        return is_valid
