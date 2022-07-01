import urllib.request
import sys

def getUserInfo(uid):
    response = ""
    try:
        req = urllib.request.urlopen("http://i80misc01.itec.kit.edu/coffee/getuser.php?rfid=" + uid)
        response = req.read().decode('utf-8')
    except:
        with open("/home/pi/logs/userInfo.log", "a") as f:
            f.write("User Info error: %s \n" % sys.exc_info()[0])
        pass
    return response

def passOrder(uid, black, water):
    response = ""
    try:
        req = urllib.request.urlopen("http://i80misc01.itec.kit.edu/coffee/buy.php?rfid=" + uid + "&black=" + black + "&water=" + water)
    #    response = req.read().decode('utf-8')
    except:
        with open("/home/pi/logs/order.log", "a") as f:
            f.write("Order error: %s" % sys.exc_info()[0])
        pass
    #return response
