# Mengimpor library
import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory
import numpy as np
import pandas as pd

# Membuat judul
st.title('CATERING ORDER')

# Menambah subheader
st.subheader('Selamat datang di aplikasi optimasi catering order')

# Fungsi utama
def main():
    
    # Nilai awal
    order = 400
    
    # Menambahkan kolom input kuota
    with st.container():
        col_k = st.columns(1)
        with col_k[0]:
            order = st.number_input('Order', value=order)
            
 
    # Menambahkan garis pembatas
    st.markdown('---'*10)

    # Memastikan bahwa kuota dan budget tidak saling bertentangan
    sum_cap = sum([df.Capacity[indeks] for indeks in range(len(df.Id))])
    
    if order > sum_cap:
        st.error("Melebihi kapasitas order ke vendor!")
        return
    
    # Membuat model
    model = pyo.ConcreteModel()

    # Mendefinisikan variabel
    model.Ven = pyo.Var(range(len(df.Id)), bounds=(0,None))
    
    # Mendefinisikan nama variabel baru untuk memudahkan penulisan
    ven = model.Ven
    
    # Mendefinisikan fungsi pembatas
    ven_sum = sum([ven[indeks] for indeks in range(len(df.Id))])
    model.balance = pyo.Constraint(expr = ven_sum == order)

    model.limits = pyo.ConstraintList()
    for indeks in range(len(df.Id)):
        model.limits.add(expr = ven[indeks] <= df.Capacity[indeks])


    # Mendefinisikan fungsi tujuan
    ven_sum_obj = sum([ven[indeks]*df.Cost[indeks] for indeks in range(len(df.Id))])
    model.obj = pyo.Objective(expr = ven_sum_obj, sense=minimize)

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
    for i in range(len(ven)):
        print('Vendor', df.Vendor[i], '=', pyo.value(ven[i]))

    print('Nilai fungsi tujuan =', pyo.value(model.obj))
# Mengeksekusi fungsi main
if __name__ == '__main__':
    main()
