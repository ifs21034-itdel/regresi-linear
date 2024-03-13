from tkinter import *
from tkinter import messagebox
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

root = Tk()
root.title("Prediksi Harga Penjualan Rumah")
root.geometry("400x350")

# Fungsi untuk memprediksi harga penjualan rumah
def predict_price():
    # Memuat dataset
    try:
        data = pd.read_csv("Rumah.csv")
    except FileNotFoundError:
        messagebox.showerror("Error", "File dataset tidak ditemukan")
        return

    # Memeriksa apakah kolom yang diperlukan ada di dataset
    required_columns = ['bedrooms', 'bathrooms', 'sqft_living', 'price']
    if not all(col in data.columns for col in required_columns):
        messagebox.showerror("Error", "Kolom yang diperlukan tidak ditemukan dalam dataset")
        return

    # Memeriksa apakah ada nilai yang hilang dalam dataset
    if data[required_columns].isnull().values.any():
        messagebox.showerror("Error", "Dataset berisi nilai yang hilang")
        return

    # Mendapatkan fitur dari input pengguna
    try:
        bedrooms = float(entry_bedroom.get())
        bathrooms = float(entry_bathroom.get())
        sqft_living = float(entry_sqft_living.get())
    except ValueError:
        messagebox.showerror("Error", "Masukkan angka yang valid untuk fitur-fitur rumah")
        return

    # Melatih model regresi linear
    X = data[['bedrooms', 'bathrooms', 'sqft_living']]
    y = data['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Melakukan prediksi harga
    predicted_price = model.predict([[bedrooms, bathrooms, sqft_living]])

    # Menampilkan hasil prediksi kepada pengguna
    messagebox.showinfo("Hasil Prediksi", f"Harga prediksi rumah: ${predicted_price[0]:,.2f}")

# Label
label_bedroom = Label(root, text="Jumlah Kamar Tidur:")
label_bedroom.grid(row=0, column=0, padx=10, pady=5)
label_bathroom = Label(root, text="Jumlah Kamar Mandi:")
label_bathroom.grid(row=1, column=0, padx=10, pady=5)
label_sqft_living = Label(root, text="Luas Ruang (sqft):")
label_sqft_living.grid(row=2, column=0, padx=10, pady=5)

# Entry widgets
entry_bedroom = Entry(root)
entry_bedroom.grid(row=0, column=1, padx=10, pady=5)
entry_bathroom = Entry(root)
entry_bathroom.grid(row=1, column=1, padx=10, pady=5)
entry_sqft_living = Entry(root)
entry_sqft_living.grid(row=2, column=1, padx=10, pady=5)

# Tombol Prediksi
button_predict = Button(root, text="Prediksi Harga", command=predict_price)
button_predict.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

root.mainloop()
