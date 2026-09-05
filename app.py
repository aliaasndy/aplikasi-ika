import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================

st.set_page_config(
    page_title="IKA Anak Sungai",
    page_icon="💧",
    layout="wide"
)

# ============================================================
# DATA PARAMETER
# ============================================================

PARAMETER_DATA = {
    "pH": {
        "bobot": 0.137,
        "deviasi": 0.02,
        "satuan": "unit",
    },
    "BOD": {
        "bobot": 0.132,
        "deviasi": 3.64,
        "satuan": "mg/L",
    },
    "COD": {
        "bobot": 0.140,
        "deviasi": 4.82,
        "satuan": "mg/L",
    },
    "TSS": {
        "bobot": 0.086,
        "deviasi": 1.73,
        "satuan": "mg/L",
    },
    "DO": {
        "bobot": 0.167,
        "deviasi": 10.0,
        "satuan": "mg/L",
    },
    "NO3-N": {
        "bobot": 0.081,
        "deviasi": 5.0,
        "satuan": "mg/L",
    },
    "T-P": {
        "bobot": 0.100,
        "deviasi": 0.384,
        "satuan": "mg/L",
    },
    "Fecal Coli": {
        "bobot": 0.157,
        "deviasi": 10.0,
        "satuan": "MPN/100 mL",
    },
}


# ============================================================
# FUNGSI MEMBATASI NILAI Q
# ============================================================

def batas_q(q):
    """
    Q-Nilai dibatasi antara 0 sampai 100.
    """

    if q is None:
        return 0.0

    if isinstance(q, complex):
        return 0.0

    if math.isnan(q):
        return 0.0

    return max(0.0, min(100.0, float(q)))


# ============================================================
# FUNGSI Q-NILAI pH BIASA
# ============================================================

def q_ph(x):

    if x <= 1:
        return 0

    elif x <= 7:
        q = (
            -0.0375 * x**5
            + 0.5379 * x**4
            - 1.8352 * x**3
            + 0.1667 * x**2
            + 7.8273 * x
            - 6.7143
        )
        return batas_q(q)

    elif x <= 8:
        q = -4 * x + 116
        return batas_q(q)

    elif x <= 13:
        q = (
            -0.463 * x**3
            + 19.155 * x**2
            - 263.07 * x
            + 1200.4
        )
        return batas_q(q)

    else:
        return 0


# ============================================================
# FUNGSI Q-NILAI pH WILAYAH GAMBUT
# ============================================================

def q_ph_gambut(x):

    if x <= 4.1:

        z = x + 2.79

        q = (
            -0.0375 * z**5
            + 0.5379 * z**4
            - 1.8352 * z**3
            + 0.1667 * z**2
            + 7.8273 * z
            - 9.5327
        )

        return batas_q(q)

    elif x <= 7:
        q = 1.437 * x + 77.9642
        return batas_q(q)

    elif x <= 8:
        q = -4 * x + 116
        return batas_q(q)

    elif x <= 13:
        q = (
            -0.463 * x**3
            + 19.155 * x**2
            - 263.07 * x
            + 1200.4
        )
        return batas_q(q)

    else:
        return 0


# ============================================================
# FUNGSI Q-NILAI BOD
# ============================================================

def q_bod(x):

    if x <= 7:

        q = (
            -0.25 * x**3
            + 4.0952 * x**2
            - 26.726 * x
            + 118.14
        )

        return batas_q(q)

    elif x <= 32:

        q = (
            6e-05 * x**4
            - 0.0067 * x**3
            + 0.3286 * x**2
            - 8.3016 * x
            + 90.378
        )

        return batas_q(q)

    else:
        return 0


# ============================================================
# FUNGSI Q-NILAI COD
# ============================================================

def q_cod(x):

    if x <= 20:

        q = (
            0.0204 * x**2
            - 1.4479 * x
            + 99.614
        )

        return batas_q(q)

    elif x <= 25:

        q = -2.9803 * x + 138.43

        return batas_q(q)

    elif x <= 50:

        q = -0.9054 * x + 86.555

        return batas_q(q)

    elif x <= 100:

        q = (
            -0.0055 * x**2
            + 0.2907 * x
            + 40.428
        )

        return batas_q(q)

    elif x <= 150:

        q = (
            0.0088 * x**2
            - 2.4487 * x
            + 171.57
        )

        return batas_q(q)

    else:
        return 0


