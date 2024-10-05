import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv('hour.csv')  

# Title dan Deskripsi
st.title("Bike Sharing Dashboard - Overview")
st.write("Ini adalah bagian overview dari analisis penggunaan sepeda berdasarkan dataset Bike Sharing.")

# Menentukan batas outlier menggunakan IQR (Interquartile Range)
Q1 = df['cnt'].quantile(0.25)
Q3 = df['cnt'].quantile(0.75)
IQR = Q3 - Q1

# Mendefinisikan batas bawah dan batas atas untuk outlier
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Menghapus data yang termasuk outlier berdasarkan batas IQR
df = df[(df['cnt'] >= lower_bound) & (df['cnt'] <= upper_bound)]

# Section 1: Total Pengguna Sepeda
st.header("Total Pengguna Sepeda")
total_pengguna = df['cnt'].sum()  # Total semua penggunaan sepeda
st.metric(label="Total Penggunaan Sepeda 2011 - 2012", value=f"{total_pengguna:,}")

# Section 2: Distribusi Pengguna Berdasarkan Waktu Hari (Morning, Afternoon, Evening)
st.header("Distribusi Penggunaan Berdasarkan Jam")

# Menambahkan kolom baru 'time_of_day' untuk mengelompokkan waktu dalam hari (pagi, siang, malam)
def assign_time_of_day(hr):
    if 6 <= hr < 12:
        return '06.00 - 11.59'
    elif 12 <= hr < 18:
        return '12.00 - 17.59'
    elif 18 <= hr <= 23:
        return '18.00 - 23.59'
    else:
        return '00.00 - 05.59'

df['time_of_day'] = df['hr'].apply(assign_time_of_day)

# Visualisasi penggunaan sepeda berdasarkan waktu dalam hari menggunakan Streamlit chart
time_of_day_group = df.groupby('time_of_day')['cnt'].mean().reset_index()
st.bar_chart(time_of_day_group.set_index('time_of_day'))
st.write("Dari grafik terlihat jelas bahwa penggunaan sepeda paling tinggi terjadi pada siang hingga sore hari. Ini menunjukkan bahwa banyak orang memanfaatkan layanan bike sharing untuk kegiatan seperti bekerja, sekolah, atau rekreasi pada waktu-waktu tersebut.")

# Section 3: Trend Penggunaan Sepeda per Musim
st.header("Trend Penggunaan Sepeda berdasarkan musim")


# Mengonversi kolom 'season' menjadi deskripsi yang lebih mudah dipahami
df['season_desc'] = df['season'].replace({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

# Plot trend penggunaan sepeda berdasarkan musim
seasonal_trend = df.groupby('season_desc')['cnt'].mean()

st.line_chart(seasonal_trend)
st.write("Data menunjukkan bahwa musim gugur merupakan musim dengan tingkat penggunaan layanan bike sharing tertinggi. Kondisi cuaca yang sejuk dan cerah pada musim gugur, serta adanya event atau kampanye terkait sepeda, mungkin menjadi beberapa faktor yang berkontribusi terhadap peningkatan penggunaan sepeda pada periode tersebut.")

# Section 4: Visualisasi Klustering Pengguna Berdasarkan Cuaca
st.header("Visualisasi Klustering Pengguna Berdasarkan Cuaca")

# Mengonversi kolom 'weathersit' menjadi deskripsi yang lebih mudah dipahami
df['weathersit_desc'] = df['weathersit'].replace({1: 'Clear', 2: 'Mist', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'})

# Mengelompokkan pengguna berdasarkan cuaca
weather_group = df.groupby('weathersit_desc')['cnt'].mean()
st.bar_chart(weather_group)

st.write("Dari grafik tersebut, dapat disimpulkan bahwa cuaca memiliki pengaruh yang sangat besar terhadap minat masyarakat untuk menggunakan layanan berbagi sepeda. Cuaca cerah menjadi faktor pendorong utama, sementara cuaca buruk menjadi penghalang. Hasil ini sejalan dengan intuisi umum bahwa kondisi cuaca yang baik akan mendorong lebih banyak orang untuk beraktivitas di luar ruangan, termasuk bersepeda.")