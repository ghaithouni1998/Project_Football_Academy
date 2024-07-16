from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import DATABASE


class Offer:
    def __init__(self, data):
        self.id = data["id"]

        self.position = data["position"]

        self.age = data["age"]

        self.weight = data["weight"]

        self.height = data["height"]

        self.skills = data["skills"]

        self.trainer_id = data["trainer_id"]

        self.scout_id = data["scout_id"]

        self.created_at = data["created_at"]

        self.updated_at = data["updated_at"]

        # self.poster = user.User.get_by_id({"id": self.user_id})

    @classmethod
    def create(cls, data):
        query = """INSERT INTO offers (position, age, weight, height, skills, trainer_id)

                VALUES(%(position)s, %(age)s, %(weight)s, %(height)s, %(skills)s, %(trainer_id)s);"""

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all_libre(cls):
        query = "SELECT * FROM offers WHERE scout_id = 0;"

        results = connectToMySQL(DATABASE).query_db(query)

        all_offers = []

        for row in results:
            all_offers.append(cls(row))
        return all_offers

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM offers;"

        results = connectToMySQL(DATABASE).query_db(query)

        all_offers = []

        for row in results:
            all_offers.append(cls(row))
        return all_offers

    @classmethod
    def offers_one_player(cls, data):
        query = """SELECT * FROM offers
   JOIN player_offers_selection ON player_offers_selection.offer_id = offers.id
        WHERE offers.id IN ( SELECT player_offers_selection.offer_id FROM player_offers_selection) and player_id = %(id)s ;"""

        results = connectToMySQL(DATABASE).query_db(query, data)

        all_offers = []
        if results:
            for row in results:
                all_offers.append(cls(row))
        return all_offers

    @classmethod
    def offers_for_players(cls):
        query = """SELECT * FROM offers
        WHERE offers.scout_id !=0 AND offers.id NOT IN (SELECT offer_id FROM player_offers_selection);"""

        results = connectToMySQL(DATABASE).query_db(query)

        all_offers = []

        for row in results:
            all_offers.append(cls(row))
        return all_offers

    @classmethod
    def get_by_id(cls, data):
        query = """

        SELECT * FROM offers 

        WHERE id = %(id)s;"""

        result = connectToMySQL(DATABASE).query_db(query, data)

        return cls(result[0])

    @classmethod
    def get_offer_by_scout(cls, data):
        query = """

            SELECT * FROM offers

            WHERE scout_id = %(scout_id)s;"""

        results = connectToMySQL(DATABASE).query_db(query, data)

        offers = []

        for row in results:
            offers.append(cls(row))
        return offers

    @classmethod
    def get_offer_by_trainer(cls, data):
        query = """

            SELECT * FROM offers

            WHERE trainer_id = %(trainer_id)s;"""

        results = connectToMySQL(DATABASE).query_db(query, data)

        offers = []

        for row in results:
            offers.append(cls(row))
        return offers

    @classmethod
    def edit(cls, data):
        query = """

        UPDATE offers SET position = %(position)s, age= %(age)s, weight = %(weight)s, height = %(height)s, skills = %(skills)s

        WHERE id = %(id)s;"""

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = """DELETE FROM offers 

        WHERE id = %(id)s;"""

        return connectToMySQL(DATABASE).query_db(query, data)
