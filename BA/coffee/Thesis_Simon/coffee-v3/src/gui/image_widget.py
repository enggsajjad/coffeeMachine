import logging
import sys

from PyQt5.QtCore import QDir, QEvent, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QImage, QImageReader, QPainter, QPixmap, QPen
from PyQt5.QtWidgets import (QApplication, QFileDialog, QGesture,
                             QGestureEvent, QLabel, QWidget, QPinchGesture,
                             QPanGesture, QSizePolicy)

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

class ImageWidget(QWidget):
    position = 0
    horizontal_offset = 0
    vertical_offset = 0
    scale_factor = 1
    current_step_scale_factor = 1
    max_width = 0
    max_height = 0

    is_transformed = False
    transform = pyqtSignal()

    prev_image = None
    next_image = None
    current_image = None

    path = ""
    files = None

    def __init__(self, parent=None, max_width=2000, max_height=2000, horizontal_offset=0, vertical_offset=0):
        super().__init__(parent)
        # self.image_label = QLabel()
        # self.image_label.setSizePolicy(
        #     QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.image_label.setScaledContents(True)
        # self.setCentralWidget(self.image_label)
        # self.setCentralWidget(self)
        # self.setWindowTitle("Image Viewer")
        # self.resize(500, 400)
        self.max_width = max_width
        self.max_height = max_height

        self.horizontal_offset_default = horizontal_offset
        self.vertical_offset_default = vertical_offset
        self.horizontal_offset = self.horizontal_offset_default
        self.vertical_offset = self.vertical_offset_default
        self.setMinimumSize(200, 200)

    def grabGestures(self, gestures):
        for gesture in gestures:
            self.grabGesture(gesture)

    def event(self, e):
        if (e.type() == QEvent.Gesture):
            return self.gesture_event(e)
        return super().event(e)

    def resizeEvent(self, event):
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        iw = self.current_image.width()
        ih = self.current_image.height()
        wh = self.height()
        ww = self.width()

        p.translate(ww/2, wh/2)
        p.translate(self.horizontal_offset, self.vertical_offset)
        p.scale(self.current_step_scale_factor * self.scale_factor,
                self.current_step_scale_factor * self.scale_factor)
        p.translate(-iw/2, -ih/2)
        p.drawImage(0, 0, self.current_image)
        

    def gesture_event(self, event):
        pinch = event.gesture(Qt.PinchGesture)
        if pinch:
            self.pinch_triggered(pinch)
        pan = event.gesture(Qt.PanGesture)
        if pan:
            self.pan_triggered(pan)
        swipe = event.gesture(Qt.SwipeGesture)
        if swipe:
            self.swipe_triggered(swipe)
        tap = event.gesture(Qt.TapGesture)
        if tap:
            self.swipe_triggered(tap)

        if not self.is_transformed:
            self.is_transformed = True
            self.transform.emit()
        return True

    def reset_transform(self):
        self.is_transformed = False
        self.scale_factor = 1
        self.current_step_scale_factor = 1
        self.horizontal_offset = self.horizontal_offset_default
        self.vertical_offset = self.vertical_offset_default
        self.update()

    def pinch_triggered(self, gesture):
        change_flags = gesture.changeFlags()
        if change_flags & QPinchGesture.ScaleFactorChanged:
            self.current_step_scale_factor = gesture.totalScaleFactor()
        if gesture.state() == Qt.GestureFinished:
            self.scale_factor *= self.current_step_scale_factor
            self.current_step_scale_factor = 1

        # self.translate_image(gesture.startCenterPoint() - gesture.centerPoint())

        self.update()

    def pan_triggered(self, gesture):
        delta = gesture.delta()
        self.horizontal_offset += delta.x()
        self.vertical_offset += delta.y()
        self.update()

    def swipe_triggered(self, gesture):
        print(gesture)

    def tap_triggered(self, gesture):
        print(gesture)

    def open_directory(self, path):
        self.path = path
        directory = QDir(path)
        name_filters = ["*.jpg", "*.png", "*.jpeg", "*.gif"]
        self.files = directory.entryList(
            name_filters, QDir.Files | QDir.Readable, QDir.Time | QDir.Reversed)
        if not self.files:
            LOG.error("Directory not found or empty: %s", directory.path())
        self.go_last_image()

    def load_image(self, file_name):
        reader = QImageReader(file_name)
        reader.setAutoTransform(True)
        if not reader.canRead():
            LOG.warning("%s: can't load image",
                        QDir.toNativeSeparators(file_name))
            return QImage()

        image = QImage()
        if not reader.read(image):
            LOG.warning("%s: corrupted image",
                        QDir.toNativeSeparators(file_name))
            return QImage()

        # Reduce in case someone has large photo images
        # This reduces the maximum pixels in the image, not the scale when painting
        # maximum_size = QSize(2000, 2000)
        # if image.size().width() > maximum_size.width() or image.height() > maximum_size.height():
        #     image = image.scaled(
        #         maximum_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # if image.width() > image.height():
        #     if image.width() > self.width():
        #         self.scale_factor = self.width() / image.width()
        #     else: 
        #         self.scale_factor = image.width() / self.width()
        # elif image.height() > image.width():
        #     if image.height() > self.height():
        #         self.scale_factor = self.height() / image.height()

        # image = image.scaled(self.max_width, self.max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # if image.width() < self.max_width / 2:
        #     image = image.scaled(self.max_width * 2 / 3, self.max_height * 10, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        #     self.vertical_offset += image.height()
        #     return image

        return image.scaled(self.max_width, self.max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)


    def go_next_image(self):
        if not self.files:
            return

        if self.position < len(self.files) - 1:
            self.position += 1
        else:
            self.position = 0

        self.prev_image = self.current_image
        self.current_image = self.next_image
        if self.position + 1 < len(self.files):
            self.next_image = self.load_image(
                self.path + '/' + self.files[self.position + 1])
        else:
            self.next_image = self.load_image(
                self.path + '/' + self.files[0])

        self.update()

    def go_prev_image(self):
        if not self.files:
            return

        if self.position >= 0:
            self.position -= 1
        else:
            self.position = len(self.files) - 2

        self.next_image = self.current_image
        self.current_image = self.prev_image
        self.prev_image = self.load_image(
            self.path + '/' + self.files[self.position-1])
        
        self.update()

    def go_last_image(self):
        if not self.files:
            return

        self.position = len(self.files) - 1
        self.go_to_image(self.position)

        self.update()

    def go_to_image(self, index):
        if not self.files:
            return

        if index < 0 or index >= len(self.files):
            LOG.warning("go_to_image: invalid index: %s", index)
            return

        if index == self.position + 1:
            self.go_next_image()
            return

        if self.position > 0 and index == self.position - 1:
            self.go_prev_image()
            return

        self.position = index

        if index > 0:
            self.prev_image = self.load_image(
                self.path + '/' + self.files[self.position - 1])
        else:
            self.prev_image = QImage()

        self.current_image = self.load_image(
            self.path + '/' + self.files[self.position])
        if self.position+1 < len(self.files):
            self.next_image = self.load_image(
                self.path + '/' + self.files[self.position + 1])
        else:
            self.next_image = self.load_image(
                self.path + '/' + self.files[0])
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    image_viewer = ImageWidget()
    image_viewer.show()
    # image_viewer.open()
    # image_viewer.scale_image(image_viewer.scaleFactor)
    image_viewer.open_directory("/home/skorz/Pictures")
    image_viewer.grabGesture(Qt.PinchGesture)
    image_viewer.grabGesture(Qt.PanGesture)
    image_viewer.grabGesture(Qt.SwipeGesture)
    image_viewer.grabGesture(Qt.TapGesture)
    sys.exit(app.exec_())
