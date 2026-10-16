import psycopg2
from psycopg2 import sql

def obtener_cuartiles_desde_postgres(tabla, campo):
    # 1. Configura la conexión a tu base de datos
    conn = psycopg2.connect(
        dbname="mdm6data",
        user="postgres",
        password="P0stgr3s",
        host="mdm.ivea.local",
        port="5432"
    )
    cursor = conn.cursor()
    
     # Construimos la query usando f-strings limpios.
    # Colocamos comillas dobles "" alrededor de la tabla y el campo por si acaso 
    # el esquema o la columna tienen mayúsculas o caracteres especiales.
    query = f"""
    SELECT 
        percentile_cont(0.25) WITHIN GROUP (ORDER BY "{campo}") AS q1,
        percentile_cont(0.50) WITHIN GROUP (ORDER BY "{campo}") AS q2,
        percentile_cont(0.75) WITHIN GROUP (ORDER BY "{campo}") AS q3
    FROM {tabla};
    """
    
    # Ejecutamos la cadena directa de texto sin pasar parámetros adicionales
    cursor.execute(query)
    q1, q2, q3 = cursor.fetchone()
    
    # 3. Cerrar conexiones
    cursor.close()
    conn.close()
    
    return q1, q2, q3


