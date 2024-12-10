# Mengimpor library
import streamlit as st
import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory

# Membuat judul
st.title('CATERING ORDER')

# Menambah subheader
st.subheader('Selamat datang di aplikasi optimasi catering order')

# Fungsi utama
def main():
    
    # Nilai awal
    kuota = 400
    budget = 7000000 
    harga_ayam = 15000 
    ayam_min = 100 
    harga_daging = 17000 
    daging_min = 50 
    harga_ikan = 13000 
    ikan_min = 50
    harga_telur = 13000 
    telur_min = 50
    harga_special = 15000 
    special_min = 50 
    
    # Menambahkan kolom input kuota
    with st.container():
        col_k = st.columns(1)
        with col_k[0]:
            kuota = st.number_input('Kuota', value=kuota)
            
    # Menambahkan garis pembatas
    st.markdown('---'*10)
    
    # Menambahkan kolom input budget
    with st.container():
        col_b = st.columns(1)
        with col_b[0]:
            budget = st.number_input('Budget', value=budget)
    
    # Menambahkan garis pembatas
    st.markdown('---'*10)  
    
    # Menambahkan kolom input harga ayam
    with st.container():
        col_a = st.columns(1)
        with col_a[0]:
            harga_ayam = st.number_input('Harga Ayam Per Porsi', value=harga_ayam)
    
    # Menambahkan kolom input kuota minimum ayam
    with st.container():
        col1 = st.columns(1)
        with col1[0]:
            ayam_min = st.number_input('Ayam (Min)', value=ayam_min)
    
    # Menambahkan garis pembatas
    st.markdown('---'*10)
    
    # Menambahkan kolom input harga daging
    with st.container():
        col_d = st.columns(1)
        with col_d[0]:
            harga_daging = st.number_input('Harga Daging Per Porsi', value=harga_daging)
    
    # Menambahkan kolom input kuota minimum daging
    with st.container():
        col2= st.columns(1)
        with col2[0]:
            daging_min = st.number_input('Daging (Min)', value=daging_min)
    
    # Menambahkan garis pembatas
    st.markdown('---'*10)
    
    # Menambahkan kolom input harga ikan
    with st.container():
        col_i = st.columns(1)
        with col_i[0]:
            harga_ikan = st.number_input('Harga Ikan Per Porsi', value=harga_ikan)
    
    # Menambahkan kolom input kuota minimum ikan
    with st.container():
        col3 = st.columns(1)
        with col3[0]:
            ikan_min = st.number_input('Ikan (Min)', value=ikan_min)

    # Menambahkan garis pembatas
    st.markdown('---'*10)

    # Menambahkan kolom input harga telur
    with st.container():
        col_t = st.columns(1)
        with col_t[0]:
            harga_telur = st.number_input('Harga Telur Per Porsi', value=harga_telur)
    
    # Menambahkan kolom input kuota minimum telur
    with st.container():
        col4 = st.columns(1)
        with col4[0]:
            telur_min = st.number_input('Telur (Min)', value=telur_min)

    # Menambahkan garis pembatas
    st.markdown('---'*10)
    
    # Menambahkan kolom input harga special
    with st.container():
        col_s = st.columns(1)
        with col_s[0]:
            harga_special = st.number_input('Harga Special Per Porsi', value=harga_special)
    
    # Menambahkan kolom input kuota minimum special
    with st.container():
        col5 = st.columns(1)
        with col5[0]:
            special_min = st.number_input('Special (Min)', value=special_min)
 
    # Menambahkan garis pembatas
    st.markdown('---'*10)

    # Memastikan bahwa kuota dan budget tidak saling bertentangan
    total_min_budget = (ayam_min * harga_ayam) + (daging_min * harga_daging) + (ikan_min * harga_ikan) + (telur_min * harga_telur) + (special_min * harga_special)
    if total_min_budget > budget:
        st.error("Budget tidak cukup untuk memenuhi kuota minimum!")
        return
    
    # Membuat model
    model = pyo.ConcreteModel()

    # Mendefinisikan variabel
    model.a = pyo.Var(bounds=(ayam_min,None))
    model.d = pyo.Var(bounds=(daging_min,None))
    model.i = pyo.Var(bounds=(ikan_min,None))
    model.t = pyo.Var(bounds=(telur_min,None))
    model.s = pyo.Var(bounds=(special_min,None))
    
    # Mendefinisikan namavariabel baru untuk memudahkan penulisan
    a = model.a
    d = model.d
    i = model.i
    t = model.t
    s = model.s
    
    # Mendefinisikan fungsi pembatas
    model.C1 = pyo.Constraint(expr = harga_ayam*a+harga_daging*d+harga_ikan*i+harga_telur*t+harga_special*s<=budget)
    model.C2 = pyo.Constraint(expr = a+d+i+t+s==kuota)
    model.C3 = pyo.Constraint(expr = a>=0)
    model.C4 = pyo.Constraint(expr = d>=0)
    model.C5 = pyo.Constraint(expr = i>=0)
    model.C6 = pyo.Constraint(expr = t>=0)
    model.C7 = pyo.Constraint(expr = s>=0)

    # Mendefinisikan fungsi tujuan
    model.obj = pyo.Objective(expr = harga_ayam*a+harga_daging*d+harga_ikan*i+harga_telur*t+harga_special*s, sense=maximize)

    # Mendefinisikan solver
    opt = SolverFactory('glpk')
    
    # Menjalankan optimasi
    results = opt.solve(model, tee=True)  # tee=True untuk menampilkan output solver di konsol
    
    # Periksa apakah solver berhasil menemukan solusi
    if results.solver.status != SolverStatus.ok or results.solver.termination_condition != TerminationCondition.optimal:
        st.error(f"Solusi tidak ditemukan! Status solver: {results.solver.status}, Termination condition: {results.solver.termination_condition}")
        return
    
    # Menyimpan hasil model
    a_value = pyo.value(a)
    d_value = pyo.value(d)
    i_value = pyo.value(i)
    t_value = pyo.value(t)
    s_value = pyo.value(s)
    z_value = pyo.value(model.obj)
    
    # Menambahkan garis pembatas
    st.markdown('---'*10)
    
    # Menampilkan hasil optimasi
    st.write('<center><b><h3>Ayam= ', a_value,'</b></h3>', unsafe_allow_html=True)
    st.write('<center><b><h3>Daging= ', d_value,'</b></h3>', unsafe_allow_html=True)
    st.write('<center><b><h3>Ikan= ', i_value,'</b></h3>', unsafe_allow_html=True)
    st.write('<center><b><h3>Telur= ', t_value,'</b></h3>', unsafe_allow_html=True)
    st.write('<center><b><h3>Special= ', s_value,'</b></h3>', unsafe_allow_html=True)
    st.write('<center><b><h3>Total= ', z_value,'</b></h3>', unsafe_allow_html=True)

# Mengeksekusi fungsi main
if __name__ == '__main__':
    main()
