import logging
import urllib.request as request

import pymysql.cursors

import util

LOG = logging.getLogger(__name__)


class User():
    """Represents a user"""

    def __init__(self, token, uid, name, balance, coffee_milk_pref=False, water_milk_pref=False):
        """ token: str, uid: str, name: str, balance: int, coffee_milk_pref: bool """
        self.token = token
        self.uid = uid
        self.name = name
        self.balance = balance
        self.coffee_milk_pref = coffee_milk_pref
        self.water_milk_pref = water_milk_pref

    def __repr__(self):
        return "<User token:{} uid:{} name:{} balance:{} coffee_milk_pref:{} water_milk_pref:{}>".format(
            self.token, self.uid, self.name, self.balance, self.coffee_milk_pref, self.water_milk_pref)


def commit(user):
    """Inserts or updates current user in local db. Returns id in db"""
    db_conn = pymysql.connect(
        host='localhost', user='root', passwd='root', db='coffee')
    try:
        with db_conn.cursor() as cur:
            # insert and update user attributes
            sql = "INSERT INTO users (`token`, `name`, `balance`, `coffee_milk_pref`, `water_milk_pref`) \
                    VALUES (%s, %s, %s, %s, %s) \
                ON DUPLICATE KEY UPDATE \
                `token`= VALUES(`token`) , `name` = VALUES(`name`) , `balance` = VALUES(`balance`) , `coffee_milk_pref` = VALUES(`coffee_milk_pref`), `water_milk_pref` = VALUES(`water_milk_pref`)"
            cur.execute(sql, (user.token, user.name, user.balance,
                              user.coffee_milk_pref, user.water_milk_pref))
            db_conn.commit()

            cur.execute("SELECT id FROM users WHERE token = %s", (user.token))
            id_in_db = cur.fetchone()[0]

            # insert new uids
            cur.execute("INSERT IGNORE INTO uids (uid, user_id) VALUES (%s, %s)",
                        (user.uid, id_in_db,))
            db_conn.commit()

            return id_in_db
    except pymysql.OperationalError:
        util.terminate_after_error()
    finally:
        db_conn.close()


def update_milk_pref(token, coffee, milk):
    db_conn = pymysql.connect(
        host='localhost', user='root', passwd='root', db='coffee')
    try:
        with db_conn.cursor() as cur:
            if coffee:
                sql = "UPDATE users SET coffee_milk_pref = %s WHERE token = %s"
            else:
                sql = "UPDATE users SET water_milk_pref = %s WHERE token = %s"
            cur.execute(sql, (milk, token,))
            db_conn.commit()
    finally:
        db_conn.close()


def _get_uid_list():
    req = request.urlopen(
        "http://i80web2.ira.uka.de/coffee/getusers.php?secret=42!")
    response = req.read().decode('utf-8')
    response = response.replace(' ', '').split('\n')
    temp = list(map(lambda x: x.split(';')[:3], response))
    return temp


def _get_user_from_server(uid):
    """Get user from accounting server"""
    try:
        req = request.urlopen(
            "http://i80web2.itec.kit.edu/coffee/getuser.php?rfid=" + uid)
        resp = req.read().decode('utf-8').split(";")
        if len(resp) < 4:
            return
        coffee_milk_pref = False
        if resp[3] == "milk":
            coffee_milk_pref = True
        return User(resp[4], uid, resp[1], int(resp[2]), coffee_milk_pref)
    except:
        LOG.exception(
            "An exception was raised while trying to get user from accounting server")


def _get_user_from_db(uid):
    """Get user from local database"""
    db_conn = pymysql.connect(
        host='localhost', user='root', passwd='root', db='coffee')
    try:
        with db_conn.cursor() as cur:
            cur.execute("SELECT `token`, `name`, `balance`, `coffee_milk_pref`, `water_milk_pref` FROM users \
                WHERE id = (SELECT user_id FROM uids WHERE uid = %s)", (uid,))
            result = cur.fetchone()
            if result is not None:
                return User(result[0], uid, result[1], result[2], result[3], result[4])
    except:
        LOG.exception(
            "An exception was raised while trying to get user from local database")
    finally:
        db_conn.close()


def get_user(uid):
    """Get user by uid. uid has to be one of the user's registered rfid tags"""

    # try to fetch current user information from server
    server_user = _get_user_from_server(uid)
    db_user = _get_user_from_db(uid)

    if server_user:
        LOG.debug("Got user from server: %s", server_user)

        if db_user:
            # user already in db, just update uid, balance, do not overwrite milk preference
            db_user.uid = uid
            db_user.balance = server_user.balance
            LOG.debug("Updated user in local db: %s", db_user)
        else:
            commit(server_user)
            return server_user
    else:
        if db_user:
            LOG.debug("Could not reach server, only fetching user from local db")
        else:
            LOG.debug("Could not get user from accounting server, \
                either because the rfid-token is not registered yet, or the network is down.")

    if db_user:
        commit(db_user)
    return db_user
