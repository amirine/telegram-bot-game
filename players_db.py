import psycopg2

conn = psycopg2.connect(host="localhost",
                        port=5432,
                        database="bot",
                        user="postgres",
                        password="postgres")
cur = conn.cursor()
print("Database opened successfully")


class PlayersDataBase:

    @staticmethod
    def get_player_telegram_id(player_id: int) -> int:
        """Gets player telegram_id by player_id"""
        cur.execute("""SELECT telegram_id FROM players WHERE player_id = {}""".format(player_id))
        query_results = cur.fetchall()
        return query_results[0][0]

    @staticmethod
    def get_player_name(player_id: int) -> str:
        """Gets player_name by player_id"""
        cur.execute("""SELECT player_name FROM players WHERE player_id = {}""".format(player_id))
        query_results = cur.fetchall()
        return query_results[0][0]

    @staticmethod
    def add_player_to_db(telegram_id: int, player_name: str) -> None:
        """Adds new player with {telegram_id}, {player_name} to database"""
        query = """INSERT INTO players (telegram_id, player_name) VALUES ({}, '{}')""".format(telegram_id, player_name)
        cur.execute(query)

    @staticmethod
    def check_player_in_db(telegram_id: int) -> bool:
        """Checks if player is already in a database, returns True or False"""
        cur.execute("""SELECT * FROM players WHERE telegram_id = {}""".format(telegram_id))
        return True if cur.fetchall() else False

    @staticmethod
    def check_input_for_opponent(player_id: str) -> bool:
        """Validates inputted number for the opponent player choice"""
        try:
            player_id_number = int(player_id)
            cur.execute("""SELECT player_id FROM players WHERE player_id = {}""".format(player_id_number))
            return True if cur.fetchall() else False
        except TypeError:
            return False

    @staticmethod
    def get_all_players(telegram_id: int) -> str:
        """Returns the list of players"""
        cur.execute("""SELECT player_id, player_name FROM players WHERE telegram_id <> {}""".format(telegram_id))
        query_results = cur.fetchall()
        return '\n'.join([': '.join(map(str, x)) for x in query_results])
