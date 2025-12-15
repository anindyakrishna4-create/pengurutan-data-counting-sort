# File: app.py (KODE FINAL - Matplotlib Counting Sort)

import streamlit as st
import pandas as pd
import time
from counting_sort import counting_sort 
import matplotlib.pyplot as plt
import numpy as np

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Virtual Lab: Counting Sort",
    layout="wide"
)

st.title("🔢 Virtual Lab: Counting Sort Interaktif (Matplotlib)")
st.markdown("### Visualisasi Algoritma Pengurutan Data Non-Perbandingan")

st.sidebar.header("Konfigurasi Data")

# --- Input Pengguna (Tanpa Batas Input) ---
default_data = "4, 2, 1, 5, 2, 4, 3"
input_data_str = st.sidebar.text_input(
    "Masukkan data (pisahkan dengan koma):", 
    default_data
)
speed = st.sidebar.slider("Kecepatan Simulasi (detik)", 0.1, 2.0, 0.5)

# --- Proses Data Input ---
try:
    data_list = [int(x.strip()) for x in input_data_str.split(',') if x.strip()]
    initial_data = list(data_list)
    if not initial_data:
        st.error("Masukkan setidaknya satu angka.")
        st.stop()
    if max(initial_data) > 1000: # Batasan praktis untuk Count Array yang terlalu besar
         st.warning("Perhatian: Counting Sort paling efisien jika nilai maksimum (k) tidak terlalu besar. Visualisasi mungkin lambat.")

except ValueError:
    st.error("Masukkan data dalam format angka (integer) yang dipisahkan oleh koma.")
    st.stop()
    
# --- Penjelasan ---
st.markdown("""
#### Proses Counting Sort (O(n+k)):
1. **Hitung Frekuensi:** Menghitung kemunculan setiap elemen (Kuning).
2. **Akumulasi:** Menentukan posisi akhir elemen (Grafik Count Array diperbarui).
3. **Penempatan Output:** Mengisi Array Hasil (Hijau).
""")

st.write(f"**Data Awal:** {initial_data}")

# --- Fungsi Plot Matplotlib ---
def plot_array(arr, title, highlight_indices, max_val, max_k, color_map=None):
    fig, ax = plt.subplots(figsize=(6, 3.5))
    n = len(arr)
    x_pos = np.arange(n)
    
    if arr == []: 
        ax.text(0.5, 0.5, "Array Kosong", ha='center', va='center')
        ax.set_title(title)
        plt.close(fig)
        return fig

    # Tentukan Warna
    colors = ['#4A86E8'] * n # Default (Biru)
    
    if color_map: # Khusus untuk Count Array
         x_pos = np.arange(len(color_map))
         arr = color_map # Menggunakan nilai Count Array
         
         # Highlight Count Array (merah)
         if highlight_indices[0] != -1:
             idx_to_highlight = highlight_indices[0]
             if idx_to_highlight < len(colors):
                 colors[idx_to_highlight] = '#CC0000' # Merah untuk yang diakumulasi/diperiksa
         
         ax.set_xticks(x_pos)
         ax.set_xticklabels([str(i) for i in range(len(arr))], rotation=0)
         ax.set_xlabel('Nilai Elemen (i)')
         ax.set_ylabel('Posisi Akhir (Count[i])')
    else: # Input/Output Array
         # Highlight Input (Kuning) atau Output (Hijau)
         idx1, idx2 = highlight_indices
         if idx1 != -1 and idx1 < n: # Index di Input
             colors[idx1] = '#F1C232' # Kuning
         if idx2 != -1 and idx2 < n: # Index di Output
             colors[idx2] = '#6AA84F' # Hijau
             
         ax.set_xticks(x_pos)
         ax.set_xticklabels([f'{i}' for i in range(n)], rotation=0)
         ax.set_xlabel('Index')


    # Bar Plot
    ax.bar(x_pos, arr, color=colors)
    
    # Label Nilai di Atas Bar
    for i, height in enumerate(arr):
        ax.text(x_pos[i], height + max_val * 0.02, str(height), ha='center', va='bottom', fontsize=10)
        
    ax.set_ylim(0, max_val * 1.1 if max_val > 0 else 10)
    ax.set_title(title, fontsize=12)
    
    plt.close(fig) 
    return fig


