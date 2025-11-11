import mysql.connector
#mysql.connector sirve para que python realice conexiones con BD:
from tkinter import messagebox
# messagebox es una funcion de la libreria de tkinder

def conectar_bd(): #Defiimos nuetsra funcion para conectar
    try:
        conn = mysql.connector.connect(
            host = "localhost", #Nombre del servidor
            user = "root", # Nombre del usuario
            password = "12345678", # Contraseña
            database = "toks_301" #Nombre de la base de datos
        )
        return conn #Retornamos la conexion
    except mysql.connector.Error as err:
        
        messagebox.showerror("Error", f"No se pudo establecer la conexion con la BD\n{err}")
        return None
    #Si algo sale mal, err guardará exactamente que error se generó
    # mysql.connector.Error indica exactamente cual es el error
    # f"No se pudo establecer la conexion con la BD\n{err}
    # Se muestra ese mensaje de error, junto con el error encontrado
    # return None, si existe error, devuelve None, así el resto
    # del programa sabrá que algo falló