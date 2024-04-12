import psycopg2
from flask import Flask, request
from psycopg2.extras import RealDictCursor

app = Flask(__name__)


class Atlas:
    def __init__(self):
        app.logger.info("acquiring psycopg connection")
        self.connection = psycopg2.connect(host="atlas",
                                           port="5432",
                                           dbname="atlas",
                                           user="underhill",
                                           password="baggins")
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()


@app.route('/embark', methods=['POST'])
def embark():
    with Atlas() as atlas:
        expedition_response = create_expedition(atlas)
        return expedition_response, 200


def create_expedition(atlas):
    query = """
        SELECT trail.trail_id, trail.port, count(expedition.expedition_id)
        FROM trail
             LEFT JOIN public.expedition on trail.trail_id = expedition.trail_id
        WHERE trail.demerits = 0
        GROUP BY trail.trail_id
        ORDER BY count(expedition.expedition_id)
    """
    atlas.cursor.execute(query)
    trail_data = atlas.cursor.fetchone()
    if trail_data is None:
        raise RuntimeError("no available trails for expedition")
    trail_id = trail_data["trail_id"]
    port = trail_data["port"]

    query = """
        INSERT INTO expedition (trail_id)
        VALUES (%(trail_id)s)
        RETURNING expedition_id;
    """
    parameters = {
        "trail_id": trail_id
    }
    atlas.cursor.execute(query, vars=parameters)
    expedition_id = atlas.cursor.fetchone()["expedition_id"]
    atlas.connection.commit()
    response = {"port": port, "expedition_id": expedition_id}
    return response


@app.route('/conclude', methods=['POST'])
def conclude():
    payload = request.get_json(force=True)
    expedition_id = payload["expedition_id"]
    with Atlas() as atlas:
        conclude_expedition(atlas, expedition_id)
        return {}, 200


def conclude_expedition(atlas, expedition_id):
    query = """
        DELETE FROM expedition
        WHERE expedition_id = %(expedition_id)s;
    """
    parameters = {
        "expedition_id": expedition_id
    }
    atlas.cursor.execute(query, vars=parameters)
    atlas.connection.commit()


@app.route('/demerit', methods=['POST'])
def demerit():
    payload = request.get_json(force=True)
    expedition_id = payload["expedition_id"]
    with Atlas() as atlas:
        demerit_trail(atlas, expedition_id)
        return {}, 200


def demerit_trail(atlas, expedition_id):
    query = """
        SELECT trail.trail_id
        FROM trail
             LEFT JOIN public.expedition on trail.trail_id = expedition.trail_id
        WHERE expedition.expedition_id = %(expedition_id)s;
    """
    parameters = {
        "expedition_id": expedition_id,
    }
    atlas.cursor.execute(query, vars=parameters)
    trail_data = atlas.cursor.fetchone()
    if trail_data is None:
        raise RuntimeError("no available trails for expedition")
    trail_id = trail_data["trail_id"]
    query = """
        UPDATE trail 
           SET demerits = trail.demerits + 1
        WHERE trail_id = %(trail_id)s;
    """
    parameters = {
        "trail_id": trail_id,
    }
    atlas.cursor.execute(query, vars=parameters)
    atlas.connection.commit()