# --- Visualisasi Utama ---
if st.button("Mulai Simulasi Counting Sort"):
    
    sorted_result, history = counting_sort(list(data_list))
    max_data_value = max(initial_data) if initial_data else 10
    max_count_value = max([max(state['count']) for state in history if state['count']] + [1])
    
    st.markdown("---")
    st.subheader("Visualisasi Langkah Demi Langkah")
    
    # Tempatkan visualisasi di tiga kolom
    col_input, col_count, col_output = st.columns([1, 1, 1])
    
    status_placeholder = st.empty()
    table_placeholder = st.empty()
    
    # --- Loop Simulasi ---
    for step, state in enumerate(history):
        
        current_arr = state['array']
        current_count = state['count']
        current_output = state['output']
        (idx1, idx2, action_type) = state['highlight']
        action = state['action']
        
        # Penentuan Highlight berdasarkan Fase:
        if action_type in ('Hitung', 'Penempatan'):
            highlight_input = (idx1, -1)
            highlight_output = (-1, idx2)
            highlight_count = (idx2, -1) if action_type == 'Hitung' else (current_arr[idx1], -1) 
        elif action_type == 'Akumulasi':
            highlight_input = (-1, -1)
            highlight_output = (-1, -1)
            highlight_count = (idx1, -1)
        else:
            highlight_input = (-1, -1)
            highlight_output = (-1, -1)
            highlight_count = (-1, -1)


        # --- Tampilkan Grafik (Matplotlib) ---
        with col_input:
             st.markdown("##### 1. Input Array")
             fig_input = plot_array(current_arr, "Input Array (Arr)", highlight_input, max_data_value, 0)
             st.pyplot(fig_input, clear_figure=True)
        
        with col_count:
             st.markdown("##### 2. Count Array")
             fig_count = plot_array(current_count, "Count Array (Posisi)", (-1, -1), max_count_value, 
                                     max_k=len(current_count), color_map=current_count)
             # Highlight di count_arr dilakukan di fungsi plot, jadi kita kirim highlight index (idx1)
             if action_type in ('Hitung', 'Akumulasi', 'Penempatan'):
                 idx_c = idx2 if action_type == 'Hitung' else idx1 if action_type == 'Akumulasi' else current_arr[idx1]
                 fig_count = plot_array(current_count, "Count Array (Posisi)", (idx_c, -1), max_count_value, 
                                         max_k=len(current_count), color_map=current_count)
             st.pyplot(fig_count, clear_figure=True)

        with col_output:
             st.markdown("##### 3. Output Array")
             fig_output = plot_array(current_output, "Output Array (Hasil)", highlight_output, max_data_value, 0)
             st.pyplot(fig_output, clear_figure=True)


        # --- Tabel & Status ---
        with table_placeholder.container():
            st.markdown("---")
            st.markdown("##### Detail Count Array")
            # Tampilkan Count Array sebagai tabel untuk memudahkan pemahaman Kumulatif Sum
            df_count = pd.DataFrame({'Nilai': range(len(current_count)), 'Hitungan': current_count})
            st.dataframe(df_count.T, hide_index=False, use_container_width=True)


        with status_placeholder.container():
            st.info(f"**Langkah ke-{step+1}** | **Aksi:** {action_type}")
            st.caption(action)
            
            if action_type == 'Selesai':
                 st.success("Array telah terurut! Proses Counting Sort Selesai.")
        
        # Jeda untuk simulasi
        time.sleep(speed)

    # --- Hasil Akhir Final ---
    st.balloons()
    st.success(f"**Pengurutan Selesai!**")
    st.write(f"**Data Terurut:** {sorted_result}")
    st.info(f"Algoritma Counting Sort selesai dalam **{len(history)-1}** langkah visualisasi.")
