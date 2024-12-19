from tkinter import messagebox
import customtkinter
import webbrowser
import sqlite3


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

# La clase EspacioAdmin hereda todos los atributos y funciones de la clase customtkinter.CTkToplevel (clase base para la ventana secundaria). 
# Esto significa que EspacioAdmin es una ventana secundaria de customtkinter.
class EspacioAdmin(customtkinter.CTkToplevel):
    # Define el constructor de la clase EspacioAdmin, que se ejecuta automáticamente al crear una instancia de la clase EspacioAdmin.
    # master se utiliza para determinar cuál es la ventana principal (puede ser None si no se especifica). 
    def __init__(self, padre):
        # Llama al constructor de la clase base (CTkToplevel). 
        # Esto asegura que la ventana secundaria sea correctamente inicializada como una ventana CTkToplevel.
        super().__init__(padre)
        self.geometry("900x500")
        self.title("Administrador")
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.resizable(False, False)
        self.App = padre

        # Mensaje de bienvenida
        self.bienvenida = customtkinter.CTkLabel(self, text="Modo Administrador", font=("Segoe UI", 20))
        self.bienvenida.pack(padx=20, pady=20)
        self.bienvenida.place(relx=0.05, rely=0.05)

        # Botón para consultar planes de convalidación
        self.crear_plan = customtkinter.CTkButton(
            master=self,
            text="Crear plan de convalidación",
            font=("Segoe UI", 14),
            command= self.crearPlan,
            corner_radius=32,
            width=150,
            height=50,
        )
        self.crear_plan.pack(padx=20, pady=20)
        self.crear_plan.place(relx=0.05, rely=0.15)

        # Botón para cerrar sesión
        self.boton_cerrar = customtkinter.CTkButton(
            master=self,
            text="Cerrar Sesión",
            font=("Segoe UI", 14),
            command=self.volverAtras,
            corner_radius=32,
            width=150,
            height=50,
        )
        self.boton_cerrar.place(relx=0.8, rely=0.02)

        self.frame_contenedor = None
        self.widgets_creados = False
    
    def volverAtras(self):
        self.destroy()
        self.App.entrada_usuario.delete(0, customtkinter.END)
        self.App.entrada_contrasena.delete(0, customtkinter.END)
        self.App.deiconify()  
    
    def crearPlan(self):
        #Etiquetas
        if self.widgets_creados:
            for widgets in self.frame_contenedor.winfo_children():
                widgets.destroy()

        if self.frame_contenedor is None:
            self.frame_contenedor = customtkinter.CTkFrame(self, height=400, fg_color='transparent')
            self.frame_contenedor.pack(fill='x', pady=(130,0))

        self.etiqueta_origen = customtkinter.CTkLabel(self.frame_contenedor, text="Origen", font=("Segoe UI", 14))
        self.etiqueta_origen.pack(padx=20, pady=20)
        self.etiqueta_origen.place(relx=0.2, rely= 0.05)

        self.etiqueta_destino = customtkinter.CTkLabel(self.frame_contenedor, text="Destino", font=("Segoe UI", 14))
        self.etiqueta_destino.pack(padx=20, pady=20)
        self.etiqueta_destino.place(relx=0.6, rely= 0.05)

        self.etiqueta_uni = customtkinter.CTkLabel(self.frame_contenedor, text="Universidad:", font=("Segoe UI", 14))
        self.etiqueta_uni.pack(padx=20, pady=20)
        self.etiqueta_uni.place(relx=0.05 , rely= 0.2)

        self.etiqueta_centro = customtkinter.CTkLabel(self.frame_contenedor, text="Centro:", font=("Segoe UI", 14))
        self.etiqueta_centro.pack(padx=20, pady=20)
        self.etiqueta_centro.place(relx=0.05 , rely= 0.35)

        self.etiqueta_grado = customtkinter.CTkLabel(self.frame_contenedor, text="Grado:", font=("Segoe UI", 14))
        self.etiqueta_grado.pack(padx=20, pady=20)
        self.etiqueta_grado.place(relx=0.05 , rely= 0.5)

        self.etiqueta_duracion = customtkinter.CTkLabel(self.frame_contenedor, text="Duracion:", font=("Segoe UI", 14))
        self.etiqueta_duracion.pack(padx=20, pady=20)
        self.etiqueta_duracion.place(relx=0.05 , rely= 0.65)

        self.etiqueta_curso = customtkinter.CTkLabel(self.frame_contenedor, text="Curso:", font=("Segoe UI", 14))
        self.etiqueta_curso.pack(padx=20, pady=20)
        self.etiqueta_curso.place(relx=0.05 , rely= 0.8)

        self.entrada_uni_O = customtkinter.CTkLabel(self.frame_contenedor, text="Universidad de Córdoba (UCO)", font=("Segoe UI", 14))
        self.entrada_uni_O.pack(padx=20, pady=20)
        self.entrada_uni_O.place(relx = 0.2, rely = 0.2)

        # Botones
        from Paquete import Universidades, Centros

        self.entrada_uni_D = customtkinter.CTkOptionMenu(self.frame_contenedor, values=["Seleccione una opción"])
        self.entrada_uni_D.pack(padx=20, pady=20)
        self.entrada_uni_D.place(relx = 0.6, rely = 0.2)
        Universidades(self.entrada_uni_D)
        self.entrada_uni_D.configure(command=self.actualizar_centros)
        

        self.entrada_centro_O = customtkinter.CTkOptionMenu(self.frame_contenedor, values=["Seleccione una opción"])
        self.entrada_centro_O.pack(padx=20, pady=20)
        self.entrada_centro_O.place(relx = 0.2, rely = 0.35)
        Centros(self.entrada_centro_O, "Universidad de Córdoba (UCO)")
        self.entrada_centro_O.configure(command=self.actualizar_grados)

        self.entrada_centro_D = customtkinter.CTkOptionMenu(self.frame_contenedor, values=["Seleccione una opción"])
        self.entrada_centro_D.pack(padx=20, pady=20)
        self.entrada_centro_D.place(relx = 0.6, rely = 0.35)
        self.entrada_centro_D.configure(command=self.actualizar_grados)

        self.entrada_grado_O = customtkinter.CTkOptionMenu(self.frame_contenedor, values=["Seleccione una opción"])
        self.entrada_grado_O.pack(padx=20, pady=20)
        self.entrada_grado_O.place(relx = 0.2, rely = 0.5)

        self.entrada_grado_D = customtkinter.CTkOptionMenu(self.frame_contenedor, values=["Seleccione una opción"])
        self.entrada_grado_D.pack(padx=20, pady=20)
        self.entrada_grado_D.place(relx = 0.6, rely = 0.5)

        self.opcion_tiempo = customtkinter.CTkOptionMenu(self.frame_contenedor, values=["Seleccione una opción","1º Cuatrimestre", "2º Cuatrimestre","Curso Completo"])
        self.opcion_tiempo.pack(padx=20, pady=20)
        self.opcion_tiempo.place(relx = 0.2, rely = 0.65)

        self.opcion_curso = customtkinter.CTkOptionMenu(self.frame_contenedor, values=["Seleccione una opción","2º", "3º","4º", "5º", "6º"])
        self.opcion_curso.pack(padx=20, pady=20)
        self.opcion_curso.place(relx = 0.2, rely = 0.8)

        #Botón para ir a la ventana de equivalencia de asignaturas
        self.boton_siguiente = customtkinter.CTkButton(
            master=self.frame_contenedor,
            text="Siguiente",
            font=("Segoe UI", 14),
            command= self.siguienteVentana,
            corner_radius=32,
            width=150,
            height=50
        )
        self.boton_siguiente.pack(padx=20, pady=20)
        self.boton_siguiente.place(relx=0.6, rely=0.75)

        self.widgets_creados = True
    
    def siguienteVentana(self):
        if self.entrada_uni_D.get()=="Seleccione una opción" or self.entrada_centro_O.get()=="Seleccione una opción" or\
        self.entrada_centro_D.get()=="Seleccione una opción" or self.entrada_grado_O.get()=="Seleccione una opción" or \
        self.entrada_grado_D.get()=="Seleccione una opción":
           messagebox.showwarning("Error", "Por favor, rellena todos los campos")
        else:
            self.withdraw()
            EspacioAsignaturas(self)

    def actualizar_centros(self, universidad):
        from Paquete import Centros
        self.entrada_centro_D.set("Seleccione una opción")
        self.entrada_grado_D.set("Seleccione una opción")
        Centros(self.entrada_centro_D, universidad)

    def actualizar_grados(self, centro):
        from Paquete import Grados
        if centro==self.entrada_centro_O.get():
            self.entrada_grado_O.set("Seleccione una opción")
            Grados(self.entrada_grado_O, centro)
        else:
            self.entrada_grado_D.set("Seleccione una opción")
            Grados(self.entrada_grado_D, centro)


