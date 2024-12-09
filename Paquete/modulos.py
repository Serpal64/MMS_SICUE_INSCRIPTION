from tkinter.ttk import * 
import tkinter as tk
from tkinter import messagebox
import webbrowser

def verificar_credenciales(usuario, contraseña):

    if usuario == "admin" and contraseña == "1234":
        messagebox.showinfo("Acceso permitido", "Inicio de sesión administrador exitoso")
    elif usuario == "Sergio" and contraseña == "Palacios":
        messagebox.showinfo("Acceso permitido", "Inicio de sesión de estudiante exitoso")
    elif usuario == "" or contraseña == "":
        messagebox.showerror("Acceso denegado", "Por favor, introduce el usuario o contraseña")
    else:
        messagebox.showerror("Acceso denegado", "Usuario o Contraseña incorrectos")

def mostrar_ayuda():

    webbrowser.open("https://www.crue.org/sicue/")

def espacio_alumno():

    ventana_alumno = tk.Tk()
    ventana_alumno.geometry("1600x900")
    ventana_alumno.title("Espacio de alumnos")

    etiqueta = tk.Label(ventana_alumno, text="Este espacio está por definir")
    etiqueta.pack(pady=5, padx=5)

    ventana_alumno.mainloop()