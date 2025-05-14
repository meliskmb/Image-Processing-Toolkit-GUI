# Görüntü İşleme Uygulaması (Image Processing Toolkit GUI)

Bu proje, **PyQt5** ile geliştirilen, temel görüntü işleme işlemlerini kullanıcı dostu bir masaüstü uygulamasıdır. Arayüzde orijinal ve işlenmiş görseller alt alta gösterilir; işlem grupları kategorilere ayrılmıştır ve scroll desteklidir.

---

## Proje Özeti

- Dönem: 2024–2025 Eğitim Yılı, Görüntü İşleme Dönem Projesi
- Teknolojiler: Python, PyQt5, Pillow (PIL), NumPy, Matplotlib
- Amaç: Görseller üzerinde temel işleme fonksiyonlarının uygulanmasını kolaylaştıran bir arayüz geliştirmek.

## Arayüz Özellikleri

-  **İkili Görsel Panel:**  
  Sol panelde orijinal ve işlenmiş görüntü alt alta gösterilir.
  
-  **Kategorilere Ayrılmış Butonlar:**  
  Filtreleme, Histogram, Eşikleme, Morfolojik, Geometrik, Centroid & Skeleton ve Genel işlemler ayrı gruplarda sunulur.

-  **Kaydırma Alanı (Scroll):**  
  Tüm butonlar gruplar halinde dikey olarak yerleştirilmiştir ve scroll alanıyla erişilebilir.

-  **Geri Al (Undo) Özelliği:**  
  Yapılan işlemler geri alınabilir.

-  **Değişiklikleri Kaydet Butonu:**  
  İşlenmiş görseli orijinal gibi tanımlayarak yeni işlemlere sıfırdan başlamayı sağlar.

-  **İşlem Sonrası Kayıt:**  
  İşlenmiş görsel sağ tıklanarak istenilen formata kayıt edilebilir.

##  Özellik Listesi

###  Genel
- Görüntü Aç
- Geri Al
- Değişikliği Kaydet
- Sağ tıklayarak görüntü kaydetme (işlenmiş)

###  Filtreler
- Ortalama Filtresi
- Ortanca Filtresi
- Kenar Tespiti
- Yumuşatma Filtresi
- Keskinleştirme Filtresi

###  Histogram
- Histogram Göster
- Histogram Eşitleme
- Kontrast Germe

###  Eşikleme
- Manuel Eşikleme
- Otsu Eşikleme
- Kapur Eşikleme

###  Morfolojik İşlemler
- Dilation (Genişletme)
- Erosion (Aşındırma)

###  Geometrik İşlemler
- 90° Döndürme
- Shearing (X yönlü)
- Yatay / Dikey Aynalama

###  Diğer
- Ağırlık Merkezi Hesaplama (ikili görüntüde)
- İskelet Çıkarma

##  Kurulum ve Kullanım

### Gerekli Kütüphaneler:

```bash
pip install pyqt5 numpy pillow matplotlib
```

### Çalıştırmak için

```bash
python main.py
```

##  Proje Yapısı

```css
Image-Processing-Toolkit-GUI/
├── main.py
├── filters/
│   ├── convolution.py
│   ├── histogram.py
│   ├── morphology.py
│   ├── geometry.py
│   └── thresholding.py
└── README.md
```

### Notlar
- Arayüz ekran çözünürlüğüne duyarlıdır, scroll ile tam kontrol sağlanır.
- Uygulama yalnızca .png, .jpg, .bmp gibi standart görsel formatlarını destekler.
- Tüm filtre ve dönüşümler kendi fonksiyonlarınla yapılmıştır; OpenCV gibi hazır fonksiyonlar kullanılmamıştır.

---

### Geliştirici Notu
Bu proje hem görüntü işleme temellerini hem de GUI tasarımı becerilerini geliştirmek amacıyla sıfırdan yazılmıştır.