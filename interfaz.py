import customtkinter
from PIL import Image, ImageTk
from CTkMenuBar import *
from tkinter import Menu
from pathlib import Path
import sys

# Importar paquete con los módulos
sys.path.append(str(Path(__file__).parent / "Paquete"))
from Paquete import *

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):

    # Función de clase aplicación de la ventana principal
    def __init__(self):
        super().__init__()
        self.title("Página principal")
        self.geometry("600x450")
        self.resizable(False, False)
    


        self.configurar_menu()

        # Configuración del saludo inicial
        self.etiqueta_saludo = customtkinter.CTkLabel(
            master=self, text="Bienvenid@ al Programa MMS", fg_color="transparent", font=("Segoe UI", 14)
        )
        self.etiqueta_saludo.pack(pady=5, padx=5)

        # Entrada para usuario
        self.etiqueta_usuario = customtkinter.CTkLabel(master=self, text="Usuario:", fg_color="transparent", font=("Segoe UI", 14))
        self.etiqueta_usuario.pack(pady=5)
        self.entrada_usuario = customtkinter.CTkEntry(master=self)
        self.entrada_usuario.pack(pady=5)

        # Entrada para contraseña
        self.etiqueta_contrasena = customtkinter.CTkLabel(
            master=self, text="Contraseña:", fg_color="transparent", font=("Segoe UI", 14)
        )
        self.etiqueta_contrasena.pack(pady=5)
        self.entrada_contrasena = customtkinter.CTkEntry(master=self, show="*")
        self.entrada_contrasena.pack(pady=5)

        # Botón para iniciar sesión 
        self.boton_iniciar = customtkinter.CTkButton(
            master=self,
            text="Iniciar sesión",
            font=("Segoe UI", 14),
            command=lambda: verificar_credenciales(self, self.entrada_usuario.get(), self.entrada_contrasena.get()),
            corner_radius=32,
            width=150,
            height=50
        )
        self.boton_iniciar.pack(pady=5, padx=5)
        self.boton_iniciar.place(relx=0.5, rely=0.7, anchor="center")

        # Ventanas emergentes
        self.toplevel_window = None

    # Función para el menú desplegable de la aplicación
    def configurar_menu(self):

        self.menubar = CTkMenuBar(master=self)
        self.Inicio = CustomDropdownMenu(widget=self.menubar.add_cascade("Inicio"))
        self.Ayuda = CustomDropdownMenu(widget=self.menubar.add_cascade("Ayuda"))
        self.Inicio.add_option(option="Administrador", command=None)
        self.Inicio.add_option(option="Estudiante", command=lambda: espacio_alumno(self))
        self.Inicio.add_option(option="Profesor")
        
        self.Ayuda.add_option(option="Manual")
        self.Ayuda.add_separator()
        self.Ayuda.add_option(option="Más información", command=mostrar_ayuda)
    
    
    



