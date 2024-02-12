# Bismillah

biomarkers = ["SpO2", "BP Dia", "BP Sys", "HRV", "Stress", "HR", "Body Temp"]
"""
) Asal bukan 00:00:00 -> Data harian
...
Algoritma manual:
- Kalau baris datanya ada biomarkernya, maka timestampnya itu berguna, catat sebagai titik 0 blok ini
- Kalau baris selanjutnya
    - masih ada biomarkernya, teruskan
    - tiada biomarkernya, dan interval masih <= 10 menit (atau lebih sedikit), teruskan
    - tiada biomarker lagi, dan interval sudah >15 menit, maka durasi blok ini adalah dari awal tadi hingga timestamp terakhir ketika biomarker masih ada. Namun, catat titik ini sebagai titik 0 blok nyala tak dipakai
    - Kalau baris selanjutnya
        - ada lagi biomarkernya, mulai dari awal lagi.
        - tidak ada biomarker lagi, dan interval masih <= 10 menit (atau lebih sedikit), teruskan
        - tiada biomarker lagi, dan interval sudah >15 menit, maka durasi blok nyala tak dipakai ini adalah dari awal tadi hingga timestamp terakhir ketika biomarker tidak ada.


"""

t_start_nd, t_end_nd, t_start_ntd, t_end_ntd = 0
durasi_nyala_digunakan = 0
durasi_nyala_tak_digunakan = 0

def isUsed(row):
    for col in row:
        if col in ["SpO2", "BP Dia", "BP Sys", "HRV", "Stress", "HR"]:
            if col.isna(): return False
            else: return True
        if col == "Body Temp":
            if 35.6 < col < 39:
                return True
            else: return False

def calculate_durations(row):
    if(t_start_nd == 0 or t_start_ntd == 0):
        if isUsed(row):
            t_start_nd = row["Timestamp"]
        else:
            t_start_ntd = row["Timestamp"]

    elif (t_start_nd != 0):
        if isUsed(row):
            interval = row["Timestamp"] - t_start_nd
            if(interval <= 15):
                durasi_nyala_digunakan += interval
                t_start_nd = row["Timestamp"]
            else:
                t_start_nd = 0

    elif (t_start_ntd != 0):
        


def main():
    while True:
        if data_is_coming():
            calculate_durations(row)