# ============================================================
# FUNGSI Q-NILAI TSS
# ============================================================

def q_tss(x):

    if x <= 50:

        q = -0.06 * x + 90

        return batas_q(q)

    elif x <= 60:

        q = 87

        return batas_q(q)

    elif x <= 100:

        q = (
            -4e-16 * x**2
            - 0.1 * x
            + 93
        )

        return batas_q(q)

    elif x <= 150:

        q = -0.08 * x + 91

        return batas_q(q)

    elif x <= 450:

        q = (
            -3e-05 * x**2
            - 0.1145 * x
            + 96.81
        )

        return batas_q(q)

    elif x <= 500:

        q = -0.18 * x + 121

        return batas_q(q)

    elif x <= 501:

        q = -11 * x + 5531

        return batas_q(q)

    elif x <= 2000:

        q = 20

        return batas_q(q)

    else:
        return 0


# ============================================================
# FUNGSI Q-NILAI DO
# ============================================================

def q_do(x):

    if x <= 2:

        q = (
            -0.6574 * x**2
            + 10.157 * x
            + 7e-15
        )

        return batas_q(q)

    elif x <= 7:

        q = (
            -0.023 * x**3
            - 0.993 * x**2
            + 26.124 * x
            - 30.173
        )

        return batas_q(q)

    elif x <= 8.5:

        q = 1.2438 * x + 87.428

        return batas_q(q)

    elif x <= 9:

        q = 98

        return batas_q(q)

    elif x <= 11:

        q = (
            -8.0809 * x**3
            - 227.43 * x**2
            + 2101.2 * x
            - 6300.1
        )

        return batas_q(q)

    else:
        return 0


# ============================================================
# FUNGSI Q-NILAI NO3-N
# ============================================================

def q_no3(x):

    if x <= 1:

        q = -x + 97

        return batas_q(q)

    elif x <= 6:

        q = (
            0.6989 * x**2
            - 12.05 * x
            + 107.32
        )

        return batas_q(q)

    elif x <= 15:

        q = (
            0.0714 * x**3
            - 3.4111 * x
            + 78.091
        )

        return batas_q(q)

    elif x <= 40:

        q = (
            -1e-16 * x**3
            + 0.0715 * x**2
            - 1.3929 * x
            + 62.214
        )

        return batas_q(q)

    elif x <= 50:

        q = (
            4e-16 * x**2
            - 0.8 * x
            + 50
        )

        return batas_q(q)

    elif x <= 60:

        q = (
            0.02 * x**2
            - 2.5 * x
            + 85
        )

        return batas_q(q)

    elif x <= 100:

        q = (
            0.0029 * x**2
            - 0.5571 * x
            + 30.114
        )

        return batas_q(q)

    elif x <= 101:

        q = -2 * x + 230

        return batas_q(q)

    elif x <= 200:

        q = 1

        return batas_q(q)

    else:
        return 0


# ============================================================
# FUNGSI Q-NILAI T-P
# ============================================================

def q_tp(x):

    if x <= 0.1:

        q = -8 * x + 100

        return batas_q(q)

    elif x <= 0.8:

        q = (
            246.13 * x**3
            - 304.86 * x**2
            + 30.477 * x
            + 91.909
        )

        return batas_q(q)

    elif x <= 5:

        q = (
            0.0924 * x**6
            - 6.8787 * x**5
            + 1352 * x**4
            - 64.708 * x**3
            + 148.85 * x**2
            - 184 * x
            + 126.81
        )

        return batas_q(q)

    elif x <= 10:

        q = (
            -0.0648 * x**3
            + 1.4524 * x**2
            - 18.882 * x
            + 56.921
        )

        return batas_q(q)

    elif x <= 12:

        q = 2.5 * x - 37.5

        return batas_q(q)

    else:
        return 0


# ============================================================
# FUNGSI Q-NILAI FECAL COLI
# ============================================================

