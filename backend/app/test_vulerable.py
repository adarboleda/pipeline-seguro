import os
import subprocess

# Ejecución de comandos del sistema operativo (RCE)
def ejecutar_comando(comando_del_usuario):
    os.system(comando_del_usuario)
    subprocess.Popen(comando_del_usuario, shell=True)

# Inyección SQL Clásica (Concatenación de strings insegura)
def buscar_usuario(user_id):
    query = "SELECT * FROM usuarios WHERE id = " + str(user_id)
    return query

# Ejecución de código arbitrario
def evaluar_math(expression):
    return eval(expression)
