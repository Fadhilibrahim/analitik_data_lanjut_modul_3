import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Judul aplikasi
st.title('Streamlit Simple App')

# Menambahkan navigasi di sidebar
page = st.sidebar.radio("Pilih halaman", ["Dataset", "Visualisasi"])

if page == "Dataset":
    st.header("Halaman Dataset")

    # Baca file CSV
    try:
        # Pastikan path sesuai dengan lokasi file yang benar
        data = pd.read_csv("D:/FADHIL/DAL Streamlit/app/pddikti_example.csv.csv")  
        
        # Tampilkan data di Streamlit
        st.write(data)
    except FileNotFoundError:
        st.error("File 'pddikti_example.csv.csv' tidak ditemukan. Pastikan file ada di lokasi yang benar.")
    except Exception as e:
        st.error(f"Terjadi error saat membaca file: {e}")

elif page == "Visualisasi":
    st.header("Halaman Visualisasi")
    st.write("Visualisasi data akan ditampilkan di sini.")

# Baca file CSV
data = pd.read_csv("D:/FADHIL/DAL Streamlit/app/pddikti_example.csv.csv")  # Pastikan path benar

# Pilih Universitas menggunakan selectbox
selected_university = st.selectbox('Pilih Universitas', data['universitas'].unique())

# Filter data berdasarkan universitas yang dipilih
filtered_data = data[data['universitas'] == selected_university]

# Buat figure dan axis baru untuk visualisasi
fig, ax = plt.subplots(figsize=(12, 6))

# Loop untuk setiap program studi
for prog_studi in filtered_data['program_studi'].unique():
    subset = filtered_data[filtered_data['program_studi'] == prog_studi]
    subset = subset.sort_values(by='id', ascending=False)

    ax.plot(subset['semester'], subset['jumlah'], label=prog_studi)

# Menambahkan judul dan label sumbu
ax.set_title(f"Visualisasi Data untuk {selected_university}")
ax.set_xlabel('Semester')
ax.set_ylabel('Jumlah')
ax.legend()

# Rotasi label sumbu x
plt.xticks(rotation=90)

# Tampilkan figure di Streamlit
st.pyplot(fig)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='csv_db 6'
    )
    return connection

def get_data_from_db():
    conn = get_connection()
    query = "SELECT * FROM 'pddikti_example_csv' WHERE 1"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.title('Streamlit Simple App')

page = st.sidebar.radio("Pilih halaman", ["Dataset", "Visualisai", "Form Input"])

# Tampilkan konten berdasarkan halaman yang dipilih
if page == "Dataset":
    st.header("Halaman Dataset")
elif page == "Visualisasi":
    st.header("Halaman Visualisasi")
elif page == "Form Input":
    st.header("Halaman Form Input")

with st.form(key='input_form'):
    input_semester = st.text_input('Semester')
    input_jumlah = st.number_input('Jumlah', min_value=0, format='%d')
    input_program_studi = st.text_input('Program Studi')
    input_universitas = st.text_input('Universitas')
    submit_button = st.form_submit_button(label='Submit Data')

if submit_button:
    conn = get_connection()
    cursor = conn.cursor()  # Pastikan penamaan variabel adalah 'cursor'
    
    query = """
    INSERT INTO pddikti_example_csv (`COL 2`, `COL 3`, `COL 4`, `COL 5`)
    VALUES (%s, %s, %s, %s)
    """
    
    # Eksekusi query dengan parameter dari form
    cursor.execute(query, (input_semester, input_jumlah, input_program_studi, input_universitas))
    
    conn.commit()
    conn.close()
    st.success("Data successfully submitted to the database!")