def q_fecal_coli(x):

    if x <= 30:

        q = (
            -0.004 * x**3
            + 0.2471 * x**2
            - 5.2535 * x
            + 102.14
        )

        return batas_q(q)

    elif x <= 500:

        q = (
            3e-09 * x**4
            + 4e-06 * x**3
            + 0.0019 * x**2
            - 0.3953 * x
            + 67.962
        )

        return batas_q(q)

    elif x <= 1000:

        q = -0.014 * x + 36

        return batas_q(q)

    elif x <= 5000:

        q = -0.002 * x + 24

        return batas_q(q)

    elif x <= 10000:

        q = -0.0008 * x + 18

        return batas_q(q)

    elif x <= 20000:

        q = -0.0002 * x + 12

        return batas_q(q)

    elif x <= 40000:

        q = (
            5e-23 * x**2
            - 0.0001 * x
            + 10
        )

        return batas_q(q)

    elif x <= 50000:

        q = 6

        return batas_q(q)

    else:
        return 0


# ============================================================
# FUNGSI MENGHITUNG Q BERDASARKAN PARAMETER
# ============================================================

def hitung_q(parameter, x, wilayah_gambut=False):

    if parameter == "pH":

        if wilayah_gambut:
            return q_ph_gambut(x)

        return q_ph(x)

    elif parameter == "BOD":
        return q_bod(x)

    elif parameter == "COD":
        return q_cod(x)

    elif parameter == "TSS":
        return q_tss(x)

    elif parameter == "DO":
        return q_do(x)

    elif parameter == "NO3-N":
        return q_no3(x)

    elif parameter == "T-P":
        return q_tp(x)

    elif parameter == "Fecal Coli":
        return q_fecal_coli(x)

    return 0


# ============================================================
# FUNGSI PENERAPAN DEVIASI
# ============================================================

def terapkan_deviasi(nilai_uji, deviasi, arah):

    if arah == "+":
        return nilai_uji + deviasi

    elif arah == "-":
        return nilai_uji - deviasi

    return nilai_uji


# ============================================================
# FUNGSI KATEGORI IKA
# ============================================================

def kategori_ika(ika):

    if ika > 85 and ika <= 100:
        return "Sangat Baik"

    elif ika > 60 and ika <= 85:
        return "Sedang"

    elif ika >= 0 and ika <= 60:
        return "Buruk"

    return "Di luar rentang"


# ============================================================
# JUDUL
# ============================================================

st.title("💧 Aplikasi Perhitungan IKA Anak Sungai")

st.write(
    "Silakan masukkan data pemantauan kualitas air. "
    "Aplikasi akan menerapkan deviasi, menghitung Q-Nilai, "
    "mengalikan faktor pembobot, dan menghasilkan nilai IKA."
)


# ============================================================
# IDENTITAS PEMANTAUAN
# ============================================================

st.header("🌸 Identitas Pemantauan")

col1, col2, col3 = st.columns(3)

with col1:

    nama_anak_sungai = st.text_input(
        "Nama Anak Sungai"
    )

with col2:

    titik_pantau = st.selectbox(
        "Titik Pantau",
        ["Hulu", "Tengah", "Hilir"]
    )

with col3:

    semester = st.selectbox(
        "Semester",
        ["Semester 1", "Semester 2"]
    )


# ============================================================
# PILIH JENIS WILAYAH pH
# ============================================================

wilayah_gambut = st.checkbox(
    "Gunakan persamaan pH wilayah gambut"
)


# ============================================================
# INPUT 8 PARAMETER
# ============================================================

st.header("🧪 Input 8 Parameter Kualitas Air")

col1, col2 = st.columns(2)

with col1:

    ph = st.number_input(
        "1. pH",
        min_value=0.0,
        value=7.00,
        step=0.01
    )

    bod = st.number_input(
        "2. BOD (mg/L)",
        min_value=0.0,
        value=0.00,
        step=0.01
    )

    cod = st.number_input(
        "3. COD (mg/L)",
        min_value=0.0,
        value=0.00,
        step=0.01
    )

    tss = st.number_input(
        "4. TSS (mg/L)",
        min_value=0.0,
        value=0.00,
        step=0.01
    )


with col2:

    do = st.number_input(
        "5. DO (mg/L)",
        min_value=0.0,
        value=0.00,
        step=0.01
    )

    no3 = st.number_input(
        "6. Nitrat / NO3-N (mg/L)",
        min_value=0.0,
        value=0.00,
        step=0.01
    )

    tp = st.number_input(
        "7. Fosfat / T-P (mg/L)",
        min_value=0.0,
        value=0.00,
        step=0.001
    )

    fecal = st.number_input(
        "8. Total Fecal Coli (MPN/100 mL)",
        min_value=0.0,
        value=0.00,
        step=1.00
    )

