import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton,
    QFileDialog, QVBoxLayout, QWidget, QMenu, QAction
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import numpy as np
from PIL import Image

from filters.convolution import apply_mean_filter, apply_median_filter, apply_edge_filter

class ImageProcessor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Görüntü İşleme Uygulaması")
        self.setGeometry(100, 100, 800, 600)

        self.original_image = None
        self.image_label = QLabel("Bir görüntü seçin", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.image_label.customContextMenuRequested.connect(self.show_context_menu)

        # Buton
        self.open_button = QPushButton("Görüntü Aç")
        self.open_button.clicked.connect(self.load_image)
        self.mean_button = QPushButton("Ortalama Filtresi")
        self.mean_button.clicked.connect(self.apply_mean)
        self.median_button = QPushButton("Ortanca Filtresi")
        self.median_button.clicked.connect(self.apply_median)
        self.edge_button = QPushButton("Kenar Tespiti")
        self.edge_button.clicked.connect(self.apply_edge)

        layout = QVBoxLayout()
        layout.addWidget(self.open_button)
        layout.addWidget(self.image_label)
        layout.addWidget(self.mean_button)
        layout.addWidget(self.median_button)
        layout.addWidget(self.edge_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Görüntü Seç", "", "Image Files (*.png *.jpg *.bmp *.pnm)")
        if path:
            self.original_image = Image.open(path).convert("RGB")
            self.show_image(self.original_image)

    def show_image(self, pil_image):
        # Pillow görüntüsünü numpy dizisine dönüştür
        np_image = np.array(pil_image)

        # RGB mi kontrol et
        if len(np_image.shape) == 3 and np_image.shape[2] == 3:
            height, width, channel = np_image.shape
            bytes_per_line = 3 * width
            qimage = QImage(np_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        else:
            # Gri görüntü ise
            height, width = np_image.shape
            bytes_per_line = width
            qimage = QImage(np_image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)

        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))

    def show_context_menu(self, pos):
        if self.original_image:
            menu = QMenu(self)
            save_action = QAction("Görüntüyü Kaydet", self)
            save_action.triggered.connect(self.save_image)
            menu.addAction(save_action)
            menu.exec_(self.image_label.mapToGlobal(pos))

    def save_image(self):
        path, _ = QFileDialog.getSaveFileName(self, "Görüntüyü Kaydet", "", "PNG Files (*.png);;JPG Files (*.jpg)")
        if path and self.original_image:
            self.original_image.save(path)
    
    def apply_mean(self):
        if self.original_image:
            gray = self.original_image.convert("L")  # Griye çevir
            gray_np = np.array(gray)
            filtered_np = apply_mean_filter(gray_np)
            filtered_image = Image.fromarray(filtered_np)
            self.show_image(filtered_image)

    def apply_median(self):
        if self.original_image:
            gray = self.original_image.convert("L")
            gray_np = np.array(gray)
            filtered_np = apply_median_filter(gray_np)
            filtered_image = Image.fromarray(filtered_np)
            self.show_image(filtered_image)

    def apply_edge(self):
        if self.original_image:
            gray = self.original_image.convert("L")
            gray_np = np.array(gray)
            filtered_np = apply_edge_filter(gray_np)
            filtered_image = Image.fromarray(filtered_np)
            self.show_image(filtered_image)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessor()
    window.show()
    sys.exit(app.exec_())
