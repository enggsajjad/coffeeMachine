from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
 
from gui.get_uid_gen import Ui_GetUid
from gui.image_widget import ImageWidget

class GetUid(QDialog, Ui_GetUid):

    IMAGE_DIR = "res/images"
    NEXT_TIMEOUT = 60 # 120s
    next_timer_count = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        image_widget = ImageWidget(self, 796, 392, vertical_offset=42)
        image_widget.show()
        image_widget.open_directory(self.IMAGE_DIR)
        image_widget.setGeometry(0, 0, self.width(), self.height())
        image_widget.grabGestures([Qt.PinchGesture, Qt.PanGesture])
        image_widget.lower()
        self.image_widget = image_widget

        self.button_left.clicked.connect(image_widget.go_prev_image)
        self.button_right.clicked.connect(image_widget.go_next_image)
        self.button_last.clicked.connect(image_widget.go_last_image)
        self.button_left.clicked.connect(self.button_reset.click)
        self.button_right.clicked.connect(self.button_reset.click)
        self.button_last.clicked.connect(self.button_reset.click)

        self.button_left.clicked.connect(self.next_timer_start)
        self.button_right.clicked.connect(self.next_timer_start)
        self.button_last.clicked.connect(self.next_timer_start)

        self.button_reset.hide()
        self.button_reset.clicked.connect(image_widget.reset_transform)
        self.button_reset.clicked.connect(self.button_reset.hide)
        image_widget.transform.connect(self.button_reset.show)

        self.text.hide()

        self.progressBar.setRange(0, self.NEXT_TIMEOUT)
        self.next_timer = QTimer(self)
        self.next_timer.timeout.connect(self.next_timer_update)
        self.next_timer_start()
    
    def next_timer_start(self):
        self.progressBar.reset()
        self.next_timer_count = 0
        self.next_timer_update()
        self.next_timer.start(1000)

    def next_timer_stop(self):
        self.progressBar.reset()
        self.next_timer_count = 0
        self.next_timer.stop()

    def next_timer_update(self):
        if self.next_timer_count < self.NEXT_TIMEOUT:
            self.next_timer_count = self.next_timer_count + 1
            self.progressBar.setValue(self.next_timer_count)
        else:
            self.button_right.click()
    
    def show_making_coffee(self, show):
        if show:
            self.text.show()
            self.admin_button.hide()
        else:
            self.text.hide()
            self.admin_button.show()

    @pyqtSlot()
    def reload_images(self):
        self.image_widget.open_directory(self.IMAGE_DIR)