# ============================================================
# TOMBOL PERHITUNGAN
# ============================================================

st.divider()

if st.button(
    "💧 Simpan dan Lanjutkan Perhitungan",
    type="primary",
    use_container_width=True
):

    # ========================================================
    # DATA HASIL UJI
    # ========================================================

    nilai_asli = {
        "pH": ph,
        "BOD": bod,
        "COD": cod,
        "TSS": tss,
        "DO": do,
        "NO3-N": no3,
        "T-P": tp,
        "Fecal Coli": fecal,
    }

    # ========================================================
    # ARAH DEVIASI OTOMATIS
    # ========================================================

    arah_deviasi = {
        "pH": "+",
        "BOD": "+",
        "COD": "+",
        "TSS": "+",
        "DO": "+",
        "NO3-N": "+",
        "T-P": "+",
        "Fecal Coli": "+",
    }

    # ========================================================
    # DATA PERUNTUKAN
    # ========================================================

    peruntukan_data = {
        "pH": "Perairan",
        "BOD": "Perairan",
        "COD": "Perairan",
        "TSS": "Perairan",
        "DO": "Perairan",
        "NO3-N": "Perairan",
        "T-P": "Perairan",
        "Fecal Coli": "Perairan",
    }

    # ========================================================
    # RUMUS Q
    # ========================================================

    rumus_data = {
        "pH": "q_ph / q_ph_gambut",
        "BOD": "q_bod",
        "COD": "q_cod",
        "TSS": "q_tss",
        "DO": "q_do",
        "NO3-N": "q_no3",
        "T-P": "q_tp",
        "Fecal Coli": "q_fecal_coli",
    }

    # ========================================================
    # HASIL TANPA DEVIASI
    # ========================================================

    hasil_tanpa_deviasi = []
    total_ika_tanpa_deviasi = 0

    for parameter in PARAMETER_DATA:

        x_asli = nilai_asli[parameter]

        q_nilai = hitung_q(
            parameter,
            x_asli,
            wilayah_gambut=wilayah_gambut
        )

        bobot = PARAMETER_DATA[parameter]["bobot"]

        subtotal = q_nilai * bobot

        total_ika_tanpa_deviasi += subtotal

        hasil_tanpa_deviasi.append({
            "Parameter": parameter,
            "Satuan": PARAMETER_DATA[parameter]["satuan"],
            "Hasil Uji": round(x_asli, 4),
            "Peruntukan": peruntukan_data[parameter],
            "Rumus Q": rumus_data[parameter],
            "Q-Nilai": round(q_nilai, 2),
            "Faktor Pembobot (W)": bobot,
            "Nilai Sub-Total": round(subtotal, 2)
        })

    total_ika_tanpa_deviasi = batas_q(
        total_ika_tanpa_deviasi
    )

    kategori_tanpa_deviasi = kategori_ika(
        total_ika_tanpa_deviasi
    )

    # ========================================================
    # HASIL DENGAN DEVIASI
    # ========================================================

    hasil_dengan_deviasi = []
    total_ika_dengan_deviasi = 0

    for parameter in PARAMETER_DATA:

        x_asli = nilai_asli[parameter]

        deviasi = PARAMETER_DATA[parameter]["deviasi"]

        arah = arah_deviasi[parameter]

        # Terapkan deviasi
        x_setelah_deviasi = terapkan_deviasi(
            x_asli,
            deviasi,
            arah
        )

        # Nilai tidak boleh negatif
        if x_setelah_deviasi < 0:
            x_setelah_deviasi = 0

        # Hitung Q-Nilai dari hasil setelah deviasi
        q_nilai = hitung_q(
            parameter,
            x_setelah_deviasi,
            wilayah_gambut=wilayah_gambut
        )

        # Faktor pembobot
        bobot = PARAMETER_DATA[parameter]["bobot"]

        # Q-Nilai x Faktor Pembobot
        subtotal = q_nilai * bobot

        # Sigma Subtotal
        total_ika_dengan_deviasi += subtotal

        hasil_dengan_deviasi.append({
            "Parameter": parameter,
            "Satuan": PARAMETER_DATA[parameter]["satuan"],
            "Hasil Uji Asli": round(x_asli, 4),
            "Ekv. Deviasi": round(deviasi, 4),
            "Arah": arah,
            "Hasil Uji Setelah Deviasi": round(
                x_setelah_deviasi,
                4
            ),
            "Peruntukan": peruntukan_data[parameter],
            "Rumus Q": rumus_data[parameter],
            "Q-Nilai": round(q_nilai, 2),
            "Faktor Pembobot (W)": bobot,
            "Nilai Sub-Total": round(subtotal, 2)
        })

    total_ika_dengan_deviasi = batas_q(
        total_ika_dengan_deviasi
    )

    kategori_dengan_deviasi = kategori_ika(
        total_ika_dengan_deviasi
    )

    # ========================================================
    # SIMPAN HASIL
    # ========================================================

    st.session_state["hasil_tanpa_deviasi"] = (
        hasil_tanpa_deviasi
    )

    st.session_state["hasil_dengan_deviasi"] = (
        hasil_dengan_deviasi
    )

    st.session_state["total_ika_tanpa_deviasi"] = (
        total_ika_tanpa_deviasi
    )

    st.session_state["total_ika_dengan_deviasi"] = (
        total_ika_dengan_deviasi
    )

    st.session_state["kategori_tanpa_deviasi"] = (
        kategori_tanpa_deviasi
    )

    st.session_state["kategori_dengan_deviasi"] = (
        kategori_dengan_deviasi
    )

    st.session_state["nama_anak_sungai"] = (
        nama_anak_sungai
    )

    st.session_state["titik_pantau"] = titik_pantau

    st.session_state["semester"] = semester