class EspacioAsignaturas(customtkinter.CTkToplevel):
    def __init__(self, EspacioAdmin):
        super().__init__(EspacioAdmin)
        self.title("Equivalencias de Asignaturas")
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.resizable(False, False)

        self.EspacioAdmin = EspacioAdmin

        if EspacioAdmin.opcion_tiempo.get() == "Curso Completo":
            self.nAsignaturas = 20
            self.geometry("1000x700")
            self.espacio_vertical = 0.04
            self.plus = 0.02
        else:
            self.nAsignaturas = 10
            self.geometry("1000x500")
            self.espacio_vertical = 0.06
            self.plus = 0.03

        self.etiqueta_titulo = customtkinter.CTkLabel(self, text="Asignaturas", font=("Segoe UI", 25))
        self.etiqueta_titulo.place(relx=0.42, rely=0.02)

        self.etiqueta_universidad_O = customtkinter.CTkLabel(self, text=f"Universidad de Origen: {self.EspacioAdmin.entrada_uni_O.cget('text')}", font=("Segoe UI", 14))
        self.etiqueta_universidad_O.place(relx=0.05, rely= 0.08)

        self.etiqueta_universidad_D = customtkinter.CTkLabel(self, text=f"Universidad de Destino: {self.EspacioAdmin.entrada_uni_D.get()}", font=("Segoe UI", 14))
        self.etiqueta_universidad_D.place(relx=0.55, rely= 0.08)

        self.etiqueta_centro_O = customtkinter.CTkLabel(self, text=f"Centro de Origen: {self.EspacioAdmin.entrada_centro_O.get()}", font=("Segoe UI", 14))
        self.etiqueta_centro_O.place(relx=0.05, rely= 0.08+self.espacio_vertical)

        self.etiqueta_centro_D = customtkinter.CTkLabel(self, text=f"Centro de Destino: {self.EspacioAdmin.entrada_centro_D.get()}", font=("Segoe UI", 14))
        self.etiqueta_centro_D.place(relx=0.55, rely= 0.08+self.espacio_vertical)

        self.etiqueta_grado_O = customtkinter.CTkLabel(self, text=f"Grado de Origen: {self.EspacioAdmin.entrada_grado_O.get()}", font=("Segoe UI", 14))
        self.etiqueta_grado_O.place(relx=0.05, rely= 0.08 + 2*self.espacio_vertical)

        self.etiqueta_grado_D = customtkinter.CTkLabel(self, text=f"Grado de Destino: {self.EspacioAdmin.entrada_grado_D.get()}", font=("Segoe UI", 14))
        self.etiqueta_grado_D.place(relx=0.55, rely= 0.08 + 2*self.espacio_vertical)

        self.etiqueta_curso = customtkinter.CTkLabel(self, text=f"Curso: {self.EspacioAdmin.opcion_curso.get()}", font=("Segoe UI", 14))
        self.etiqueta_curso.place(relx=0.05, rely= 0.08 + 3*self.espacio_vertical)

        self.etiqueta_tiempo = customtkinter.CTkLabel(self, text=f"Duración: {self.EspacioAdmin.opcion_tiempo.get()}", font=("Segoe UI", 14))
        self.etiqueta_tiempo.place(relx=0.55, rely= 0.08 + 3*self.espacio_vertical)

        self.entradasAsignaturas(0.15, 0.08 + 5*self.espacio_vertical)
        
    def entradasAsignaturas(self,  x, y):
        self.listaAsignaturas = []
        for i in range(self.nAsignaturas):
            if i == (self.nAsignaturas/2):
                x = 0.7
                y = 0.08 + 5*self.espacio_vertical
            if i < (self.nAsignaturas/2):
                self.etiqueta_asignatura = customtkinter.CTkLabel(master=self, text=f'--------------- Asignatura {i+1} ---------------')
                self.etiqueta_asignatura.place(relx=0.41, rely= y)       
            entrada_asignatura =customtkinter.CTkEntry(master=self)
            entrada_asignatura.place(relx=x, rely= y)
            self.listaAsignaturas.append(entrada_asignatura)

            y = y + self.espacio_vertical + self.plus

        y = y + self.plus
        self.boton_crear_plan = customtkinter.CTkButton(
            master=self,
            text="Crear plan de convalidación",
            font=("Segoe UI", 14),
            command= self.CrearPlan,
            corner_radius=32,
            width=150,
            height=50
        )
        self.boton_crear_plan.pack(padx=20, pady=20)
        self.boton_crear_plan.place(relx=0.5, rely=y)

        self.boton_atras = customtkinter.CTkButton(
            master=self,
            text="Atrás",
            font=("Segoe UI", 14),
            command= self.volverAtras,
            corner_radius=32,
            width=150,
            height=50
        )
        self.boton_atras.pack(padx=20, pady=20)
        self.boton_atras.place(relx=0.3, rely=y)

    def volverAtras(self):
        self.destroy()
        self.EspacioAdmin.deiconify()

    def CrearPlan(self):
        from Paquete import crearAsignaturas, equivalenciasAsignaturas, crearConvenio
        asignaturas = [asignatura.get() for asignatura in self.listaAsignaturas]
        for asignatura in asignaturas:
            if asignatura == "":
                messagebox.showwarning('Campos incompletos', 'Por favor, rellene todos los campos')
                return
        gradoOrigen = self.EspacioAdmin.entrada_grado_O.get()
        gradoDestino = self.EspacioAdmin.entrada_grado_D.get()
        curso = self.EspacioAdmin.opcion_curso.get()
        duracion = self.EspacioAdmin.opcion_tiempo.get()
        if duracion == "1º Cuatrimestre":
            duracion = "1_cuatri"
        elif duracion == "2º Cuatrimestre":
            duracion = "2_cuatri"
        else:
            duracion = "curso_completo"
        idConvenio = crearConvenio(gradoOrigen, gradoDestino, curso, duracion)
        if idConvenio != 0:
            IdAsignaturas = crearAsignaturas(asignaturas, gradoOrigen, gradoDestino, self.nAsignaturas, curso)
            equivalenciasAsignaturas(idConvenio, IdAsignaturas, self.nAsignaturas)
        self.EspacioAdmin.frame_contenedor.destroy()
        self.EspacioAdmin.widgets_creados = False
        self.EspacioAdmin.frame_contenedor = None
        self.EspacioAdmin.deiconify()
        self.destroy()
