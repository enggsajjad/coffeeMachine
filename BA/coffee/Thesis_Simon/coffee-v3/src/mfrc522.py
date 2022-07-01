class MFRC522:
    PICC_REQIDL = 0
    MI_OK = 1

    def MFRC522_Request(self, a):
        return (1, 0)

    def MFRC522_Anticoll(self):
        return (self.MI_OK, [136, 4, 28, 224, 112])
        # return (self.MI_OK, [1, 4, 28, 224, 112])