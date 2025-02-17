import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QImage

class ImageEnhancer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.image = None
    
    def initUI(self):
        self.setWindowTitle("Amélioration d'Images Nocturnes")
        self.setGeometry(100, 100, 600, 400)
        
        self.label = QLabel(self)
        self.label.setText("Aucune image chargée")
        
        self.btnLoad = QPushButton("Charger Image", self)
        self.btnLoad.clicked.connect(self.loadImage)
        
        self.btnEnhance = QPushButton("Améliorer", self)
        self.btnEnhance.clicked.connect(self.enhanceImage)
        self.btnEnhance.setEnabled(False)
        
        self.btnSave = QPushButton("Enregistrer", self)
        self.btnSave.clicked.connect(self.saveImage)
        self.btnSave.setEnabled(False)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btnLoad)
        layout.addWidget(self.btnEnhance)
        layout.addWidget(self.btnSave)
        self.setLayout(layout)
    
    def loadImage(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Ouvrir une image", "", "Images (*.png *.xpm *.jpg *.bmp)")
        if filePath:
            self.image = cv2.imread(filePath)
            self.displayImage()
            self.btnEnhance.setEnabled(True)
    
    def displayImage(self):
        if self.image is not None:
            imageRGB = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            height, width, channel = imageRGB.shape
            bytesPerLine = 3 * width
            qImg = QImage(imageRGB.data, width, height, bytesPerLine, QImage.Format.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(qImg).scaled(500, 400))
    
    def enhanceImage(self):
        if self.image is not None:
            lab = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            l = clahe.apply(l)
            enhanced_lab = cv2.merge((l, a, b))
            self.image = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
            self.displayImage()
            self.btnSave.setEnabled(True)
    
    def saveImage(self):
        if self.image is not None:
            filePath, _ = QFileDialog.getSaveFileName(self, "Enregistrer l'image", "", "Images (*.png *.jpg *.bmp)")
            if filePath:
                cv2.imwrite(filePath, self.image)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageEnhancer()
    window.show()
    sys.exit(app.exec())
