import customtkinter
from CTkMenuBar import *
from tkinter import Menu
from pathlib import Path
import sys


sys.path.append(str(Path(__file__).parent / "Paquete"))
from Paquete import *

class App(customtkinter.CTk):

    # Función de clase aplicación de la ventana principal
    def __init__(self, verificar_credenciales):
        super().__init__()
        self.title("Página principal")
        self.geometry("600x450")
        self.resizable(False, False)

        # Modo de la aplicación
        self._set_appearance_mode("Light")
        self.configurar_menu()

        # Configuración del saludo inicial
        self.etiqueta_saludo = customtkinter.CTkLabel(
            master=self, text="Bienvenid@ al Programa SICUE"
        )
        self.etiqueta_saludo.pack(pady=5, padx=5)

        # Entrada para usuario
        self.etiqueta_usuario = customtkinter.CTkLabel(master=self, text="Usuario:")
        self.etiqueta_usuario.pack(pady=5)
        self.entrada_usuario = customtkinter.CTkEntry(master=self)
        self.entrada_usuario.pack(pady=5)

        # Entrada para contraseña
        self.etiqueta_contrasena = customtkinter.CTkLabel(
            master=self, text="Contraseña:"
        )
        self.etiqueta_contrasena.pack(pady=5)
        self.entrada_contrasena = customtkinter.CTkEntry(master=self, show="*")
        self.entrada_contrasena.pack(pady=5)

        # Botón para iniciar sesión 
        self.boton_iniciar = customtkinter.CTkButton(
            master=self,
            text="Iniciar sesión",
            command=lambda: verificar_credenciales(self.entrada_usuario.get(), self.entrada_contrasena.get()),
        )
        self.boton_iniciar.pack(pady=5, padx=5)
        
    
    def configurar_menu(self):

        self.menubar = CTkMenuBar(master=self)
        self.inicio_button = customtkinter.CTkButton(self, text="Inicio", command=lambda: None)
        self.inicio_button.pack(side="top")
        self.ayuda_button = customtkinter.CTkButton(self, text="Ayuda", command=lambda: None)
        self.ayuda_button.pack(side="top")
        self.Inicio = CustomDropdownMenu(widget=self.inicio_button)
        self.Ayuda = CustomDropdownMenu(widget=self.ayuda_button)
        self.menubar.add_cascade("Inicio", self.inicio_button)
        self.Inicio.add_option(option="Administrador")
        self.Inicio.add_option(option="Estudiante")
        self.Inicio.add_option(option="Profesor")
        self.menubar.add_cascade("Ayuda", self.ayuda_button)
        self.Ayuda.add_option(option="Manual")
        self.Ayuda.add_separator()
        self.Ayuda.add_option(option="Más información", command=mostrar_ayuda)


