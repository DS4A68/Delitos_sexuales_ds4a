import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st


#data = pd.read_excel(r"data\Reporte__Delitos_sexuales_Polic_a_Nacional (1).xlsx")
#data['FECHA HECHO'] = pd.to_datetime(data['FECHA HECHO'])

grouped = pd.read_csv('grouped.csv')
etario_ = pd.read_csv("etario.csv")

st.set_page_config(layout="wide")

def run():


    st.title(" CRIME PROGRESSION ")


    grouped = pd.read_csv('grouped.csv')
    grouped = grouped.groupby('FECHA HECHO')['Count'].count().to_frame().reset_index()
    fig_1 = px.line(grouped, x= "FECHA HECHO", y= "Count")
    st.plotly_chart(fig_1,use_container_width=True)

    filter_dept_ = st.selectbox("Select Department", sorted(etario_['DEPARTAMENTO'].unique()))
    etario_df_plot = etario_[etario_['DEPARTAMENTO'] == filter_dept_]
    fig2 = px.bar(etario_df_plot,x = 'GRUPO ETARIO',y= 'FECHA HECHO')
    st.plotly_chart(fig2,use_container_width=True)



    

if __name__ == "__main__":
    run()