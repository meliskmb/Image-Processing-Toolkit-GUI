import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton,
    QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QMenu, QAction, QMessageBox
)
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import numpy as np
from PIL import Image

from filters.convolution import apply_mean_filter, apply_median_filter, apply_edge_filter, apply_smoothing_filter, apply_sharpen_filter
from filters.histogram import calculate_histogram, plot_histogram, histogram_equalization, contrast_stretching
from filters.thresholding import manual_threshold, otsu_threshold, kapur_threshold
from filters.morphology import dilation, erosion
from filters.geometry import compute_centroid, skeletonize, rotate_image, shear_image, flip_horizontal, flip_vertical

class ImageProcessor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Görüntü İşleme Uygulaması")
        self.setGeometry(100, 100, 800, 600)

        self.original_image = None
        self.processed_image = None

        self.original_image_label = QLabel("Orijinal Görüntü", self)
        self.original_image_label.setAlignment(Qt.AlignCenter)

        self.processed_image_label = QLabel("İşlenmiş Görüntü", self)
        self.processed_image_label.setAlignment(Qt.AlignCenter)

        self.original_image_label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.original_image_label.customContextMenuRequested.connect(self.show_context_menu)

        self.open_button = QPushButton("Görüntü Aç")
        self.open_button.clicked.connect(self.load_image)

        # Filtre Butonları
        self.mean_button = QPushButton("Ortalama Filtresi")
        self.mean_button.clicked.connect(self.apply_mean)
        self.median_button = QPushButton("Ortanca Filtresi")
        self.median_button.clicked.connect(self.apply_median)
        self.edge_button = QPushButton("Kenar Tespiti")
        self.edge_button.clicked.connect(self.apply_edge)
        self.hist_button = QPushButton("Histogram Göster")
        self.hist_button.clicked.connect(self.show_histogram)
        self.equalize_button = QPushButton("Histogram Eşitleme")
        self.equalize_button.clicked.connect(self.equalize_histogram)
        self.stretch_button = QPushButton("Kontrast Germe")
        self.stretch_button.clicked.connect(self.stretch_contrast)
        self.manual_thresh_button = QPushButton("Manuel Eşikleme")
        self.manual_thresh_button.clicked.connect(self.apply_manual_threshold)
        self.otsu_button = QPushButton("Otsu Eşikleme")
        self.otsu_button.clicked.connect(self.apply_otsu)
        self.kapur_button = QPushButton("Kapur Eşikleme")
        self.kapur_button.clicked.connect(self.apply_kapur)
        self.dilate_button = QPushButton("Dilation (Genişletme)")
        self.dilate_button.clicked.connect(self.apply_dilation)
        self.erode_button = QPushButton("Erosion (Aşındırma)")
        self.erode_button.clicked.connect(self.apply_erosion)
        self.centroid_button = QPushButton("Ağırlık Merkezi Hesapla")
        self.centroid_button.clicked.connect(self.show_centroid)
        self.skeleton_button = QPushButton("İskelet Çıkar")
        self.skeleton_button.clicked.connect(self.apply_skeleton)
        self.smooth_button = QPushButton("Yumuşatma Filtresi")
        self.smooth_button.clicked.connect(self.apply_smoothing)
        self.sharpen_button = QPushButton("Keskinleştirme Filtresi")
        self.sharpen_button.clicked.connect(self.apply_sharpening)
        self.rotate_button = QPushButton("90° Döndür")
        self.rotate_button.clicked.connect(self.apply_rotation)
        self.shear_button = QPushButton("X Yönünde Shearing")
        self.shear_button.clicked.connect(self.apply_shearing)
        self.flip_h_button = QPushButton("Yatay Aynalama")
        self.flip_h_button.clicked.connect(self.apply_flip_horizontal)
        self.flip_v_button = QPushButton("Dikey Aynalama")
        self.flip_v_button.clicked.connect(self.apply_flip_vertical)

        # Görselleri yan yana tutan layout
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.original_image_label)
        image_layout.addWidget(self.processed_image_label)

        layout = QVBoxLayout()
        layout.addWidget(self.open_button)
        layout.addLayout(image_layout)
        layout.addWidget(self.mean_button)
        layout.addWidget(self.median_button)
        layout.addWidget(self.edge_button)
        layout.addWidget(self.hist_button)
        layout.addWidget(self.equalize_button)
        layout.addWidget(self.stretch_button)
        layout.addWidget(self.manual_thresh_button)
        layout.addWidget(self.otsu_button)
        layout.addWidget(self.kapur_button)
        layout.addWidget(self.dilate_button)
        layout.addWidget(self.erode_button)
        layout.addWidget(self.centroid_button)
        layout.addWidget(self.skeleton_button)
        layout.addWidget(self.smooth_button)
        layout.addWidget(self.sharpen_button)
        layout.addWidget(self.rotate_button)
        layout.addWidget(self.shear_button)
        layout.addWidget(self.flip_h_button)
        layout.addWidget(self.flip_v_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Görüntü Seç", "", "Image Files (*.png *.jpg *.bmp *.pnm)")
        if path:
            self.original_image = Image.open(path).convert("RGB")
            self.processed_image = None
            self.show_original_image(self.original_image)
            self.processed_image_label.clear()

    def pil_to_pixmap(self, pil_image):
        img = pil_image.convert("RGB")
        data = img.tobytes("raw", "RGB")
        qimage = QImage(data, img.width, img.height, QImage.Format_RGB888)
        return QPixmap.fromImage(qimage)

    def show_original_image(self, pil_image):
        pixmap = self.pil_to_pixmap(pil_image)
        self.original_image_label.setPixmap(pixmap.scaled(
            self.original_image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def show_processed_image(self, pil_image):
        pixmap = self.pil_to_pixmap(pil_image)
        self.processed_image_label.setPixmap(pixmap.scaled(
            self.processed_image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def show_context_menu(self, pos):
        if self.original_image:
            menu = QMenu(self)
            save_action = QAction("Görüntüyü Kaydet", self)
            save_action.triggered.connect(self.save_image)
            menu.addAction(save_action)
            menu.exec_(self.original_image_label.mapToGlobal(pos))

    def save_image(self):
        path, _ = QFileDialog.getSaveFileName(self, "Görüntüyü Kaydet", "", "PNG Files (*.png);;JPG Files (*.jpg)")
        if path:
            image_to_save = self.processed_image if self.processed_image else self.original_image
            if image_to_save:
                image_to_save.save(path)

    # --- Filtre Fonksiyonları ---
    def apply_mean(self):
        if self.original_image:
            gray = self.original_image.convert("L")
            result = apply_mean_filter(np.array(gray))
            img = Image.fromarray(result)
            self.show_processed_image(img)
            self.processed_image = img

    def apply_median(self):
        if self.original_image:
            gray = self.original_image.convert("L")
            result = apply_median_filter(np.array(gray))
            img = Image.fromarray(result)
            self.show_processed_image(img)
            self.processed_image = img

    def apply_edge(self):
        if self.original_image:
            gray = self.original_image.convert("L")
            result = apply_edge_filter(np.array(gray))
            img = Image.fromarray(result)
            self.show_processed_image(img)
            self.processed_image = img

    def show_histogram(self):
        if self.processed_image:
            gray = self.processed_image.convert("L")
        elif self.original_image:
            gray = self.original_image.convert("L")
        else:
            return
        histogram = calculate_histogram(np.array(gray))
        plot_histogram(histogram)

    def equalize_histogram(self):
        img = self.processed_image or self.original_image
        if img:
            gray = img.convert("L")
            result = histogram_equalization(np.array(gray))
            out = Image.fromarray(result)
            self.show_processed_image(out)
            self.processed_image = out

    def stretch_contrast(self):
        img = self.processed_image or self.original_image
        if img:
            gray = img.convert("L")
            result = contrast_stretching(np.array(gray))
            out = Image.fromarray(result)
            self.show_processed_image(out)
            self.processed_image = out

    def apply_manual_threshold(self):
        img = self.processed_image or self.original_image
        if not img:
            return
        gray = img.convert("L")
        value, ok = QInputDialog.getInt(self, "Eşik Değeri", "0–255:", min=0, max=255)
        if ok:
            binary = manual_threshold(np.array(gray), value)
            out = Image.fromarray(binary)
            self.show_processed_image(out)
            self.processed_image = out

    def apply_otsu(self):
        img = self.processed_image or self.original_image
        if img:
            gray = img.convert("L")
            binary = otsu_threshold(np.array(gray))
            out = Image.fromarray(binary)
            self.show_processed_image(out)
            self.processed_image = out

    def apply_kapur(self):
        img = self.processed_image or self.original_image
        if img:
            gray = img.convert("L")
            binary = kapur_threshold(np.array(gray))
            out = Image.fromarray(binary)
            self.show_processed_image(out)
            self.processed_image = out

    def apply_dilation(self):
        if self.processed_image:
            binary = np.array(self.processed_image.convert("L"))
            result = dilation(binary)
            out = Image.fromarray(result)
            self.show_processed_image(out)
            self.processed_image = out

    def apply_erosion(self):
        if self.processed_image:
            binary = np.array(self.processed_image.convert("L"))
            result = erosion(binary)
            out = Image.fromarray(result)
            self.show_processed_image(out)
            self.processed_image = out

    def show_centroid(self):
        if self.processed_image:
            binary = np.array(self.processed_image.convert("L"))
            if not np.array_equal(np.unique(binary), [0, 255]):
                QMessageBox.warning(self, "Uyarı", "İkili görüntü gereklidir.")
                return
            result_img = self.processed_image.convert("RGB")
            centroid = compute_centroid(binary)
            if centroid:
                img = result_img.copy()
                draw = QPainter(QPixmap.fromImage(self.pil_to_pixmap(img).toImage()))
                pen = QPen(Qt.red)
                pen.setWidth(6)
                draw.setPen(pen)
                draw.drawPoint(*centroid)
                draw.end()
                self.show_processed_image(img)

    def apply_skeleton(self):
        if self.processed_image:
            binary = np.array(self.processed_image.convert("L"))
            if not np.array_equal(np.unique(binary), [0, 255]):
                QMessageBox.warning(self, "Uyarı", "İkili görüntü gereklidir.")
                return
            result = skeletonize(binary)
            out = Image.fromarray(result)
            self.show_processed_image(out)
            self.processed_image = out

    def apply_smoothing(self):
        img = self.processed_image or self.original_image
        if img:
            gray = img.convert("L")
            result = apply_smoothing_filter(np.array(gray))
            out = Image.fromarray(result)
            self.show_processed_image(out)
            self.processed_image = out

    def apply_sharpening(self):
        img = self.processed_image or self.original_image
        if img:
            gray = img.convert("L")
            result = apply_sharpen_filter(np.array(gray))
            out = Image.fromarray(result)
            self.show_processed_image(out)
            self.processed_image = out

    def apply_rotation(self):
        img = self.processed_image or self.original_image
        if img:
            out = rotate_image(img, angle_deg=90)
            self.show_processed_image(out)
            self.processed_image = out

    def apply_shearing(self):
        img = self.processed_image or self.original_image
        if img:
            out = shear_image(img, shear_x=0.2, shear_y=0)
            self.show_processed_image(out)
            self.processed_image = out

    def apply_flip_horizontal(self):
        img = self.processed_image or self.original_image
        if img:
            out = flip_horizontal(img)
            self.show_processed_image(out)
            self.processed_image = out

    def apply_flip_vertical(self):
        img = self.processed_image or self.original_image
        if img:
            out = flip_vertical(img)
            self.show_processed_image(out)
            self.processed_image = out

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessor()
    window.show()
    sys.exit(app.exec_())
