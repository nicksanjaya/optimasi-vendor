# Mengimpor library
import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory
import numpy as np
import pandas as pd
import streamlit as st

# Membuat judul
st.title('OPTIMIZATION ORDER')

# Menambah subheader
st.subheader('Selamat datang di aplikasi optimasi kuota order ke vendor subcon')

# Fungsi utama
def solve_optimization(df,order):
    
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
        model.limits.add(expr = ven[indeks] >= df.Order[indeks])

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
    
    # Menambahkan garis pembatas
    st.markdown('---'*10)
    
    # Menampilkan hasil optimasi
    for i in range(len(ven)):
        st.write('<center><b><h3>Vendor', df.Vendor[i], '=', pyo.value(ven[i]), '</b></h3>', unsafe_allow_html=True)

    st.write('<center><b><h3>Cost =', pyo.value(model.obj), '</b></h3>', unsafe_allow_html=True)

def convert_df(df):
    # Check if necessary columns exist
    required_columns = ['Id', 'Capacity', 'Vendor', 'Cost','Order']
    for col in required_columns:
        if col not in df.columns:
            st.error(f"Missing required column: {col}")
            return
            
    df["Order"] = df["Order"].astype(int)
    df["Capacity"] = df["Capacity"].astype(int)
    df["Cost"] = df["Cost"].astype(int)

def preprocessing(df):
    preprocessor_numerik = Pipeline([
        ('imputasi', SimpleImputer(strategy='constant', fill_value='0'))
    ])
    
    # Menggabungkan kedua pipeline di atas
    preprocessor = ColumnTransformer([
        ('preprocessing numerik', preprocessor_numerik, df.Order)],
        remainder='passthrough',
        verbose_feature_names_out=False
    )


# Upload Excel file
uploaded_file = st.file_uploader("Upload Excel Vendor File", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        preprocessing(df) 
        st.write(df)  
    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")
        
    convert_df(df)
    # Input box for capacity
    order = st.number_input("Enter Order:", min_value=0)

    # Button to create schedule
    if st.button("Calculate"):
        try:
            solve_optimization(df,order)
        except Exception as e:
            st.error(f"Error : {e}")
