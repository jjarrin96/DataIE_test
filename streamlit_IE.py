import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.header("Reporte Prueba")

dtype_dict = {
    'Mes':str,
    'Total Nacional':float,
    'Agricultura, ganadería y pesca':float,
    'Minas y canteras':float,
    'Manufactura':float,
    'Suministro de Electricidad Gas Vapor y Aire acondicionado':float,
    'Distribución de Agua Alcantarillado y gestión de desechos':float,
    'Construcción':float,
    'Comercio':float,
    'Transporte y almacenamiento':float,
    'Actividades de Alojamiento':float,
    'Información y comunicación':float,
    'Financieras y seguros':float,
    'Actividades inmobiliarias':float,
    'Actividades profesionales':float,
    'Actividades de servicios administrativos y de apoyo':float,
    'Administración pública y defensa':float,
    'Enseñanza':float,
    'Actividades de atención a salud':float,
    'Actividades entretenimiento':float,
    'Otras actividades de servicios':float,
    'Actividades de los hogares como empleadores domésticos':float,
    'Actividades de Organizaciones':float

}
# Datos cargados
df_ventas = pd.read_csv("https://raw.githubusercontent.com/jjarrin96/DataIE_test/main/Datos/v_py.csv", sep=';')
df_ventas.set_index(df_ventas.columns[0], inplace=True)

df_empresas = pd.read_csv("https://raw.githubusercontent.com/jjarrin96/DataIE_test/main/Datos/ranking.csv", sep=';')
# Agregar la barra de filtro al principio de la aplicación
selected_column = st.selectbox('Selecciona una columna', df_ventas.columns)

# Filtrar el DataFrame según la columna seleccionada
filtered_df = df_ventas[[selected_column]]

# Mostrar los datos filtrados
# st.dataframe(filtered_df)

# creación de periodos

st.subheader("Resumen")

# seccion 1 - grafico

current_month = 5
periods = (2023-2011)*12 + current_month

# Configurar las columnas en Streamlit
col1, col2 = st.columns(2)

