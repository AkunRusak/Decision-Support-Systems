import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import pandas as pd

class AHPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AHP - Pemilihan Lokasi Bisnis")
        self.root.geometry("600x400")

        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Upload File", command=self.upload_file)
        self.file_menu.add_command(label="Save File", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

        self.label = tk.Label(root, text="Analytic Hierarchy Process (AHP) - Pemilihan Lokasi Bisnis", font=("Arial", 14))
        self.label.pack(pady=10)

        self.text_area = tk.Text(root, height=15, width=70)
        self.text_area.pack(pady=10)

        self.result_label = tk.Label(root, text="Hasil AHP akan ditampilkan di sini", font=("Arial", 12))
        self.result_label.pack(pady=10)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            try:
                self.df = pd.read_excel(file_path)
                self.text_area.insert(tk.END, "File berhasil diupload:\n")
                self.text_area.insert(tk.END, self.df.to_string())
                self.calculate_ahp()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal membaca file: {e}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.text_area.get("1.0", tk.END))
                messagebox.showinfo("Info", "File berhasil disimpan")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan file: {e}")

    def calculate_ahp(self):
        try:
            # Contoh perhitungan AHP sederhana
            criteria = self.df.columns[1:]
            alternatives = self.df.iloc[:, 0]
            matrix = self.df.iloc[:, 1:].values

            # Normalisasi matriks
            norm_matrix = matrix / matrix.sum(axis=0)

            # Hitung bobot kriteria
            weights = norm_matrix.mean(axis=1)

            # Hitung skor akhir
            scores = np.dot(matrix, weights)

            # Tampilkan hasil
            result = "\nHasil AHP:\n"
            for alt, score in zip(alternatives, scores):
                result += f"{alt}: {score:.4f}\n"
            self.result_label.config(text=result)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menghitung AHP: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AHPApp(root)
    root.mainloop()
