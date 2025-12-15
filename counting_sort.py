# File: counting_sort.py (KODE FINAL)

# List global untuk menyimpan riwayat langkah
HISTORY = []

def counting_sort(data_list):
    """
    Mengimplementasikan Counting Sort dan mencatat setiap langkah di HISTORY.
    """
    global HISTORY
    HISTORY = []
    
    arr = data_list[:]
    n = len(arr)
    
    # 1. Tentukan nilai maksimum (k) untuk membuat Count Array
    if not arr:
        return [], HISTORY
        
    k = max(arr)
    
    # Inisialisasi Count Array dan Output Array
    # Ukuran Count Array adalah k + 1 (indeks 0 hingga k)
    count_arr = [0] * (k + 1)
    output_arr = [0] * n
    
    # Catat status awal (Input, Count, Output)
    HISTORY.append({
        'array': arr[:], 
        'count': count_arr[:], 
        'output': output_arr[:],
        'highlight': (-1, -1, 'Inisialisasi'), 
        'action': f'Inisialisasi Count Array (Ukuran: {k+1}) dan Output Array.'
    })
    
    # 2. Fase Menghitung Frekuensi
    # array: arr -> count_arr
    HISTORY.append({
        'array': arr[:], 
        'count': count_arr[:], 
        'output': output_arr[:],
        'highlight': (-1, -1, 'Hitung Frekuensi'), 
        'action': 'Fase 1: Menghitung Frekuensi Elemen pada Count Array.'
    })
    for i in range(n):
        element = arr[i]
        count_arr[element] += 1
        
        # Catat setiap kali elemen dihitung (opsional, untuk visualisasi per langkah)
        HISTORY.append({
            'array': arr[:], 
            'count': count_arr[:], 
            'output': output_arr[:],
            'highlight': (i, element, 'Hitung'), # i: index di arr, element: index di count_arr
            'action': f'Elemen {element} di Indeks {i} dihitung. Count[{element}] = {count_arr[element]}'
        })

    # 3. Fase Akumulasi (Kumulatif Sum)
    # count_arr[i] sekarang menyimpan posisi akhir elemen i dalam output_arr
    HISTORY.append({
        'array': arr[:], 
        'count': count_arr[:], 
        'output': output_arr[:],
        'highlight': (-1, -1, 'Kumulatif Sum'), 
        'action': 'Fase 2: Akumulasi Jumlah (Kumulatif Sum) pada Count Array.'
    })
    for i in range(1, k + 1):
        count_arr[i] += count_arr[i - 1]
        
        # Catat setiap akumulasi
        HISTORY.append({
            'array': arr[:], 
            'count': count_arr[:], 
            'output': output_arr[:],
            'highlight': (i, i, 'Akumulasi'), # i: index di count_arr
            'action': f'Count[{i}] = Count[{i}] + Count[{i-1}]. Posisi akhir elemen {i} adalah {count_arr[i]}'
        })

    # 4. Fase Pembangunan Output Array (Mengisi Output Array)
    # Penting: Loop mundur (range(n - 1, -1, -1)) untuk menjaga stabilitas pengurutan.
    HISTORY.append({
        'array': arr[:], 
        'count': count_arr[:], 
        'output': output_arr[:],
        'highlight': (-1, -1, 'Isi Output'), 
        'action': 'Fase 3: Mengisi Output Array dari belakang (menjaga stabilitas).'
    })
    for i in range(n - 1, -1, -1):
        element = arr[i]
        
        # Posisi di output_arr
        output_pos = count_arr[element] - 1
        
        # Tempatkan elemen ke output_arr
        output_arr[output_pos] = element
        
        # Kurangi count (untuk elemen dengan nilai yang sama berikutnya)
        count_arr[element] -= 1
        
        # Catat langkah penempatan
        HISTORY.append({
            'array': arr[:], 
            'count': count_arr[:], 
            'output': output_arr[:],
            'highlight': (i, output_pos, 'Penempatan'), # i: index arr, output_pos: index output_arr
            'action': f'Elemen {element} dari arr[{i}] ditempatkan di output_arr[{output_pos}].'
        })

    # 5. Salin Hasil ke Array Asli (Opsional, tapi penting jika ingin arr terurut)
    # (Diabaikan karena visualisasi fokus ke output_arr)
    
    # STATUS SELESAI DICATAT SETELAH SEMUA PROSES PENGURUTAN SELESAI
    HISTORY.append({
        'array': arr[:], 
        'count': count_arr[:], 
        'output': output_arr[:],
        'highlight': (-1, -1, 'Selesai'), 
        'action': 'Pengurutan Selesai. Hasil ada di Output Array.'
    })
    
    return output_arr, HISTORY