# ============================================================
# TAMPILKAN HASIL
# ============================================================

if "hasil_tanpa_deviasi" in st.session_state:

    st.divider()

    # ========================================================
    # RINGKASAN DATA PEMANTAUAN
    # ========================================================

    st.header("📋 Ringkasan Data Pemantauan")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.write(
            f"**Nama Anak Sungai:** "
            f"{st.session_state['nama_anak_sungai']}"
        )

    with col_b:
        st.write(
            f"**Titik Pantau:** "
            f"{st.session_state['titik_pantau']}"
        )

    with col_c:
        st.write(
            f"**Semester:** "
            f"{st.session_state['semester']}"
        )


    # ========================================================
    # DATA HASIL ASLI DAN HASIL + DEVIASI
    # ========================================================

    df_asli = pd.DataFrame(
        st.session_state["hasil_tanpa_deviasi"]
    )

    df_plus = pd.DataFrame(
        st.session_state["hasil_dengan_deviasi"]
    )


    # ========================================================
    # MEMBUAT HASIL - DEVIASI
    # ========================================================

    hasil_minus_deviasi = []
    total_ika_minus_deviasi = 0

    for _, row in df_asli.iterrows():

        parameter = row["Parameter"]

        x_asli = float(row["Hasil Uji"])

        deviasi = float(
            PARAMETER_DATA[parameter]["deviasi"]
        )

        # Hasil Uji - Deviasi
        x_setelah_minus = x_asli - deviasi

        # Nilai tidak boleh negatif
        if x_setelah_minus < 0:
            x_setelah_minus = 0

        # Hitung Q-Nilai
        q_nilai_minus = hitung_q(
            parameter,
            x_setelah_minus,
            wilayah_gambut=wilayah_gambut
        )

        # Faktor pembobot
        bobot = PARAMETER_DATA[parameter]["bobot"]

        # Subtotal
        subtotal_minus = q_nilai_minus * bobot

        # Total IKA
        total_ika_minus_deviasi += subtotal_minus

        hasil_minus_deviasi.append({

            "Parameter": parameter,

            "Satuan":
                PARAMETER_DATA[parameter]["satuan"],

            "Hasil Uji Asli":
                round(x_asli, 4),

            "Ekv. Deviasi":
                round(deviasi, 4),

            "Arah":
                "-",

            "Hasil Uji Setelah Deviasi":
                round(x_setelah_minus, 4),

            "Peruntukan":
                row["Peruntukan"],

            "Rumus Q":
                row["Rumus Q"],

            "Q-Nilai":
                round(q_nilai_minus, 2),

            "Faktor Pembobot (W)":
                bobot,

            "Nilai Sub-Total":
                round(subtotal_minus, 2)

        })


    # Batasi total IKA
    total_ika_minus_deviasi = batas_q(
        total_ika_minus_deviasi
    )

    kategori_minus_deviasi = kategori_ika(
        total_ika_minus_deviasi
    )

    df_minus = pd.DataFrame(
        hasil_minus_deviasi
    )


    # ========================================================
    # TABEL 1 - HASIL UJI ASLI
    # ========================================================

    st.divider()

    st.header(
        "📊 Tabel 1. Perhitungan IKA Nilai Asli"
    )

    st.caption(
        "Hasil perhitungan menggunakan nilai hasil uji asli "
        "tanpa penambahan atau pengurangan ekivalen deviasi."
    )

    st.dataframe(
        df_asli,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # TOTAL IKA NILAI ASLI
    # ========================================================

    st.subheader("💧 Hasil IKA Nilai Asli")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "IKA Nilai Asli",
            f"{st.session_state['total_ika_tanpa_deviasi']:.2f}"
        )

    with col2:
        st.metric(
            "Kategori",
            st.session_state["kategori_tanpa_deviasi"]
        )


    # ========================================================
    # TABEL 2 - HASIL + DEVIASI
    # ========================================================

    st.divider()

    st.header(
        "📊 Tabel 2. Perhitungan IKA Hasil Uji + Deviasi"
    )

    st.caption(
        "Hasil uji setelah ditambahkan ekivalen deviasi (+)."
    )

    st.dataframe(
        df_plus,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # TOTAL IKA + DEVIASI
    # ========================================================

    st.subheader("💧 Hasil IKA + Deviasi")

    col3, col4 = st.columns(2)

    with col3:
        st.metric(
            "IKA + Deviasi",
            f"{st.session_state['total_ika_dengan_deviasi']:.2f}"
        )

    with col4:
        st.metric(
            "Kategori",
            st.session_state["kategori_dengan_deviasi"]
        )


    # ========================================================
    # TABEL 3 - HASIL - DEVIASI
    # ========================================================

    st.divider()

    st.header(
        "📊 Tabel 3. Perhitungan IKA Hasil Uji − Deviasi"
    )

    st.caption(
        "Hasil uji setelah dikurangi ekivalen deviasi (−)."
    )

    st.dataframe(
        df_minus,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # TOTAL IKA - DEVIASI
    # ========================================================

    st.subheader("💧 Hasil IKA − Deviasi")

    col5, col6 = st.columns(2)

    with col5:
        st.metric(
            "IKA − Deviasi",
            f"{total_ika_minus_deviasi:.2f}"
        )

    with col6:
        st.metric(
            "Kategori",
            kategori_minus_deviasi
        )


    # ========================================================
    # TABEL GABUNGAN PER PARAMETER
    # ========================================================

    st.divider()

    st.header(
        "📋 Tabel 4. Perbandingan Hasil Asli, + Deviasi, dan − Deviasi"
    )

    data_gabungan = []

    for parameter in df_asli["Parameter"]:

        asli = df_asli[
            df_asli["Parameter"] == parameter
        ].iloc[0]

        plus = df_plus[
            df_plus["Parameter"] == parameter
        ].iloc[0]

        minus = df_minus[
            df_minus["Parameter"] == parameter
        ].iloc[0]

        data_gabungan.append({

            "Parameter": parameter,

            "Satuan":
                asli["Satuan"],

            "Hasil Uji Asli":
                asli["Hasil Uji"],

            "Deviasi":
                plus["Ekv. Deviasi"],

            "Hasil + Deviasi":
                plus["Hasil Uji Setelah Deviasi"],

            "Hasil − Deviasi":
                minus["Hasil Uji Setelah Deviasi"],

            "Q-Nilai Asli":
                asli["Q-Nilai"],

            "Q-Nilai +":
                plus["Q-Nilai"],

            "Q-Nilai −":
                minus["Q-Nilai"],

            "Subtotal Asli":
                asli["Nilai Sub-Total"],

            "Subtotal +":
                plus["Nilai Sub-Total"],

            "Subtotal −":
                minus["Nilai Sub-Total"]

        })


    df_gabungan = pd.DataFrame(
        data_gabungan
    )

    st.dataframe(
        df_gabungan,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# HITUNG HASIL GABUNGAN ± DEVIASI
# ============================================================

# Gabungan diambil sebagai nilai rata-rata hasil + deviasi
# dan hasil - deviasi
total_ika_gabungan = (
    total_ika_dengan_deviasi
    + total_ika_minus_deviasi
) / 2

total_ika_gabungan = batas_q(
    total_ika_gabungan
)

kategori_gabungan = kategori_ika(
    total_ika_gabungan
)


# ============================================================
# RINGKASAN HASIL IKA
# ============================================================

st.divider()

st.header("💧 Ringkasan Hasil IKA")

df_ringkasan = pd.DataFrame({
    "Metode": [
        "Nilai Asli",
        "Hasil Uji + Deviasi",
        "Hasil Uji − Deviasi",
        "Hasil Uji ± Deviasi"
    ],
    "Nilai IKA": [
        round(total_ika_tanpa_deviasi, 2),
        round(total_ika_dengan_deviasi, 2),
        round(total_ika_minus_deviasi, 2),
        round(total_ika_gabungan, 2)
    ],
    "Kategori": [
        kategori_tanpa_deviasi,
        kategori_dengan_deviasi,
        kategori_minus_deviasi,
        kategori_gabungan
    ]
})

st.dataframe(
    df_ringkasan,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# PERBANDINGAN NILAI IKA
# ============================================================

st.divider()

st.header("📌 Perbandingan Nilai IKA")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Nilai Asli",
        f"{total_ika_tanpa_deviasi:.2f}"
    )

with col2:
    st.metric(
        "+ Deviasi",
        f"{total_ika_dengan_deviasi:.2f}"
    )

with col3:
    st.metric(
        "− Deviasi",
        f"{total_ika_minus_deviasi:.2f}"
    )

with col4:
    st.metric(
        "± Gabungan",
        f"{total_ika_gabungan:.2f}"
    )


# ============================================================
# GRAFIK PERBANDINGAN Q-NILAI
# ============================================================

st.divider()

st.header("📈 Perbandingan Q-Nilai")

fig_q, ax_q = plt.subplots(
    figsize=(12, 6)
)

posisi = range(len(df_gabungan))

lebar = 0.25

ax_q.bar(
    [x - lebar for x in posisi],
    df_gabungan["Q-Nilai Asli"],
    width=lebar,
    label="Nilai Asli"
)

ax_q.bar(
    posisi,
    df_gabungan["Q-Nilai +"],
    width=lebar,
    label="+ Deviasi"
)

ax_q.bar(
    [x + lebar for x in posisi],
    df_gabungan["Q-Nilai −"],
    width=lebar,
    label="− Deviasi"
)

ax_q.set_xticks(
    list(posisi)
)

ax_q.set_xticklabels(
    df_gabungan["Parameter"],
    rotation=30
)

ax_q.set_xlabel("Parameter")

ax_q.set_ylabel("Q-Nilai")

ax_q.set_title(
    "Perbandingan Q-Nilai Nilai Asli, + Deviasi, dan − Deviasi"
)

ax_q.set_ylim(0, 100)

ax_q.legend()

st.pyplot(fig_q)

plt.close(fig_q)


# ============================================================
# DOWNLOAD CSV
# ============================================================

st.divider()

st.header("⬇️ Download Hasil Perhitungan")


# Download Nilai Asli
csv_asli = df_asli.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Hasil Nilai Asli CSV",
    data=csv_asli,
    file_name="hasil_ika_nilai_asli.csv",
    mime="text/csv",
    use_container_width=True
)


# Download Hasil + Deviasi
csv_plus = df_plus.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Hasil + Deviasi CSV",
    data=csv_plus,
    file_name="hasil_ika_plus_deviasi.csv",
    mime="text/csv",
    use_container_width=True
)


# Download Hasil - Deviasi
csv_minus = df_minus.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Hasil − Deviasi CSV",
    data=csv_minus,
    file_name="hasil_ika_minus_deviasi.csv",
    mime="text/csv",
    use_container_width=True
)


# Download Tabel Gabungan
csv_gabungan = df_gabungan.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Tabel Gabungan CSV",
    data=csv_gabungan,
    file_name="hasil_ika_gabungan.csv",
    mime="text/csv",
    use_container_width=True
)


# Download Ringkasan
csv_ringkasan = df_ringkasan.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Ringkasan IKA CSV",
    data=csv_ringkasan,
    file_name="ringkasan_ika.csv",
    mime="text/csv",
    use_container_width=True
)
# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Aplikasi Perhitungan Indeks Kualitas Air (IKA) Anak Sungai"
)
