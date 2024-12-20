import tkinter as tk
from tkinter import messagebox
import time
import sys
sys.setrecursionlimit(80000)  # Increase the limit to 2000 or higher as needed

# Daftar Stopwords
stopwords = {
    'yang', 'untuk', 'dengan', 'di', 'ke', 'pada', 'adalah', 'itu', 'dan', 'tersebut',
    'saya', 'kami', 'mereka', 'memiliki', 'menjadi', 'menyebabkan', 'menggunakan', 'untuk',
    'seperti', 'mempunyai', 'menulis', 'berada', 'menghadapi', 'belajar', 'setiap',
    'akan', 'sudah', 'sedang', 'dari', 'dalam', 'sebuah', 'hingga' , 'ini' , 'aku', 'hari' ,'kita', 'semoga', 'merasa', 'daerah', 'sangat', 'masyarakat', 'lebih', 'banyak', 'oleh', 'memberikan'
}

# Fungsi rekursif Merge Sort
def merge_sort_rekursif(data):
    if len(data) > 1:
        mid = len(data) // 2
        left_half = data[:mid]
        right_half = data[mid:]

        merge_sort_rekursif(left_half)
        merge_sort_rekursif(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i][1] > right_half[j][1]:
                data[k] = left_half[i]
                i += 1
            else:
                data[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            data[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            data[k] = right_half[j]
            j += 1
            k += 1

    return data

# Fungsi iteratif Selection Sort
def selection_sort_iteratif(data):
    n = len(data)
    for i in range(n):
        max_idx = i
        for j in range(i + 1, n):
            if data[j][1] > data[max_idx][1]:
                max_idx = j
        data[i], data[max_idx] = data[max_idx], data[i]

    return data

# Fungsi iteratif untuk menghitung frekuensi hanya kata yang muncul di lebih dari satu postingan
def hitung_frekuensi_valid_iteratif(postingan_list):
    frekuensi = {}
    for postingan in postingan_list:
        for kata in postingan.lower().split():  # Pecah menjadi kata-kata
            kata = kata.strip('.,!?')  # Bersihkan tanda baca
            if kata and kata not in stopwords:  # Abaikan stopwords dan kata kosong
                if kata not in frekuensi:
                    frekuensi[kata] = 1
                else:
                    frekuensi[kata] += 1
    # Ambil hanya kata yang muncul lebih dari satu kali
    return {kata: jumlah for kata, jumlah in frekuensi.items() if jumlah > 1}

def hitung_frekuensi_valid_rekursif(postingan_list, frekuensi=None):
    # Basis rekursif: jika daftar postingan kosong
    if not postingan_list:
        return {kata: jumlah for kata, jumlah in frekuensi.items() if jumlah > 1}

    # Inisialisasi frekuensi jika kosong
    if frekuensi is None:
        frekuensi = {}

    # Proses postingan pertama
    postingan = postingan_list[0]
    for kata in postingan.lower().split():
        kata = kata.strip('.,!?')  # Bersihkan tanda baca
        if kata and kata not in stopwords:  # Abaikan stopwords dan kata kosong
            frekuensi[kata] = frekuensi.get(kata, 0) + 1

    # Rekursi dengan sisa postingan
    return hitung_frekuensi_valid_rekursif(postingan_list[1:], frekuensi)

# Fungsi utama untuk hitung frekuensi dan sorting
def hitung_waktu_eksekusi(teks, freq_recursive=False, sort_recursive=False):
    postingan_list = [post.strip() for post in teks.split('.') if post.strip()]
    mulai = time.perf_counter()

    # Hitung frekuensi
    if freq_recursive:
        hasil_frekuensi = hitung_frekuensi_valid_rekursif(postingan_list)
    else:
        hasil_frekuensi = hitung_frekuensi_valid_iteratif(postingan_list)

    # Sorting hasil
    data = list(hasil_frekuensi.items())
    if sort_recursive:
        data = merge_sort_rekursif(data)
    else:
        data = selection_sort_iteratif(data)

    selesai = time.perf_counter()
    waktu_eksekusi = (selesai - mulai) * 1_000_000  # Waktu dalam mikrodetik
    return data, len(postingan_list), waktu_eksekusi

# Aplikasi GUI utama dengan menu
class TwitterTrendApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Trend Twitter")
        self.root.geometry("600x500")
        self.root.configure(bg="#1DA1F2")

        self.current_frame = None
        self.input_data = ""
        self.freq_recursive = False
        self.sort_recursive = False
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_frame()

        frame = tk.Frame(self.root, bg="#1DA1F2")
        frame.pack(expand=True, fill="both")

        title = tk.Label(frame, text="Aplikasi Trend Twitter", font=("Arial", 18, "bold"), fg="white", bg="#1DA1F2")
        title.pack(pady=20)

        btn_input = tk.Button(frame, text="Input Data", font=("Arial", 14), bg="black", fg="white", command=self.create_input_menu)
        btn_input.pack(pady=10, ipadx=10, ipady=5)

        btn_options = tk.Button(frame, text="Opsi Analisis", font=("Arial", 14), bg="black", fg="white", command=self.create_option_menu)
        btn_options.pack(pady=10, ipadx=10, ipady=5)

        btn_trending = tk.Button(frame, text="Lihat Trending", font=("Arial", 14), bg="black", fg="white", command=self.create_trending_menu)
        btn_trending.pack(pady=10, ipadx=10, ipady=5)

        self.current_frame = frame

    def create_input_menu(self):
        self.clear_frame()

        frame = tk.Frame(self.root, bg="#1DA1F2")
        frame.pack(expand=True, fill="both")

        label = tk.Label(frame, text="Masukkan Data Postingan:", font=("Arial", 14, "bold"), fg="white", bg="#1DA1F2")
        label.pack(pady=10)

        self.input_text = tk.Text(frame, height=10, width=50, font=("Arial", 12), bg="white", fg="black")
        self.input_text.pack(pady=10)

        btn_save = tk.Button(frame, text="Simpan Data", font=("Arial", 12), bg="black", fg="white", command=self.save_input_data)
        btn_save.pack(pady=10, ipadx=10, ipady=5)

        btn_back = tk.Button(frame, text="Kembali", font=("Arial", 12), bg="black", fg="white", command=self.create_main_menu)
        btn_back.pack(pady=10, ipadx=10, ipady=5)

        self.current_frame = frame

    def save_input_data(self):
        self.input_data = self.input_text.get("1.0", tk.END).strip()
        messagebox.showinfo("Info", "Data berhasil disimpan!")

    def create_option_menu(self):
        self.clear_frame()

        frame = tk.Frame(self.root, bg="#1DA1F2")
        frame.pack(expand=True, fill="both")

        label = tk.Label(frame, text="Pilih Metode Analisis:", font=("Arial", 14, "bold"), fg="white", bg="#1DA1F2")
        label.pack(pady=10)

        self.freq_var = tk.IntVar(value=0)
        self.sort_var = tk.IntVar(value=0)

        freq_label = tk.Label(frame, text="Metode Frekuensi:", font=("Arial", 12), fg="white", bg="#1DA1F2")
        freq_label.pack(anchor="w", padx=20)

        tk.Radiobutton(frame, text="Iteratif", variable=self.freq_var, value=0, font=("Arial", 12), bg="#1DA1F2", fg="black", selectcolor="#1DA1F2").pack(anchor="w", padx=40)
        tk.Radiobutton(frame, text="Rekursif", variable=self.freq_var, value=1, font=("Arial", 12), bg="#1DA1F2", fg="black", selectcolor="#1DA1F2").pack(anchor="w", padx=40)

        sort_label = tk.Label(frame, text="Metode Sorting:", font=("Arial", 12), fg="white", bg="#1DA1F2")
        sort_label.pack(anchor="w", padx=20)

        tk.Radiobutton(frame, text="Iteratif", variable=self.sort_var, value=0, font=("Arial", 12), bg="#1DA1F2", fg="black", selectcolor="#1DA1F2").pack(anchor="w", padx=40)
        tk.Radiobutton(frame, text="Rekursif", variable=self.sort_var, value=1, font=("Arial", 12), bg="#1DA1F2", fg="black", selectcolor="#1DA1F2").pack(anchor="w", padx=40)

        btn_save = tk.Button(frame, text="Simpan Opsi", font=("Arial", 12), bg="black", fg="white", command=self.save_options)
        btn_save.pack(pady=10, ipadx=10, ipady=5)

        btn_back = tk.Button(frame, text="Kembali", font=("Arial", 12), bg="black", fg="white", command=self.create_main_menu)
        btn_back.pack(pady=20, ipadx=10, ipady=5)

        self.current_frame = frame

    def save_options(self):
        self.freq_recursive = self.freq_var.get() == 1
        self.sort_recursive = self.sort_var.get() == 1
        messagebox.showinfo("Info", "Opsi berhasil disimpan!")

    def create_trending_menu(self):
        self.clear_frame()

        frame = tk.Frame(self.root, bg="#1DA1F2")
        frame.pack(expand=True, fill="both")

        label = tk.Label(frame, text="Hasil Trending:", font=("Arial", 14, "bold"), fg="white", bg="#1DA1F2")
        label.pack(pady=10)

        self.output_text = tk.Text(frame, height=15, width=50, font=("Arial", 12), bg="white", fg="black")
        self.output_text.pack(pady=10)

        if self.input_data:
            data, jumlah_postingan, waktu = hitung_waktu_eksekusi(self.input_data, self.freq_recursive, self.sort_recursive)
            data = data[:10]  # Batasi hasil menjadi 10 trending teratas
            hasil = f"Jumlah Postingan: {jumlah_postingan}\nWaktu Eksekusi: {waktu:.2f} mikrodetik\n\n"
            hasil += "\n".join([f"{kata}: {jumlah}" for kata, jumlah in data])
            self.output_text.insert("1.0", hasil)
        else:
            self.output_text.insert("1.0", "Tidak ada data untuk dianalisis.")

        btn_back = tk.Button(frame, text="Kembali", font=("Arial", 12), bg="black", fg="white", command=self.create_main_menu)
        btn_back.pack(pady=20, ipadx=10, ipady=5)

        self.current_frame = frame

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

# Menjalankan aplikasi
root = tk.Tk()
app = TwitterTrendApp(root)
root.mainloop()
