import logging

from PyQt5.QtCore import Qt, QTimer, QEvent, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog

import gui.got_user_gen as got_user_gen

from order import MILK_PRICE, COFFEE_PRICE, WATER_PRICE
from util import price_to_str, str_to_price, DispensingStatus

LOG = logging.getLogger(__name__)

class GotUser(QDialog, got_user_gen.Ui_Dialog):
    cancel = pyqtSignal()
    order_complete = pyqtSignal(bool, bool)

    CANCEL_TIMEOUT = 180
    OK_TIMEOUT = 20

    cancel_timer_countdown = 0
    ok_timer_countdown = 0

    # if coffee was ordered, set in display_order, later needed in complete_order
    coffee = True

    # if milk was preset
    milk = False

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.with_milk_label.hide()

        self.cancel_timer = QTimer(self)
        self.cancel_timer.timeout.connect(self.cancel_timer_update)
        self.ok_timer = QTimer(self)
        self.ok_timer.timeout.connect(self.ok_timer_update)

        self.cancel_button.clicked.connect(self.cancel_session)
        self.dismiss_button.clicked.connect(self.hide_warning)
        self.dismiss_button_deny.clicked.connect(self.cancel_button.click)
        self.cancel_button.clicked.connect(lambda: LOG.debug("Canceled by user."))
        self.add_milk.clicked.connect(self.calculate_total)
        self.ok_button.clicked.connect(self.complete_order)

        self.water_yes_button.clicked.connect(self.display_water_order)
        self.water_no_button.clicked.connect(self.display_coffee_order)

        self.grabGesture(Qt.TapGesture)

    def event(self, e):
        if (e.type() == QEvent.Gesture):
            tap = e.gesture(Qt.TapGesture)
            if tap:
                self.reset_cancel_timer()
                LOG.debug("Cancel timer reset by user touch")
            return True
        return super().event(e)

    @pyqtSlot(str, int, bool, str, int)
    def display_user(self, user_name, balance, milk, last_order_summary, dispensing_status):
        self.milk = milk
        self.user.setText("Welcome " + user_name + "!")
        self.user.setAlignment(Qt.AlignCenter)

        self.balance.setText(price_to_str(balance))

        self.add_milk_pre.setChecked(milk)
        self.last_order.setText(last_order_summary)


        if balance > 0:
            self.balance.setStyleSheet("color: black; font-size: 36px; font-weight: bold;")
        else:
            self.balance.setStyleSheet("color: red; font-size: 36px; font-weight: bold;")
        
        if dispensing_status == DispensingStatus.ALLOW:
            self.stackedWidget.setCurrentWidget(self.unlocked)
        elif dispensing_status == DispensingStatus.WARN:
            self.stackedWidget.setCurrentWidget(self.balance_warning)
        elif dispensing_status == DispensingStatus.DENY:
            self.stackedWidget.setCurrentWidget(self.balance_denied)

        self.start_cancel_timer()


    @pyqtSlot(bool, bool)
    # TODO: remove milk parameter
    def display_order(self, coffee, milk):
        self.stop_cancel_timer()

        # bug: sometimes coffee is recognized as water,
        # as a workaround default is coffee and water needs to be confirmed in self.water_page dialog
        self.display_coffee_order()
        if coffee:
            self.coffee_or_water.setCurrentWidget(self.coffee_page)
        else:
            self.coffee_or_water.setCurrentWidget(self.water_page)
            self.without_milk_label.hide()
            self.with_milk_label.hide()

        self.milk_price.setText(price_to_str(MILK_PRICE))

        self.coffee = True


        self.stackedWidget.setCurrentWidget(self.ordered)

    def display_coffee_order(self):
        self.label.setText("Coffee")
        self.price.setText(price_to_str(COFFEE_PRICE))
        self.water_drop.hide()
        self.coffee_beans.show()
        self.with_milk_label.setVisible(self.add_milk.isChecked())
        self.without_milk_label.setHidden(self.add_milk.isChecked())
        self.coffee = True
        self.coffee_or_water.setCurrentWidget(self.coffee_page)
        self.milk_label.setEnabled(self.add_milk.isChecked())
        self.milk_price.setEnabled(self.add_milk.isChecked())
        self.calculate_total()

    def display_water_order(self):
        self.label.setText("Water")
        self.price.setText(price_to_str(WATER_PRICE))
        self.water_drop.show()
        self.coffee_beans.hide()
        self.coffee = False

        # water + milk disabled
        self.milk_label.setEnabled(False)
        self.milk_price.setEnabled(False)

        self.calculate_total()

    def calculate_total(self):
        price = str_to_price(self.price.text())
        if self.milk_price.isEnabled():
            price += str_to_price(self.milk_price.text())
        self.total_price.setText(price_to_str(price))
        return price

    def start_cancel_timer(self):
        self.cancel_timer_countdown = self.CANCEL_TIMEOUT + 1
        self.cancel_button.setText("Cancel")
        self.cancel_timer_update()
        self.cancel_timer.start(1000)

    def stop_cancel_timer(self):
        self.cancel_timer.stop()
        self.cancel_timer_countdown = 0

    def reset_cancel_timer(self):
        self.stop_cancel_timer()
        self.start_cancel_timer()

    def cancel_timer_update(self):
        if self.cancel_timer_countdown > 0:
            self.cancel_timer_countdown = self.cancel_timer_countdown - 1
            if self.cancel_timer_countdown < 30:
                self.cancel_button.setText("Cancel ({})".format(self.cancel_timer_countdown))
        else:
            LOG.debug("Canceled by timer.")
            self.cancel_session()

    def start_ok_timer(self):
        self.ok_timer_countdown = self.OK_TIMEOUT + 1
        self.ok_button.setText("OK")
        self.ok_timer_update()
        self.ok_timer.start(1000)

    def stop_ok_timer(self):
        self.ok_timer.stop()
        self.ok_timer_countdown = 0
        self.ok_button.setText("OK")

    def ok_timer_update(self):
        if self.ok_timer_countdown > 0:
            self.ok_timer_countdown = self.ok_timer_countdown - 1
            self.ok_button.setText("OK\n({})".format(self.ok_timer_countdown))
        else:
            self.ok_button.click()

    def complete_order(self):
        self.stop_ok_timer()
        self.order_complete.emit(self.coffee, self.add_milk.isChecked())

    def cancel_session(self):
        self.stop_cancel_timer()
        self.cancel.emit()
        self.stackedWidget.setCurrentWidget(self.unlocked)

    def hide_warning(self):
        self.add_milk_pre.setChecked(self.milk)
        self.stackedWidget.setCurrentWidget(self.unlocked)
