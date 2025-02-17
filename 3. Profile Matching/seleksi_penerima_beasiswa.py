import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QFileDialog, QLineEdit, QHBoxLayout

class BeasiswaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Profile Matching - Seleksi Beasiswa")
        self.setGeometry(100, 100, 600, 500)
        
        layout = QVBoxLayout()
        
        self.label = QLabel("Masukkan Data Kandidat:")
        layout.addWidget(self.label)
        
        form_layout = QHBoxLayout()
        self.nama_input = QLineEdit()
        self.nama_input.setPlaceholderText("Nama")
        form_layout.addWidget(self.nama_input)
        
        self.akademik_input = QLineEdit()
        self.akademik_input.setPlaceholderText("Akademik")
        form_layout.addWidget(self.akademik_input)
        
        self.ekonomi_input = QLineEdit()
        self.ekonomi_input.setPlaceholderText("Ekonomi")
        form_layout.addWidget(self.ekonomi_input)
        
        self.kepribadian_input = QLineEdit()
        self.kepribadian_input.setPlaceholderText("Kepribadian")
        form_layout.addWidget(self.kepribadian_input)
        
        self.btn_tambah = QPushButton("Tambah Kandidat")
        self.btn_tambah.clicked.connect(self.tambah_kandidat)
        form_layout.addWidget(self.btn_tambah)
        
        layout.addLayout(form_layout)
        
        self.label_hasil = QLabel("Hasil Seleksi Beasiswa:")
        layout.addWidget(self.label_hasil)
        
        self.table = QTableWidget()
        layout.addWidget(self.table)
        
        self.btn_proses = QPushButton("Proses Seleksi")
        self.btn_proses.clicked.connect(self.proses_seleksi)
        layout.addWidget(self.btn_proses)
        
        self.btn_simpan = QPushButton("Simpan ke Excel")
        self.btn_simpan.clicked.connect(self.simpan_excel)
        layout.addWidget(self.btn_simpan)
        
        self.setLayout(layout)
        
        self.kandidat_list = []
    
    def tambah_kandidat(self):
        nama = self.nama_input.text()
        akademik = self.akademik_input.text()
        ekonomi = self.ekonomi_input.text()
        kepribadian = self.kepribadian_input.text()
        
        if nama and akademik and ekonomi and kepribadian:
            self.kandidat_list.append({
                "Nama": nama,
                "Akademik": int(akademik),
                "Ekonomi": int(ekonomi),
                "Kepribadian": int(kepribadian)
            })
        
        self.nama_input.clear()
        self.akademik_input.clear()
        self.ekonomi_input.clear()
        self.kepribadian_input.clear()
    
    def proses_seleksi(self):
        if not self.kandidat_list:
            return
        
        df = pd.DataFrame(self.kandidat_list)
        df["Total Skor"] = df[["Akademik", "Ekonomi", "Kepribadian"]].mean(axis=1)
        df = df.sort_values(by="Total Skor", ascending=False)
        df["Ranking"] = range(1, len(df) + 1)
        
        self.tampilkan_hasil(df)
    
    def tampilkan_hasil(self, df):
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)
        
        for row_idx, row_data in df.iterrows():
            for col_idx, value in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
    
    def simpan_excel(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Simpan File", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_name:
            data = []
            for row in range(self.table.rowCount()):
                data.append([self.table.item(row, col).text() for col in range(self.table.columnCount())])
            df = pd.DataFrame(data, columns=[self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())])
            df.to_excel(file_name, index=False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BeasiswaApp()
    window.show()
    sys.exit(app.exec_())
