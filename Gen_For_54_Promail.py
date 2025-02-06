import pandas as pd
import streamlit as st
import io

st.title("Generar formato 54 - Promail")

# Cargar archivos desde el usuario
archivo1 = st.file_uploader("Cargar archivo de la Mora", type=['csv'])
archivo2 = st.file_uploader("Cargar archivo a actualizar", type=['csv'])

if archivo1 and archivo2:
    if st.button("Realizar Cruce"):
        try:
            # Leer los archivos CSV
            df1 = pd.read_csv(archivo1)
            df2 = pd.read_csv(archivo2)
            
            # Asegurar que la columna 'Saldo_Factura' sea numérica
            df1['Saldo_Factura'] = pd.to_numeric(df1['Saldo_Factura'], errors='coerce').fillna(0)
            
            # Realizar la sumatoria del 'Saldo_Factura' por 'NIU'
            saldo_factura_dict = df1.groupby('NIU')['Saldo_Factura'].sum().to_dict()
            
            # Asegurarse de que las columnas sean numéricas
            df2['VALOR_MORA'] = pd.to_numeric(df2['VALOR_MORA'], errors='coerce').fillna(0)
            df2['VALOR_TOTAL_FAC'] = pd.to_numeric(df2['VALOR_TOTAL_FAC'], errors='coerce').fillna(0)
            
            # Actualizar el campo 'VALOR_MORA' en df2 con la sumatoria por 'NIU'
            df2['VALOR_MORA'] = df2['NIU'].map(saldo_factura_dict).fillna(df2['VALOR_MORA'])
            
            # Sumar 'VALOR_MORA' al campo 'VALOR_TOTAL_FAC'
            df2['VALOR_TOTAL_FAC'] += df2['VALOR_MORA']
            
            # Manejar los valores vacíos o 'NA' en el campo ID_FACTURA
            df2['ID_FACTURA'] = df2['ID_FACTURA'].replace('', 'NA').fillna('NA')
            
            # Lista de campos a formatear
            campos_a_formatear = [
                'CARGO_INVERSION', 'AMGC_NUM_USUARIOS', 'AMGC_VALOR_INVERSION', 'AMGC_ATENCION',
                'AMGC_NIVEL_FAC', 'CARGO_REMUNERACION', 'VALOR_SUBSIDIO', 'VALOR_TARIFA',
                'FACT_CONSUMO', 'VALOR_TOTAL_FAC', 'VALOR_CARTERA_REC'
            ]
            
            # Asegurarse de que las columnas sean numéricas y formatear a tres decimales
            for campo in campos_a_formatear:
                df2[campo] = pd.to_numeric(df2[campo], errors='coerce').fillna(0)
                df2[campo] = df2[campo].apply(lambda x: f"{x:.3f}")
            
            # Guardar el resultado en un buffer
            output = io.BytesIO()
            df2.to_csv(output, index=False, encoding='utf-8')
            output.seek(0)
            
            # Obtener el nombre del archivo original y modificarlo
            archivo2_nombre = "ZNISISFV_64716_54_" + archivo2.name
            
            # Botón para descargar el archivo actualizado
            st.download_button(label="Descargar archivo actualizado", data=output, file_name=archivo2_nombre, mime="text/csv")
            
            st.success("Actualización completada.")
        except Exception as e:
            st.error(f"Error en el procesamiento de los archivos: {e}")

#############################################################################################################
"""
st.title("Generar formato IUF1")

# Cargar archivos desde el usuario
archivo3 = st.file_uploader("Cargar archivo de la Mora", type=['csv'], key="key_archivo3")
archivo4 = st.file_uploader("Cargar archivo a actualizar", type=['csv'], key="key_archivo4")

# Botón para realizar el cruce de los archivos
if archivo3 and archivo4:
    if st.button("Realizar Cruce"):
        # Leer los archivos CSV
        df1 = pd.read_csv(archivo1)
        df2 = pd.read_csv(archivo2)
        
        # Crear un diccionario para acceder rápidamente a los valores de 'Saldo de Factura'
        saldo_factura_dict = df1.set_index('NIU')['Saldo_Factura'].to_dict()
        
        # Asegurarse de que las columnas sean numéricas
        df2['VALOR_MORA'] = pd.to_numeric(df2['VALOR_MORA'], errors='coerce').fillna(0)
        
        # Actualizar el campo 'VALOR_MORA' en df2 con los valores del diccionario
        df2['VALOR_MORA'] = df2['NIU'].map(saldo_factura_dict).fillna(df2['VALOR_MORA'])
        
        # Manejar los valores vacíos o 'NA' en el campo ID_FACTURA
        df2['ID_FACTURA'] = df2['ID_FACTURA'].replace('', 'NA')
        df2['ID_FACTURA'] = df2['ID_FACTURA'].fillna('NA')
        
        # Guardar el resultado en un buffer
        output = io.BytesIO()
        df2.to_csv(output, index=False, encoding='utf-8')
        output.seek(0)
        
        # Obtener el nombre del archivo original y modificarlo
        archivo2_nombre = "IUF1_" + archivo4.name
        
        # Botón para descargar el archivo actualizado
        st.download_button(label="Descargar archivo actualizado", data=output, file_name=archivo2_nombre, mime="text/csv")
        
        st.success("Actualización completada.") """
