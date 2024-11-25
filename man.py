import json
import re

def split_tabel_ref(text):
    # Pisahkan teks berdasarkan baris baru
    lines = text.strip().splitlines()
    # Daftar untuk tabel dan referensi
    tables = []
    refs = []
    # Variabel sementara untuk menyimpan blok tabel
    current_table = []
    # Iterasi melalui setiap baris
    for line in lines:
        line = line.strip()  # Hapus spasi di awal dan akhir
        if line.startswith("Table"):
            if current_table:  # Jika ada blok tabel sebelumnya, tambahkan ke daftar tabel
                tables.append("\n".join(current_table))
                current_table = []  # Reset blok tabel
            current_table.append(line)  # Mulai blok tabel baru
        elif line.startswith("Ref:"):
            refs.append(line)  # Tambahkan ke daftar referensi
        elif current_table:  # Tambahkan baris ke blok tabel saat ini jika ada
            current_table.append(line)
    # Tambahkan tabel terakhir jika ada
    if current_table:
        tables.append("\n".join(current_table))
    return tables, refs

def ck_is_null(ls):
    return 'null' in ls and 'not null' not in ls

def ck_is_primary(ls):
    return 'pk' in ls

def ck_is_increment(ls):
    return 'increment' in ls

def ck_default(ls):
    return 'default' in ls
    

def extract_table(table):
    lines = [line for line in table.split('\n') if line.strip()]  # Pisahkan dan hilangkan baris kosong
    if not lines:
        return {}

    # Ambil nama tabel
    table_name = lines[0].split()[-1].replace('{', '')
    items_field = []

    # Proses setiap baris field (kecuali baris pertama dan terakhir)
    for line in lines[1:-1]:
        items = [item for item in line.split() if item]  # Split dan buang elemen kosong
        tmp = {
            'name': items[0],
            'type': items[1],
            'null': len(items) < 3  # Asumsikan null jika panjang item kurang dari 3
        }

        # Ekstrak atribut dalam tanda []
        match = re.search(r"\[(.*?)\]", line)
        if match:
            result = re.split(r",\s*", match.group(1))  # Pisahkan dengan koma, fleksibel dengan spasi
            tmp['increment']    = ck_is_increment(result)
            tmp['primary']      = ck_is_primary(result)
            tmp['null']         = not tmp['primary'] and ck_is_null(result)

            print(ck_default(result))

        items_field.append(tmp)

    # Bangun hasil akhir
    result = {
        'table': table_name,
        'items': items_field
    }

    print(json.dumps(result, indent=2))
    return result
    



f = open("input.txt", "r")
text = f.read()

tables, refs = split_tabel_ref(text)

extract_table(tables[2])

