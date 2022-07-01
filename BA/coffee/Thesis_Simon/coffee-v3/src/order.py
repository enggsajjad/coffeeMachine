import logging
import urllib.error
import urllib.request as request

import pymysql

from util import price_to_str

LOG = logging.getLogger(__name__)

# set prices
MILK_PRICE = 5
COFFEE_PRICE = 20
WATER_PRICE = 1


class Order():
    """Represents an order"""

    def __init__(self, uid, coffee, milk, cheated=False):
        """uid: str, coffee: bool, milk: bool"""
        self.uid = uid
        self.coffee = coffee
        self.milk = milk
        self.cheated = cheated
        self.price = calculate_price(coffee, milk)

    def __repr__(self):
        return "<Order uid:{} coffee:{} milk:{} price:{} cheated:{}>".format(
            self.uid, self.coffee, self.milk, self.price, self.cheated)

def calculate_price(coffee, milk):
    price = 0
    if coffee:
        price += COFFEE_PRICE
    else:
        price += WATER_PRICE

    if milk:
        price += MILK_PRICE

    return price


def commit(order):
    """Inserts order into local db and updates user's balance. Returns row id of order."""
    conn = pymysql.connect(host='localhost', user='root',
                           passwd='root', db='coffee')
    try:
        cur = conn.cursor()

        sql = "SELECT @id:=user_id FROM uids WHERE uid = %s;"
        cur.execute(sql, (order.uid,))

        sql = "UPDATE users SET balance = balance - %s WHERE id = @id;"
        cur.execute(sql, (order.price))

        sql = "INSERT INTO orders (`uid`, `coffee`, `milk`, `price`, `cheated`) VALUES (%s, %s, %s, %s, %s);"
        cur.execute(sql, (order.uid, order.coffee, order.milk, order.price, order.cheated,))
        conn.commit()

        cur.execute("SELECT LAST_INSERT_ID();")
        return cur.fetchone()[0]
    finally:
        conn.close()


def set_synchronized(id_in_db, is_synchronized=True):
    """Marks the order with id_in_db as synchronized with the server"""
    conn = pymysql.connect(host='localhost', user='root',
                           passwd='root', db='coffee')
    try:
        cur = conn.cursor()
        sql = "UPDATE orders SET is_synchronized = %s WHERE id = %s"
        cur.execute(sql, (is_synchronized, id_in_db,))
        conn.commit()
    except:
        # TODO fatal if an error occurs here program cannot recover, maybe show error in gui
        LOG.critical("Could not set order to synchronized.")
    finally:
        conn.close()


def push(id_in_db, order):
    """Pushes order to the server"""
    if id_in_db is not None:
        # MAYBE first set to true and undo if pushing to server fails.
        # This avoids the case that the order was successfully pushed to the server
        # but updating it in the database failed,
        # which would possibly result in pushing the order to the server a second time
        # self._set_synchronized(True)
        try:
            black = "false" if order.milk else "true"
            water = "false" if order.coffee else "true"
            cheated = "true" if order.cheated else "false"
            req = request.urlopen("http://i80web2.itec.kit.edu/coffee/buy.php?rfid={}&black={}&water={}&cheated={}"
                                  .format(order.uid, black, water, cheated))
            if req.getcode() == 200:
                LOG.debug("Order successfully passed to server: %s", order)
                set_synchronized(id_in_db)
            else:
                LOG.error(
                    "Order couldn't be passed to server, status code: %i", req.getcode())
        except urllib.error.URLError:
            LOG.error(
                "Could not pass order to server. Maybe the connection is down. %s", order)
        except:
            LOG.exception(
                "An error occured while passing order to server: %s", order)
    else:
        LOG.error("Parameter id_in_db is None")


def get_last_order_timestamp():
    conn = pymysql.connect(host='localhost', user='root',
                           passwd='root', db='coffee')
    try:
        cur = conn.cursor()
        cur.execute("SELECT ts FROM orders ORDER BY id DESC LIMIT 1")
        return cur.fetchone()[0]
    except:
        # TODO fatal if an error occurs here programm cannot recover, maybe show error in gui
        pass
    finally:
        conn.close()

def get_last_order_summary(uid):
    conn = pymysql.connect(host='localhost', user='root',
                           passwd='root', db='coffee')
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT ts, coffee, milk, price FROM orders WHERE uid IN \
                (SELECT uid FROM uids WHERE user_id = (SELECT user_id FROM uids WHERE uid = %s)) \
                ORDER BY id DESC LIMIT 1", (uid,))
            result = cur.fetchone()
            if result is None:
                return ""
            ts = result[0]
            coffee = result[1]
            milk = result[2]
            price = result[3]

            summary = ts.strftime("%d/%m/%y %H:%Mh") +  "\n"
            if coffee:
                summary += "Coffee"
            else:
                summary += "Water"
            if milk:
                summary += " + Milk"
            summary += "\n" + price_to_str(price)

            return summary
    finally:
        conn.close()

def push_all():
    """Push all unsynchronized orders to server"""
    conn = pymysql.connect(host='localhost', user='root',
                           passwd='root', db='coffee')
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, uid, coffee, milk FROM orders WHERE is_synchronized = FALSE")
        rows = cur.fetchall()

        for row in rows:
            order = Order(row[1], row[2], row[3])
            LOG.info("Pushing unsynchronized order to accounting server: %s", order)
            push(row[0], order)
    finally:
        conn.close()


def process_order(uid, coffee, milk, cheated=False):
    """Process order and return new balance"""
    new_order = Order(uid, coffee, milk, cheated)
    order_id = commit(new_order)
    push(order_id, new_order)
    return new_order

if __name__ == "__main__":
    # process_order('0123', False, True)
    push_all()