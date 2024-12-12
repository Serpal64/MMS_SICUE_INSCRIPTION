from tkinter.ttk import * 
import tkinter as tk
from tkinter import messagebox
import customtkinter
import webbrowser

# Esta es la ventana que se abre para los estudiantes
class EspacioEstudiante(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("700x500")
        self.title("Estudiante")
        self._set_appearance_mode("Dark")
        self.resizable(False, False)

        # Mensaje de bienvenida
        self.bienvenida = customtkinter.CTkLabel(self, text="Hola Alumno!", font=("Segoe UI", 20))
        self.bienvenida.pack(padx=20, pady=20)
        self.bienvenida.place(relx=0.05, rely=0.05)

        # Botón para consultar planes de convalidación
        self.consultar_inscripción = customtkinter.CTkButton(
            master=self,
            text="Consultar planes",
            font=("Segoe UI", 14),
            command= lambda: self.consultar_inscripciones(),
            corner_radius=32,
            width=150,
            height=50
        )
        self.consultar_inscripción.pack(padx=20, pady=20)
        self.consultar_inscripción.place(relx=0.05, rely=0.2)

        # Botón para realizar las inscripciones
        self.inscribirse = customtkinter.CTkButton(
            master=self,
            text="Inscribirse en un plan",
            font=("Segoe UI", 14),
            command= lambda: self.inscripción(),
            corner_radius=32,
            width=150,
            height=50
        )
        self.inscribirse.pack(padx=20, pady=20)
        self.inscribirse.place(relx=0.4, rely=0.2)

    # Falta implementarlo con la base de datos
    def consultar_inscripciones(self):

        self.texto_consulta = customtkinter.CTkTextbox(self, width=500, height=200, font=("Segoe UI", 14))
        self.texto_consulta.pack(pady=10)
        self.texto_consulta.place(relx=0.05, rely=0.4)

        self.texto_consulta.insert("1.0", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n")
        self.texto_consulta.insert("2.0", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

    # Falta implementarlo con la base de datos
    def inscripción(self):

        self.texto_consulta.destroy()

        self.etiqueta_uni_O = customtkinter.CTkLabel(self, text="Universidad:", font=("Segoe UI", 14))
        self.etiqueta_uni_O.pack(padx=20, pady=20)
        self.etiqueta_uni_O.place(relx=0.05 , rely= 0.4)

        self.entrada_uni_O = customtkinter.CTkEntry(self)
        self.entrada_uni_O.pack(padx=20, pady=20)
        self.entrada_uni_O.place(relx = 0.2, rely = 0.4)

        self.etiqueta_facultad_O = customtkinter.CTkLabel(self, text="Facultad:", font=("Segoe UI", 14))
        self.etiqueta_facultad_O.pack(padx=20, pady=20)
        self.etiqueta_facultad_O.place(relx=0.05 , rely= 0.5)

        self.entrada_facultad_O = customtkinter.CTkEntry(self)
        self.entrada_facultad_O.pack(padx=20, pady=20)
        self.entrada_facultad_O.place(relx = 0.2, rely = 0.5)

        self.etiqueta_grado_O = customtkinter.CTkLabel(self, text="Grado:", font=("Segoe UI", 14))
        self.etiqueta_grado_O.pack(padx=20, pady=20)
        self.etiqueta_grado_O.place(relx=0.05 , rely= 0.6)

        self.entrada_grado_O = customtkinter.CTkEntry(self)
        self.entrada_grado_O.pack(padx=20, pady=20)
        self.entrada_grado_O.place(relx = 0.2, rely = 0.6)

        self.etiqueta_tiempo_O = customtkinter.CTkLabel(self, text="Estancia:", font=("Segoe UI", 14))
        self.etiqueta_tiempo_O.pack(padx=20, pady=20)
        self.etiqueta_tiempo_O.place(relx=0.05 , rely= 0.7)

        self.opcion_tiempo_O = customtkinter.CTkOptionMenu(self, values=["Cuatrimestre", "Curso Completo"], command=None)
        self.opcion_tiempo_O.pack(padx=20, pady=20)
        self.opcion_tiempo_O.place(relx = 0.2, rely = 0.7)

class EspacioAdmin(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("700x500")
        self.title("Administrador")
        self._set_appearance_mode("Dark")
        self.resizable(False, False)

        # Mensaje de bienvenida
        self.bienvenida = customtkinter.CTkLabel(self, text="Modo Administrador", font=("Segoe UI", 20))
        self.bienvenida.pack(padx=20, pady=20)
        self.bienvenida.place(relx=0.05, rely=0.05)

        # Botón para consultar planes de convalidación
        self.crear_plan = customtkinter.CTkButton(
            master=self,
            text="Crear plan de convalidación",
            font=("Segoe UI", 14),
            command= lambda: self.crear_plan(),
            corner_radius=32,
            width=150,
            height=50
        )
        self.crear_plan.pack(padx=20, pady=20)
        self.crear_plan.place(relx=0.05, rely=0.2)
    
    def crearPlan(self):

        self.etiqueta_origen = customtkinter.CTkLabel(self, text="Origen", font=("Segoe UI", 14))
        self.etiqueta_origen.pack(padx=20, pady=20)
        self.etiqueta_origen.place(relx=0.2 , rely= 0.3)

        self.etiqueta_destino = customtkinter.CTkLabel(self, text="Destino", font=("Segoe UI", 14))
        self.etiqueta_destino.pack(padx=20, pady=20)
        self.etiqueta_destino.place(relx=0.4 , rely= 0.3)

        self.etiqueta_uni_O = customtkinter.CTkLabel(self, text="Universidad:", font=("Segoe UI", 14))
        self.etiqueta_uni_O.pack(padx=20, pady=20)
        self.etiqueta_uni_O.place(relx=0.05 , rely= 0.4)

        self.entrada_uni_O = customtkinter.CTkEntry(self)
        self.entrada_uni_O.pack(padx=20, pady=20)
        self.entrada_uni_O.place(relx = 0.2, rely = 0.4)

        self.etiqueta_facultad_O = customtkinter.CTkLabel(self, text="Facultad:", font=("Segoe UI", 14))
        self.etiqueta_facultad_O.pack(padx=20, pady=20)
        self.etiqueta_facultad_O.place(relx=0.05 , rely= 0.5)

        self.entrada_facultad_O = customtkinter.CTkEntry(self)
        self.entrada_facultad_O.pack(padx=20, pady=20)
        self.entrada_facultad_O.place(relx = 0.2, rely = 0.5)

        self.etiqueta_grado_O = customtkinter.CTkLabel(self, text="Grado:", font=("Segoe UI", 14))
        self.etiqueta_grado_O.pack(padx=20, pady=20)
        self.etiqueta_grado_O.place(relx=0.05 , rely= 0.6)

        self.entrada_grado_O = customtkinter.CTkEntry(self)
        self.entrada_grado_O.pack(padx=20, pady=20)
        self.entrada_grado_O.place(relx = 0.2, rely = 0.6)

        self.etiqueta_tiempo_O = customtkinter.CTkLabel(self, text="Estancia:", font=("Segoe UI", 14))
        self.etiqueta_tiempo_O.pack(padx=20, pady=20)
        self.etiqueta_tiempo_O.place(relx=0.05 , rely= 0.7)

        self.opcion_tiempo_O = customtkinter.CTkOptionMenu(self, values=["Cuatrimestre", "Curso Completo"], command=None)
        self.opcion_tiempo_O.pack(padx=20, pady=20)
        self.opcion_tiempo_O.place(relx = 0.2, rely = 0.7)



def verificar_credenciales(usuario, contraseña):

    # Acceso del admin
    if usuario == "admin" and contraseña == "1234":
        messagebox.showinfo("Acceso permitido", "Inicio de sesión administrador exitoso")
    # Acceso de los alumnos
    elif usuario == "Sergio" and contraseña == "Palacios":
        messagebox.showinfo("Acceso permitido", "Inicio de sesión de estudiante exitoso")
    elif usuario == "" or contraseña == "":
        messagebox.showerror("Acceso denegado", "Por favor, introduce el usuario o contraseña")
    else:
        messagebox.showerror("Acceso denegado", "Usuario o Contraseña incorrectos")

def mostrar_ayuda():

    webbrowser.open("https://www.crue.org/sicue/")

def espacio_alumno(parent):
    if parent.toplevel_window is None or not parent.toplevel_window.winfo_exists():
        parent.toplevel_window = EspacioEstudiante(parent)  # Crea una ventana si no está o si está destruida
    else:
        parent.toplevel_window.focus()  # Si existe, que resalte

def espacio_admin(parent):
    if parent.toplevel_window is None or not parent.toplevel_window.winfo_exists():
        parent.toplevel_window = EspacioAdmin(parent)  # Crea una ventana si no está o si está destruida
    else:
        parent.toplevel_window.focus()  # Si existe, que resalte