# Crear el gráfico de serie de tiempo utilizando plotly en la columna izquierda
with col1:
    # Crear el gráfico de serie de tiempo utilizando plotly
    fig = go.Figure()

    # Línea continua hasta cierto mes
    fig.add_trace(go.Scatter(
        x=filtered_df.index[:periods],
        y=filtered_df[selected_column][:periods],
        mode='lines',
        name='Línea continua',
        showlegend=False
    ))

    # Línea punteada a partir de cierto mes
    fig.add_trace(go.Scatter(
        x=filtered_df.index[periods:],
        y=filtered_df[selected_column][periods:],
        mode='lines',
        name='Pronósticos',
        line=dict(dash='dash'),
        showlegend=False
    ))

    fig.update_layout(
        title='Gráfico de Serie de Tiempo de Ventas',
        xaxis_title='Fecha',
        yaxis_title='Ventas (USD MM)'
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

# Resto del código en la columna derecha
with col2:
    # Aquí puedes agregar contenido adicional en la columna derecha
    st.markdown(f"<span style='font-size: 18px;'><strong>Listado de empresas del sector {selected_column}</strong></span>", unsafe_allow_html=True)

    # Filtrar la tabla de empresas según la categoría seleccionada
    df_filtrado = df_empresas.loc[df_empresas['rama'] == selected_column]
    df_filtrado.set_index(df_filtrado.columns[2],inplace=True)

    # Mostrar la tabla filtrada
    st.dataframe(df_filtrado)


# seccion 2

st.subheader("Resumen")

st.write(df_ventas.iloc[:,1:].head()
           )

st.title("Metada")

st.markdown("Aquí se ingresará texto sobre el ciiu. Ejemplo si es comercio \n pondrá algo como comercio es el actividad de comerciantes o algo así. Pendiente definir que detalle")

st.markdown("Texto sobre el sector")

# seccion 3 

st.title("Pronósticos Corto Plazo")

cp_s1 = pd.read_csv("https://raw.githubusercontent.com/jjarrin96/DataIE_test/main/Datos/cp_s1.csv", sep=';',dtype=dtype_dict,thousands=',')
cp_s2 = pd.read_csv("https://raw.githubusercontent.com/jjarrin96/DataIE_test/main/Datos/cp_s2.csv", sep=';',dtype=dtype_dict,thousands=',')
cp_s3 = pd.read_csv("https://raw.githubusercontent.com/jjarrin96/DataIE_test/main/Datos/cp_s3.csv", sep=';', dtype=dtype_dict,thousands=',')

cp_s1.set_index(cp_s1.Mes, inplace=True)
cp_s2.set_index(cp_s2.Mes, inplace=True)
cp_s3.set_index(cp_s3.Mes, inplace=True)

combined_df = pd.concat([cp_s1[selected_column], cp_s2[selected_column], cp_s3[selected_column]], axis=1)
combined_df.columns = ["Escenario Pesimista", "Escenario normal", "Escenario Optimista"]

meses_esp_ingles = {
    'ene': 'Jan',
    'feb': 'Feb',
    'mar': 'Mar',
    'abr': 'Apr',
    'may': 'May',
    'jun': 'Jun',
    'jul': 'Jul',
    'ago': 'Aug',
    'sep': 'Sep',
    'oct': 'Oct',
    'nov': 'Nov',
    'dic': 'Dec'
}

combined_df.index = combined_df.index.map(lambda fecha: meses_esp_ingles[fecha.split()[0]] + ' ' + fecha.split()[1])

# Convertir el índice a tipo datetime
combined_df.index = pd.to_datetime(combined_df.index, format='%b %Y')


# Obtener los datos antes y después de mayo de 2023
pre_may_data = combined_df.loc[combined_df.index < pd.to_datetime("2023-05-01")]
post_may_data = combined_df.loc[combined_df.index >= pd.to_datetime("2023-05-01")]


col1, col2 = st.columns(2)

with col1:
        
    # Crear el gráfico de líneas con Plotly
    fig = go.Figure()

    # Agregar las líneas correspondientes a cada DataFrame al gráfico
    for column in combined_df.columns:
        # Línea sólida para los datos anteriores a mayo de 2023
        fig.add_trace(go.Scatter(x=cp_s1["Mes"], y=combined_df[column], name=column))

    # Configurar el diseño del gráfico
    fig.update_layout(title=f"Gráfico de {selected_column} USD MM ",
                    xaxis_title="Mes",
                    yaxis_title=selected_column)

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

# Crear un contenedor para combinar col1 y col2
container = st.container()

col1,col3 = st.columns(2)

with col1: 

    cp_s1[selected_column] = pd.to_numeric(cp_s1[selected_column], errors='coerce')
    cp_s2[selected_column] = pd.to_numeric(cp_s2[selected_column], errors='coerce')
    cp_s3[selected_column] = pd.to_numeric(cp_s3[selected_column], errors='coerce')

    # Calcular las variaciones interanuales
    df1_diff = cp_s1[selected_column].pct_change(periods=12) * 100
    df2_diff = cp_s2[selected_column].pct_change(periods=12) * 100
    df3_diff = cp_s3[selected_column].pct_change(periods=12) * 100
    # Calcular las variaciones interanuales
    df1_diff = cp_s1[selected_column].pct_change(periods=12) * 100
    df2_diff = cp_s2[selected_column].pct_change(periods=12) * 100
    df3_diff = cp_s3[selected_column].pct_change(periods=12) * 100

    # Crear un DataFrame combinado con las variaciones interanuales
    combined_diff = pd.concat([df1_diff, df2_diff, df3_diff], axis=1)
    combined_diff.columns = ["Escenario Pesimista", "Escenario Normal", "Escenario Optimista"]

    # Obtener el primer período con datos
    start_date = combined_diff.dropna().index[0]

    # Filtrar los datos a partir del primer período con datos
    combined_diff = combined_diff.loc[start_date:]

    # Crear el gráfico de líneas con Plotly
    fig = go.Figure()

    # Agregar las líneas correspondientes a cada DataFrame al gráfico
    for column in combined_diff.columns:
        fig.add_trace(go.Scatter(x=combined_diff.index, y=combined_diff[column], name=column))

    # Configurar el diseño del gráfico
    fig.update_layout(title=f"Variaciones interanuales de {selected_column}",
                    xaxis_title="Mes",
                    yaxis_title="Variación Interanual (%)")

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

with col2:
        # Título del escenario optimista
    st.subheader("Escenario Optimista")
    
    # Descripción del escenario optimista
    st.write("Escenario optimista: En este escenario, se espera un panorama favorable y prometedor. Se prevé un crecimiento sólido y sostenido en el futuro. En términos económicos, implica un aumento significativo en la demanda y una expansión en los mercados. Las inversiones y el gasto de los consumidores se incrementan, lo que impulsa la producción y genera empleo. Las empresas experimentan un aumento en sus beneficios y confían en el crecimiento continuo. Este escenario tiende a ser caracterizado por una actitud positiva, confianza en el futuro y una mayor disposición al riesgo.")

with col2:
    # Título del escenario normal
    st.subheader("Escenario Normal")
    
    # Descripción del escenario normal
    st.write("Escenario normal: El escenario normal se encuentra entre los extremos del escenario optimista y pesimista. En este caso, se espera un crecimiento económico moderado y estable. Los indicadores económicos se mantienen en niveles predecibles y dentro de los rangos históricos. Existe un equilibrio entre la oferta y la demanda, y la economía opera en condiciones habituales. No hay eventos disruptivos significativos que afecten el curso esperado de los negocios y las finanzas. Las empresas siguen funcionando de manera estable, los empleos están relativamente asegurados y los consumidores mantienen un nivel de confianza razonable.")

# Escenario Pesimista
with col3:
    # Título del escenario pesimista
    st.subheader("Escenario Pesimista")
    
    # Descripción del escenario pesimista
    st.write("Escenario pesimista: En contraste con el escenario optimista, el escenario pesimista refleja un panorama desalentador y desfavorable. Se anticipa un crecimiento lento o incluso una contracción económica. Puede estar influenciado por factores como crisis económicas, conflictos geopolíticos, cambios en las políticas gubernamentales o desastres naturales. En este escenario, hay una disminución en la demanda y la actividad económica. Las empresas pueden enfrentar dificultades financieras, lo que lleva a recortes de empleo y reducción de inversiones. La confianza de los consumidores disminuye y prevalece una actitud de cautela y aversión al riesgo.")

# seccion largo plazo 

st.title("Pronósticos de Largo Plazo")

lp_s1 = pd.read_csv("https://raw.githubusercontent.com/jjarrin96/DataIE_test/main/Datos/lp_s1.csv", sep=';', dtype=dtype_dict, thousands=',')
lp_s2 = pd.read_csv("https://raw.githubusercontent.com/jjarrin96/DataIE_test/main/Datos/lp_s2.csv", sep=';', dtype=dtype_dict, thousands=',')
lp_s3 = pd.read_csv("https://raw.githubusercontent.com/jjarrin96/DataIE_test/main/Datos/lp_s3.csv", sep=';', dtype=dtype_dict, thousands=',')


lp_s1.set_index(lp_s1.Mes, inplace=True)
lp_s2.set_index(lp_s2.Mes, inplace=True)
lp_s3.set_index(lp_s3.Mes, inplace=True)


combined_df = pd.concat([lp_s1[selected_column], lp_s2[selected_column], lp_s3[selected_column]], axis=1)
combined_df.columns = ["Escenario Pesimista", "Escenario normal", "Escenario Optimista"]


combined_df.index = combined_df.index.map(lambda fecha: meses_esp_ingles[fecha.split()[0]] + ' ' + fecha.split()[1])

# Convertir el índice a tipo datetime
combined_df.index = pd.to_datetime(combined_df.index, format='%b %Y')
combined_df = combined_df.groupby(pd.DatetimeIndex(combined_df.index).year).sum()

col1, col2 = st.columns(2)
# Crear el gráfico de líneas con Plotly
fig = go.Figure()

with col1: 
    for column in combined_df.columns:
        fig.add_trace(go.Scatter(x=combined_df.index, y=combined_df[column], name=column))

    # Configurar el diseño del gráfico
    fig.update_layout(title=f"Series Anuales de {selected_column} USD MM",
                    xaxis_title="Año",
                    yaxis_title="Suma Anual",
                    legend_title="Escenarios")

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)


