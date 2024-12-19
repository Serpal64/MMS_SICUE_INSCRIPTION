import customtkinter
from pathlib import Path
import sys
from tkinter import messagebox
import sqlite3

# Agrega la ruta del subdirectorio Paquete al listado de rutas donde Python busca módulos para importar. 
# Esto permite usar los módulos dentro del directorio Paquete.
sys.path.append(str(Path(__file__).parent / "Paquete"))
# Importa todas las clases, funciones, variables, etc., definidas en el archivo __init__.py
from Paquete import EspacioAdmin, EspacioEstudiante

# La clase App hereda todos los atributos y funciones de la clase customtkinter.CTk. 
# Esto significa que App es una ventana principal de customtkinter.
class App(customtkinter.CTk):
    # Define el constructor de la clase App, que se ejecuta automáticamente al crear una instancia de App.
    def __init__(self):
        # Llama al constructor de la clase base (customtkinter.CTk) para inicializar correctamente la ventana principal.
        super().__init__()
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.title("Página principal")
        self.geometry("600x450")
        self.resizable(False, False)

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
            # Ponemos lambda para que podamos pasarle argumentos a la función verificar_credenciales
            command=self.verificar_credenciales,
            corner_radius=32,
            width=150,
            height=50
        )
        self.boton_iniciar.pack(pady=5, padx=5)
        self.boton_iniciar.place(relx=0.5, rely=0.7, anchor="center")
        

    def verificar_credenciales(self):
        resultado = None
        
        if self.entrada_usuario.get()=="" or self.entrada_contrasena.get()=="":
            messagebox.showerror("Acceso denegado", "Por favor, introduce el usuario o contraseña")
        else:
            conexion = sqlite3.connect('BaseDeDatos.db')
            cursorBD = conexion.cursor()
            cursorBD.execute(' SELECT rol, idGrado, curso, idUser FROM usuarios WHERE usuario=? AND contrasena=? ', (self.entrada_usuario.get(), self.entrada_contrasena.get()))
            resultado = cursorBD.fetchone()
            conexion.close()

        if not resultado:
            messagebox.showerror("Acceso denegado", "Usuario o Contraseña incorrectos")
        else:
            if resultado[0]=='Administrador':
                self.withdraw()
                EspacioAdmin(self)
            else:
                self.withdraw()
                EspacioEstudiante(self)

    
    
    



