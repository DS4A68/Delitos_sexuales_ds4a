from turtle import width
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas
import branca
from shapely import wkt
from shapely.geometry.multipolygon import MultiPolygon
import re
from unicodedata import normalize
from folium.plugins import TimeSliderChoropleth



#st.set_page_config(layout = "wide")
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


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

# GEOMAP 1 


data_geo = pd.read_csv('geojson\gata_geo.csv')
geo_ = geopandas.read_file('geojson\colombia.geo.json')
merged = pd.merge(data_geo,geo_, left_on ='DEPARTAMENTO', right_on= 'NOMBRE_DPT', how = 'left')
merged_ = merged.copy()
s = []
for i in merged_['geometry']:
    try:
        m = MultiPolygon([i])
        s.append(m.wkt)
    except:
        s.append(i.wkt)

merged_['geometry']= s
merged_['geometry'] = merged_['geometry'].apply(wkt.loads)
_merged_ = geopandas.GeoDataFrame(merged_, crs = 'epsg:4326')



# GEOMAP 2



orig = geo_.copy()
s_ = []
for i in orig['geometry']:
    try:
        m = MultiPolygon([i])
        s_.append(m.wkt)
    except:
        s_.append(i.wkt)
orig['geometry']= s_
orig['geometry'] = orig['geometry'].apply(wkt.loads)
_orig_ = geopandas.GeoDataFrame(orig, crs = 'epsg:4326')
dept_count_grouped_year = pd.read_csv("geojson\dept_count_grouped_year.csv")





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


    min_cn, max_cn = merged['CANTIDAD'].quantile([0.01,0.99]).apply(round,2)
    colormap = branca.colormap.LinearColormap(
        colors = ['white','yellow','orange','red','darkred'],
        vmin = min_cn,
        vmax = max_cn
    )


    map = folium.Map(location=[6.258679441576251, -75.55570032068375],
                            zoom_start=6,
                            tiles="OpenStreetMap")

    style_function = lambda x: {
        'fillColor': colormap(x['properties']['CANTIDAD']),
        'color': 'black',
        'weight':2,
        'fillOpacity':0.1
    }

    merged__ = _merged_.drop(['FECHA HECHO','CODIGO DANE','DPTO','NOMBRE_DPT','AREA','PERIMETER','HECTARES'],axis=1)
    
    colombia_geo = folium.GeoJson(
        merged__.to_json(),
        name = "Colombian Crimes",
        style_function= style_function,
        tooltip= folium.GeoJsonTooltip(
            fields = ['DEPARTAMENTO','CANTIDAD'],
            aliases= ['DEPARTAMENT','COUNT'],
            localize = True
        )
    ).add_to(map)
    colormap.add_to(map)

    


    
    #st_data = st_folium(map,width =925)
    #st.markdown("<hr>,",unsafe_allow_html=True)



    # ---------------------------------------------------------------------------


    def folium_slider(count_,
                    _orig_,
                    tmp_drange,
                    index_var,
                    index_lab,
                    value_var ="CANTIDAD",
                    caption = "EVENTOS DE VIOLENCIA SEXUAL EN COLOMBIA"):
        
        #GET COLORBAR:
        min_cn, max_cn = count_['CANTIDAD'].quantile([0.01,0.99]).apply(round,2)
        colormap = branca.colormap.LinearColormap(
            colors = ['white','yellow','orange','red','darkred'],
            vmin = min_cn,
            vmax = max_cn
        )
        colormap.caption = caption
        
        #GET STYLEDATA
        styledata = {}            
        for departamento_ in range(_orig_.shape[0]):
            res_departamento = count_[count_['DEPARTAMENTO'] == _orig_.iloc[departamento_,:]['NOMBRE_DPT']]
            #fill missing value by zero: no recorded crime that month
            c_count = res_departamento.set_index(index_var)[value_var].reindex(tmp_drange).fillna(0)
            df_tmp = pd.DataFrame(
                {'color': [colormap(count) for count in c_count], 'opacity':0.7},
                index = index_lab
            )
            styledata[str(departamento_)] = df_tmp
            
        styledict = {str(departamento_): data.to_dict(orient='index') for departamento_, data in styledata.items()}
    
        # Plot map
        map_ = folium.Map(location=[6.258679441576251, -75.55570032068375],
                            zoom_start=5,
                            tiles="OpenStreetMap")
        
        g = TimeSliderChoropleth(
            _orig_.to_json(),
            styledict=styledict
        ).add_to(map_)
        
        folium.GeoJson(_orig_.to_json(), style_function = lambda x: {
            'color': 'black',
            'weight':2,
            'fillOpacity':0
        }, tooltip=folium.GeoJsonTooltip(
                fields=['NOMBRE_DPT'],
                aliases=['DEPARTAMENTO'], 
                localize=True
            )).add_to(map_)
        
        
        colormap.add_to(map_)
        return map_






    st_data_ = st_folium(
        folium_slider(count_ = dept_count_grouped_year ,
              _orig_ = _orig_,
              tmp_drange = list(range(2010,2023,1)) ,
              index_var = 'year',
              index_lab =list(range(2010,2023,1)) ,
              value_var ="CANTIDAD",
              caption = "EVENTOS DE VIOLENCIA SEXUAL EN COLOMBIA"),width =1024)




    