with col2: 
    combined_df = combined_df.pct_change().mul(100)

    # Crear el gráfico de líneas con Plotly
    fig = go.Figure()

    # Agregar las series al gráfico
    for column in combined_df.columns:
        fig.add_trace(go.Scatter(x=combined_df.index, y=combined_df[column], name=column))

    # Configurar el diseño del gráfico
    fig.update_layout(title=f"Variaciones Anuales de {selected_column}",
                    xaxis_title="Año",
                    yaxis_title="Variación Anual (%)",
                    legend_title="Escenarios")

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)


# sección provincias 

st.title("Ventas por geografía")

mapa = pd.read_csv("https://raw.githubusercontent.com/jjarrin96/DataIE_test/main/Datos/v_mapa.csv", sep = ";")

st.dataframe(mapa)


# sección empresas
st.title("Ratios del sector")


data = {
    'Empresa': ['Empresa 1', 'Empresa 2', 'Empresa 3', 'Empresa 4', 'Empresa 5', 'Empresa 6', 'Empresa 7', 'Empresa 8', 'Empresa 9', 'Empresa 10',
                'Empresa 11', 'Empresa 12', 'Empresa 13', 'Empresa 14', 'Empresa 15', 'Empresa 16', 'Empresa 17', 'Empresa 18', 'Empresa 19', 'Empresa 20'],

}

df = pd.DataFrame(data)

