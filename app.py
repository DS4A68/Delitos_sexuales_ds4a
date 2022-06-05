from turtle import width
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import folium
from streamlit_folium import st_folium
import time


st.set_page_config(layout = "wide")
df_time = pd.read_csv("df_time_all.csv")
df_time = df_time.drop(df_time.columns.to_list()[0],axis =1)
df_time['FECHA HECHO'] = pd.to_datetime(df_time['FECHA HECHO'])



#data = pd.read_excel("Reporte__Delitos_sexuales_Polic_a_Nacional (1) (2).xlsx", nrows= 10000)
#Plto with full time series. 


#INITIAL PLOT 
df_time_big_front = df_time.groupby(pd.Grouper(key = 'FECHA HECHO',freq='M')).sum().reset_index()
plot_time = px.line(
    df_time_big_front,
    x = 'FECHA HECHO',
    y = 'CANTIDAD'
)
plot_time.update_yaxes(title_text = "Cantidad de eventos")
plot_time.update_xaxes(title_text = "Tiempo ")
plot_time.update_layout(title = " Progresion de crimenes en el tiempo " ,height = 400,width = 1600)


#TOP LEFT PLOT - WEEKDAY

df_time_weekday =  df_time.groupby(df_time["FECHA HECHO"].dt.weekday).sum().reset_index()
df_time_weekday['WEEKDAY'] =  ['LUNES','MARTES','MIERCOLES','JUEVES','VIERNES','SABADO','DOMINGO']
weekday_plot = px.bar(
    df_time_weekday,
    x = 'WEEKDAY',
    y = 'CANTIDAD' 
) 
weekday_plot.update_layout(
    title = "Crimenes por día de la semana",
    xaxis_title = "Day de la Semana",
    yaxis_title = "Cantidad de eventos",
)




df_time_month_year = df_time.copy()
df_time_month_year['MONTH'] = df_time_month_year['FECHA HECHO'].dt.month
df_time_month_year['YEAR'] = df_time_month_year['FECHA HECHO'].dt.year


month_year_plot = px.area(df_time_month_year,x = 'YEAR', y ='CANTIDAD',color = 'MONTH')
month_year_plot.update_layout(
    xaxis_title = 'Año',
    yaxis_title = 'Cantidad de eventos',
    title = "Casos por año y mes"
)




select_box = st.sidebar.selectbox("Despliege esta lista de opciones para ver los distintos analisis",("Como funciona esta apliación","Analisis tiempo",'Geoanalisis'))
#st.title("Analisis estadisitco  -  Delitos sexuales en Colombia")


if select_box == "Como funciona esta apliación":
    st.title("Analisis estadisitco  -  Delitos sexuales en Colombia")
    st.title("Como funciona esta aplicación")
    st.markdown("Bienvenido a nuestra aplicación. Mira el siguiente video si es la primera vez que entras o si deseas recordar como funciona!")
    st.markdown("Gracias")


    url = "https://www.youtube.com/watch?v=hwgfwi2wnX4"
    st.video(url)



if select_box == "Analisis tiempo":
    st.title("Analisis estadisitco  -  Delitos sexuales en Colombia")
    st.title("Progresion de los Delitos En Colombia")
    with st.container():
        st.plotly_chart(plot_time,use_conatiner_width = True)
    col1,col2 =  st.columns(2)
    with col1:
        st.plotly_chart(weekday_plot,use_conatiner_width = True)
    with col2:
        st.plotly_chart(month_year_plot,use_container_width =True)


if select_box == 'Geoanalisis':
    st.title("Analisis estadisitco  -  Delitos sexuales en Colombia")
    st.title("Analisis Geografico")

    map = folium.Map(location=[6.258679441576251, -75.55570032068375],
                        zoom_start=14,
                        tiles="OpenStreetMap")

    folium.Marker([6.258679441576251, -75.55570032068375]).add_to(map)
    st.markdown("Ignora el mensaje en amarillo debajo, espera 1 minutopara que cargue el mapa ")
    #time.sleep(60)
    
    st_data = st_folium(map,width =925)
    

    

