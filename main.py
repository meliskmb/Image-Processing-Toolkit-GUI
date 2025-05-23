import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton,
    QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QMenu, QAction, QMessageBox
)
from PyQt5.QtWidgets import QInputDialog, QGroupBox, QScrollArea
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QTimer
import numpy as np
from PIL import Image

from filters.convolution import apply_mean_filter, apply_median_filter, apply_edge_filter, apply_smoothing_filter, apply_sharpen_filter
from filters.histogram import calculate_histogram, plot_histogram, histogram_equalization, contrast_stretching
from filters.thresholding import manual_threshold, otsu_threshold, kapur_threshold
from filters.morphology import dilation, erosion
from filters.geometry import compute_centroid, skeletonize, rotate_image, shear_image, flip_horizontal, flip_vertical

#TO-DO: geri al ve kaydet ekle

class ImageProcessor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Görüntü İşleme Uygulaması")
        self.setGeometry(100, 100, 800, 600)

        self.original_image = None
        self.processed_image = None
        self.history_stack = []

        self.original_image_label = QLabel("Orijinal Görüntü", self)
        self.original_image_label.setAlignment(Qt.AlignCenter)

        self.processed_image_label = QLabel("İşlenmiş Görüntü", self)
        self.processed_image_label.setAlignment(Qt.AlignCenter)

        self.processed_image_label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.processed_image_label.customContextMenuRequested.connect(self.show_context_menu_processed)

        self.flash_label = QLabel("")
        self.flash_label.setStyleSheet("color: green; font-weight: bold;")
        self.flash_label.setAlignment(Qt.AlignCenter)
        self.flash_label.hide()

        # Butonlar
        self.open_button = QPushButton("Görüntü Aç")
        self.open_button.clicked.connect(self.load_image)
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
        self.undo_button = QPushButton("Geri Al")
        self.undo_button.clicked.connect(self.undo_last_operation)
        self.commit_button = QPushButton("Değişikliği Kaydet")
        self.commit_button.clicked.connect(self.commit_changes)

        image_column = QVBoxLayout()
        image_column.addWidget(self.original_image_label)
        image_column.addWidget(self.processed_image_label)

        filter_group = QGroupBox("Filtreler")
        filter_layout = QVBoxLayout()
        filter_layout.addWidget(self.mean_button)
        filter_layout.addWidget(self.median_button)
        filter_layout.addWidget(self.edge_button)
        filter_layout.addWidget(self.smooth_button)
        filter_layout.addWidget(self.sharpen_button)
        filter_group.setLayout(filter_layout)

        hist_group = QGroupBox("Histogram")
        hist_layout = QVBoxLayout()
        hist_layout.addWidget(self.hist_button)
        hist_layout.addWidget(self.equalize_button)
        hist_layout.addWidget(self.stretch_button)
        hist_group.setLayout(hist_layout)

        thresh_group = QGroupBox("Eşikleme")
        thresh_layout = QVBoxLayout()
        thresh_layout.addWidget(self.manual_thresh_button)
        thresh_layout.addWidget(self.otsu_button)
        thresh_layout.addWidget(self.kapur_button)
        thresh_group.setLayout(thresh_layout)

        morph_group = QGroupBox("Morfolojik")
        morph_layout = QVBoxLayout()
        morph_layout.addWidget(self.dilate_button)
        morph_layout.addWidget(self.erode_button)
        morph_group.setLayout(morph_layout)

        geom_group = QGroupBox("Geometrik")
        geom_layout = QVBoxLayout()
        geom_layout.addWidget(self.rotate_button)
        geom_layout.addWidget(self.shear_button)
        geom_layout.addWidget(self.flip_h_button)
        geom_layout.addWidget(self.flip_v_button)
        geom_group.setLayout(geom_layout)

        censke_group = QGroupBox("centroid & skeleton")
        censke_layout = QVBoxLayout()
        censke_layout.addWidget(self.centroid_button)
        censke_layout.addWidget(self.skeleton_button)
        censke_group.setLayout(censke_layout)

        control_group = QGroupBox("Genel")
        control_layout = QVBoxLayout()
        control_layout.addWidget(self.open_button)
        control_layout.addWidget(self.undo_button)
        control_layout.addWidget(self.commit_button)
        control_layout.addWidget(self.flash_label)
        control_group.setLayout(control_layout)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.addWidget(control_group)
        scroll_layout.addWidget(filter_group)
        scroll_layout.addWidget(hist_group)
        scroll_layout.addWidget(thresh_group)
        scroll_layout.addWidget(morph_group)
        scroll_layout.addWidget(geom_group)
        scroll_layout.addWidget(censke_group)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_content)

        main_layout = QHBoxLayout()
        main_layout.addLayout(image_column, 3)  
        main_layout.addWidget(scroll_area, 2)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.setStyleSheet("""
            QWidget {
                background-color: #F5EBE0;  /* Daha sıcak, açık bej ton */
                font-family: 'Segoe UI', sans-serif;    
            }

            QGroupBox {
                background-color: #D6CCC2;
                border: 1px solid #D5BDAF;
                border-radius: 8px;
                margin-top: 10px;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 4px;
                color: #5A4A42;
                font-weight: bold;
                font-size: 12pt;
            }

            QPushButton {
                background-color: #F5EBE0;
                border: 1px solid #D5BDAF;
                border-radius: 6px;
                padding: 6px 12px;
                color: #3E3E3E;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #E3D5CA;
            }

            QLabel {
                color: #4A4A4A;
                font-weight: 600;
            }

            QScrollArea {
                background-color: transparent;
            }
        """)



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


    def show_context_menu_processed(self, pos):
        if self.processed_image:
            menu = QMenu(self)
            save_action = QAction("Görüntüyü Kaydet", self)
            save_action.triggered.connect(self.save_processed_image)
            menu.addAction(save_action)
            menu.exec_(self.processed_image_label.mapToGlobal(pos))


    def save_processed_image(self):
        path, _ = QFileDialog.getSaveFileName(self, "Görüntüyü Kaydet", "", "PNG Files (*.png);;JPG Files (*.jpg)")
        if path and self.processed_image:
            self.processed_image.save(path)


    def apply_mean(self):
        if self.original_image:
            gray = self.original_image.convert("L")
            result = apply_mean_filter(np.array(gray))
            img = Image.fromarray(result)
            self.show_processed_image(img)
            self.history_stack.append(self.processed_image.copy() if self.processed_image else self.original_image.copy())
            self.processed_image = img

    def apply_median(self):
        if self.original_image:
            gray = self.original_image.convert("L")
            result = apply_median_filter(np.array(gray))
            img = Image.fromarray(result)
            self.show_processed_image(img)
            self.history_stack.append(self.processed_image.copy() if self.processed_image else self.original_image.copy())
            self.processed_image = img

    def apply_edge(self):
        if self.original_image:
            gray = self.original_image.convert("L")
            result = apply_edge_filter(np.array(gray))
            img = Image.fromarray(result)
            self.show_processed_image(img)
            self.history_stack.append(self.processed_image.copy() if self.processed_image else self.original_image.copy())
            self.processed_image = img

    def show_histogram(self):
        if not self.original_image:
            return
       
        gray = self.original_image.convert("L")
        histogram = calculate_histogram(np.array(gray))
        plot_histogram(histogram)

    def equalize_histogram(self):
        if not self.original_image:
            return
        
        gray = self.original_image.convert("L")
        result = histogram_equalization(np.array(gray))
        out = Image.fromarray(result)
        self.show_processed_image(out)
        self.history_stack.append(self.processed_image.copy() if self.processed_image else self.original_image.copy())
        self.processed_image = out

    def stretch_contrast(self):
        if not self.original_image:
            return

        gray = self.original_image.convert("L")
        result = contrast_stretching(np.array(gray))
        out = Image.fromarray(result)
        self.show_processed_image(out)
        self.history_stack.append(self.processed_image.copy() if self.processed_image else self.original_image.copy())
        self.processed_image = out

    def apply_manual_threshold(self):
        if not self.original_image:
            return

        gray = self.original_image.convert("L")
        value, ok = QInputDialog.getInt(self, "Eşik Değeri", "0–255:", min=0, max=255)
        if ok:
            binary = manual_threshold(np.array(gray), value)
            out = Image.fromarray(binary)
            self.show_processed_image(out)
            self.history_stack.append(self.processed_image.copy() if self.processed_image else self.original_image.copy())
            self.processed_image = out

    def apply_otsu(self):
        if not self.original_image:
            return

        gray = self.original_image.convert("L")
        binary = otsu_threshold(np.array(gray))
        out = Image.fromarray(binary)
        self.show_processed_image(out)
        self.history_stack.append(self.processed_image.copy() if self.processed_image else self.original_image.copy())
        self.processed_image = out

    def apply_kapur(self):
        if not self.original_image:
            return
        
        gray = self.original_image.convert("L")
        binary = kapur_threshold(np.array(gray))
        out = Image.fromarray(binary)
        self.show_processed_image(out)
        self.history_stack.append(self.processed_image.copy() if self.processed_image else self.original_image.copy())
        self.processed_image = out

    def apply_dilation(self):
        if not self.original_image:
            return
        
        binary = np.array(self.original_image.convert("L"))
        result = dilation(binary)
        out = Image.fromarray(result)
        self.show_processed_image(out)
        self.history_stack.append(self.processed_image.copy() if self.processed_image else self.original_image.copy())
        self.processed_image = out

    def apply_erosion(self):
        if not self.original_image:
            return
        
        binary = np.array(self.original_image.convert("L"))
        result = erosion(binary)
        out = Image.fromarray(result)
        self.show_processed_image(out)
        self.history_stack.append(self.processed_image.copy() if self.processed_image else self.original_image.copy())
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
                pixmap = QPixmap.fromImage(self.pil_to_pixmap(img).toImage())
                painter = QPainter()
                painter.begin(pixmap)
                pen = QPen(Qt.red)
                pen.setWidth(6)
                painter.setPen(pen)
                painter.drawPoint(*centroid)
                painter.end()
                self.processed_image_label.setPixmap(pixmap.scaled(self.processed_image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.processed_image = img

    def apply_skeleton(self):
        if self.processed_image:
            binary = np.array(self.processed_image.convert("L"))
            if not np.array_equal(np.unique(binary), [0, 255]):
                QMessageBox.warning(self, "Uyarı", "İkili görüntü gereklidir.")
                return
            result = skeletonize(binary)
            out = Image.fromarray(result)
            self.show_processed_image(out)
            self.history_stack.append(self.processed_image.copy() if self.processed_image else self.original_image.copy())
            self.processed_image = out

    def apply_smoothing(self):
        if not self.original_image:
            return
          
        gray = self.original_image.convert("L")
        result = apply_smoothing_filter(np.array(gray))
        out = Image.fromarray(result)
        self.show_processed_image(out)
        self.history_stack.append(self.processed_image.copy() if self.processed_image else self.original_image.copy())
        self.processed_image = out

    def apply_sharpening(self):
        if not self.original_image:
            return
        
        gray = self.original_image.convert("L")
        result = apply_sharpen_filter(np.array(gray))
        out = Image.fromarray(result)
        self.show_processed_image(out)
        self.history_stack.append(self.processed_image.copy() if self.processed_image else self.original_image.copy())
        self.processed_image = out

    def apply_rotation(self):
        img = self.processed_image or self.original_image
        if img:
            out = rotate_image(img, angle_deg=90)
            self.show_processed_image(out)
            self.history_stack.append(self.processed_image.copy() if self.processed_image else self.original_image.copy())
            self.processed_image = out

    def apply_shearing(self):
        if not self.original_image:
            return
        
        out = shear_image(self.original_image, shear_x=0.2, shear_y=0)
        self.show_processed_image(out)
        self.history_stack.append(self.processed_image.copy() if self.processed_image else self.original_image.copy())
        self.processed_image = out

    def apply_flip_horizontal(self):
        img = self.processed_image or self.original_image
        if img:
            out = flip_horizontal(img)
            self.show_processed_image(out)
            self.history_stack.append(self.processed_image.copy() if self.processed_image else self.original_image.copy())
            self.processed_image = out

    def apply_flip_vertical(self):
        img = self.processed_image or self.original_image
        if img:
            out = flip_vertical(img)
            self.show_processed_image(out)
            self.history_stack.append(self.processed_image.copy() if self.processed_image else self.original_image.copy())
            self.processed_image = out

    def undo_last_operation(self):
        if self.history_stack:
            last_image = self.history_stack.pop()
            self.processed_image = last_image
            self.show_processed_image(last_image)
        else:
            QMessageBox.information(self, "Geri Al", "Geri alınacak işlem yok.")

    def commit_changes(self):
        if self.processed_image:
            self.original_image = self.processed_image.copy()
            self.show_flash_message("Değişiklik kaydedildi.")

    def show_flash_message(self, message, duration=2000): 
        self.flash_label.setText(message)
        self.flash_label.show()
        QTimer.singleShot(duration, self.flash_label.hide)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessor()
    window.show()
    sys.exit(app.exec_())
