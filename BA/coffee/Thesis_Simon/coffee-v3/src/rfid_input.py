import logging
import time

import mfrc522

from util import Msg, receive_cmd

logger = logging.getLogger(__name__)


def read(conn):

    reader = mfrc522.MFRC522()
    timer = time.time()
    try:
        while True:
            time.sleep(0.5)
            receive_cmd(conn)
            if time.time() - timer > 5 * 60:
                timer = time.time()
                logger.info("MFRC522 restart")
                # restart rfid reader because it would freeze/sleep after a few hours
                reader.Close_MFRC522()
                reader = mfrc522.MFRC522()

            (status, _tag_type) = reader.MFRC522_Request(reader.PICC_REQIDL)
            if status != reader.MI_OK:
                logger.debug("Nothing read from reader")
                continue

            (status, temp) = reader.MFRC522_Anticoll()
            if status != reader.MI_OK:
                logger.error("Couldn't read rfid")
                continue

            uid = hex(temp[0])[2:] + hex(temp[1])[2:] + \
                hex(temp[2])[2:] + hex(temp[3])[2:]
            logger.info("Read raw rfid: %s, calculated hex representation: %s", " ".join(map(str, temp)), uid)
            
            # dev_user
            if uid == '884211b':
                uid = '0123'

            conn.send(Msg.E_GOT_ID)
            conn.send(uid)

    except:
        logger.exception("An error occured while handling rfid input")
    finally:
        reader.Close_MFRC522()
