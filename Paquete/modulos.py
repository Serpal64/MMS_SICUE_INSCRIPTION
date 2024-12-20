from tkinter import messagebox
import customtkinter
import webbrowser
import sqlite3


# Esta es la ventana que se abre para los estudiantes
class EspacioEstudiante(customtkinter.CTkToplevel):
    def __init__(self, padre):
        super().__init__(padre)
        self.geometry("1200x500")
        self.title("Estudiante")
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.resizable(False, False)
        self.app = padre

        # Vector para eliminar widgets
        self.vector_borrar_widgets = []

        # Obtener idUsuario
        conexion = sqlite3.connect('BaseDeDatos.db')
        cursorBD = conexion.cursor()

        cursorBD.execute('SELECT idUser FROM usuarios WHERE usuario=?', (self.app.entrada_usuario.get(),))
        resultado = cursorBD.fetchone()
        idUsuario = resultado[0]
        self.idUsuario = idUsuario
        conexion.close()

        # Mensaje de bienvenida
        self.bienvenida = customtkinter.CTkLabel(self, text="¡Hola "+self.app.entrada_usuario.get()+"!", font=("Segoe UI", 20))
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
        self.consultar_inscripción.place(relx=0.05, rely=0.2)

        # Botón para realizar las inscripciones
        self.inscribirse = customtkinter.CTkButton(
            master=self,
            text="Inscribirse en un plan",
            font=("Segoe UI", 14),
            command= lambda: self.elegir_plan(),
            corner_radius=32,
            width=150,
            height=50
        )
        self.inscribirse.place(relx=0.4, rely=0.2)

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
        self.boton_cerrar.place(relx=0.85, rely=0.02)

        # Botón para anular las inscripciones
        self.anular = customtkinter.CTkButton(
            master=self,
            text="Anular inscripción",
            font=("Segoe UI", 14),
            command= lambda: self.anular_inscripción(),
            corner_radius=32,
            width=150,
            height=50
        )
        self.anular.place(relx=0.75, rely=0.2)
    
    def borrar_widgets(self):
        for widget in self.vector_borrar_widgets:
            widget.destroy()
        self.vector_borrar_widgets.clear()
    
    def volverAtras(self):
        self.destroy()
        self.app.entrada_usuario.delete(0, customtkinter.END)
        self.app.entrada_contrasena.delete(0, customtkinter.END)
        self.app.deiconify()

    def consultar_inscripciones(self):

        self.borrar_widgets()

        self.texto_consulta = customtkinter.CTkTextbox(self, width=1000, height=200, font=("Segoe UI", 14))
        self.texto_consulta.pack(pady=10)
        self.texto_consulta.place(relx=0.05, rely=0.4)
        self.vector_borrar_widgets.append(self.texto_consulta)

        conexion = sqlite3.connect('BaseDeDatos.db')
        cursorBD = conexion.cursor()
        cursorBD.execute('''SELECT 
                                        inscripciones.idInscripcion,
                                        inscripciones.idConvenio,
                                        grados_origen.nombre AS GradoOrigen,
                                        centros_origen.nombre AS CentroOrigen,
                                        grados_destino.nombre AS GradoDestino,
                                        centros_destino.nombre AS CentroDestino,
                                        GROUP_CONCAT(asignaturas_origen.nombre, ', ') AS AsignaturasOrigen,
                                        GROUP_CONCAT(asignaturas_destino.nombre, ', ') AS AsignaturasDestino
                                    FROM 
                                        inscripciones
                                    JOIN 
                                        convenios ON inscripciones.idConvenio = convenios.idConvenio
                                    JOIN 
                                        grados AS grados_origen ON convenios.idGradoOrigen = grados_origen.idGrado
                                    JOIN 
                                        centros AS centros_origen ON grados_origen.idCentro = centros_origen.idCentro
                                    JOIN 
                                        grados AS grados_destino ON convenios.idGradoDestino = grados_destino.idGrado
                                    JOIN 
                                        centros AS centros_destino ON grados_destino.idCentro = centros_destino.idCentro
                                    LEFT JOIN 
                                        equivalenciasAsignaturas ON convenios.idConvenio = equivalenciasAsignaturas.idConvenio
                                    LEFT JOIN 
                                        asignaturas AS asignaturas_origen ON equivalenciasAsignaturas.idAsignaturaOrigen = asignaturas_origen.idAsignatura
                                    LEFT JOIN 
                                        asignaturas AS asignaturas_destino ON equivalenciasAsignaturas.idAsignaturaDestino = asignaturas_destino.idAsignatura
                                    WHERE 
                                        inscripciones.idUser = ?
                                    AND inscripciones.estado = 'Activa'
                                    GROUP BY 
                                        inscripciones.idInscripcion
                                    ORDER BY
                                        inscripciones.idInscripcion ASC;''', (str(self.idUsuario)))
        resultados = cursorBD.fetchall()

        if not resultados:
            self.texto_consulta.insert("1.0", f"No hay inscripciones realizadas\n")

        for resultado in resultados:
            idInscripcion, idConvenio, gradoOrigen, centroOrigen, gradoDestino, centroDestino, asignaturasOrigen, asignaturasDestino = resultado

            self.texto_consulta.insert("1.0", f"ID Inscripción: {idInscripcion}\n")
            self.texto_consulta.insert("2.0", f"ID Convenio: {idConvenio}\n")
            self.texto_consulta.insert("3.0", f"Grado Origen: {gradoOrigen} - Centro: {centroOrigen}\n")
            self.texto_consulta.insert("4.0", f"Grado Destino: {gradoDestino} - Centro: {centroDestino}\n")
            self.texto_consulta.insert("5.0", f"Asignaturas Origen: {asignaturasOrigen}\n")
            self.texto_consulta.insert("6.0", f"Asignaturas Destino: {asignaturasDestino}\n")
            self.texto_consulta.insert("7.0", "----------\n")

    def elegir_plan(self):

        self.borrar_widgets()

        conexion = sqlite3.connect('BaseDeDatos.db')
        cursorBD = conexion.cursor()
        cursorBD.execute('SELECT idConvenio FROM convenios')
        planes = cursorBD.fetchall()

        if not planes:
            self.etiqueta_plan = customtkinter.CTkLabel(self, text="No hay planes para elegir", font=("Segoe UI", 14))
            self.etiqueta_plan.place(relx=0.05 , rely= 0.4)
            self.vector_borrar_widgets.append(self.etiqueta_plan)
        else:
            planes = [str(row[0]) for row in planes]
            conexion.close()

            self.etiqueta_plan = customtkinter.CTkLabel(self, text="Elegir Planes:", font=("Segoe UI", 14))
            self.etiqueta_plan.place(relx=0.05 , rely= 0.4)
            self.vector_borrar_widgets.append(self.etiqueta_plan)

            self.opcion_plan = customtkinter.CTkOptionMenu(self, values=planes, command= lambda seleccion: self.obtener_datos_planes(seleccion))
            self.opcion_plan.place(relx=0.15 , rely= 0.4)
            self.vector_borrar_widgets.append(self.opcion_plan)
    
    def obtener_datos_planes(self, seleccion):

        conexion = sqlite3.connect('BaseDeDatos.db')
        cursorBD = conexion.cursor()
        cursorBD.execute('''SELECT 
                                grados_origen.nombre AS GradoOrigen,
                                centros_origen.nombre AS CentroOrigen,
                                grados_destino.nombre AS GradoDestino,
                                centros_destino.nombre AS CentroDestino,
                                convenios.curso AS Curso,
                                convenios.duracion AS Duracion
                            FROM 
                                convenios
                            JOIN grados AS grados_origen ON convenios.idGradoOrigen = grados_origen.idGrado
                            JOIN centros AS centros_origen ON grados_origen.idCentro = centros_origen.idCentro
                            JOIN grados AS grados_destino ON convenios.idGradoDestino = grados_destino.idGrado
                            JOIN centros AS centros_destino ON grados_destino.idCentro = centros_destino.idCentro
                            WHERE 
                                convenios.idConvenio = ?;''', (seleccion))
        resultado = cursorBD.fetchone()


        self.etiqueta_grado_Origen = customtkinter.CTkLabel(self, text="Grado Origen: "+str(resultado[0]), font=("Segoe UI", 14))
        self.etiqueta_grado_Origen.place(relx=0.05 , rely= 0.5)
        self.vector_borrar_widgets.append(self.etiqueta_grado_Origen)

        self.etiqueta_centro_Origen = customtkinter.CTkLabel(self, text="Centro Origen: "+str(resultado[1]), font=("Segoe UI", 14))
        self.etiqueta_centro_Origen.place(relx=0.4 , rely= 0.5)
        self.vector_borrar_widgets.append(self.etiqueta_centro_Origen)

        self.etiqueta_grado_Destino = customtkinter.CTkLabel(self, text="Grado Origen: "+str(resultado[2]), font=("Segoe UI", 14))
        self.etiqueta_grado_Destino.place(relx=0.05 , rely= 0.6)
        self.vector_borrar_widgets.append(self.etiqueta_grado_Destino)

        self.etiqueta_centro_Destino = customtkinter.CTkLabel(self, text="Centro Destino: "+str(resultado[3]), font=("Segoe UI", 14))
        self.etiqueta_centro_Destino.place(relx=0.4 , rely= 0.6)
        self.vector_borrar_widgets.append(self.etiqueta_centro_Destino)

        self.etiqueta_curso = customtkinter.CTkLabel(self, text="Curso: "+str(resultado[4]), font=("Segoe UI", 14))
        self.etiqueta_curso.place(relx=0.05 , rely= 0.7)
        self.vector_borrar_widgets.append(self.etiqueta_curso)

        self.etiqueta_duracion = customtkinter.CTkLabel(self, text="Duracion: "+str(resultado[5]), font=("Segoe UI", 14))
        self.etiqueta_duracion.place(relx=0.05 , rely= 0.8)
        self.vector_borrar_widgets.append(self.etiqueta_duracion)


        self.boton_inscripcion = customtkinter.CTkButton(self, text="Inscribirse ", command= lambda: self.inscripcion_a_plan(seleccion), font=("Segoe UI", 14))
        self.boton_inscripcion.place(relx=0.4 , rely= 0.8)
        self.vector_borrar_widgets.append(self.boton_inscripcion)
    
    def inscripcion_a_plan(self, seleccion):
        self.withdraw()
        EspacioConsultarAsignaturas(self, seleccion)
    
    def anular_inscripción(self):

        self.borrar_widgets()

        conexion = sqlite3.connect('BaseDeDatos.db')
        cursorBD = conexion.cursor()
        cursorBD.execute('SELECT idInscripcion FROM inscripciones WHERE idUser=? AND estado=?', (self.idUsuario, 'Activa'))
        inscripciones = cursorBD.fetchall()

        if not inscripciones:
            self.etiqueta_ins = customtkinter.CTkLabel(self, text="No hay inscripciones que elegir", font=("Segoe UI", 14))
            self.etiqueta_ins.place(relx=0.05 , rely= 0.4)
            self.vector_borrar_widgets.append(self.etiqueta_ins)
        else:

            inscripciones = [str(row[0]) for row in inscripciones]
            conexion.close()

            self.etiqueta_ins = customtkinter.CTkLabel(self, text="Elegir Inscripción:", font=("Segoe UI", 14))
            self.etiqueta_ins.place(relx=0.05 , rely= 0.4)
            self.vector_borrar_widgets.append(self.etiqueta_ins)

            self.opcion_ins = customtkinter.CTkOptionMenu(self, values=inscripciones, command= lambda seleccion: self.obtener_datos_inscripcion(seleccion))
            self.opcion_ins.place(relx=0.2 , rely= 0.4)
            self.vector_borrar_widgets.append(self.opcion_ins)

    def obtener_datos_inscripcion(self, seleccion):
        
        conexion = sqlite3.connect('BaseDeDatos.db')
        cursorBD = conexion.cursor()

        print(self.app.entrada_usuario.get())

        cursorBD.execute('SELECT idUser FROM usuarios WHERE usuario=?', (str(self.app.entrada_usuario.get()),))
        idUsuario = cursorBD.fetchone()

        cursorBD.execute('''SELECT 
                                grados_origen.nombre AS GradoOrigen,
                                centros_origen.nombre AS CentroOrigen,
                                grados_destino.nombre AS GradoDestino,
                                centros_destino.nombre AS CentroDestino,
                                convenios.curso AS Curso,
                                convenios.duracion AS Duracion
                            FROM 
                                inscripciones
                            JOIN convenios ON inscripciones.idConvenio = convenios.idConvenio
                            JOIN grados AS grados_origen ON convenios.idGradoOrigen = grados_origen.idGrado
                            JOIN centros AS centros_origen ON grados_origen.idCentro = centros_origen.idCentro
                            JOIN grados AS grados_destino ON convenios.idGradoDestino = grados_destino.idGrado
                            JOIN centros AS centros_destino ON grados_destino.idCentro = centros_destino.idCentro
                            WHERE 
                                inscripciones.idInscripcion = ? AND inscripciones.idUser = ?;''', (seleccion, idUsuario[0]))
        resultado = cursorBD.fetchone()
        conexion.close()

        self.etiqueta_grado_Origen = customtkinter.CTkLabel(self, text="Grado Origen: "+str(resultado[0]), font=("Segoe UI", 14))
        self.etiqueta_grado_Origen.place(relx=0.05 , rely= 0.5)
        self.vector_borrar_widgets.append(self.etiqueta_grado_Origen)

        self.etiqueta_centro_Origen = customtkinter.CTkLabel(self, text="Centro Origen: "+str(resultado[1]), font=("Segoe UI", 14))
        self.etiqueta_centro_Origen.place(relx=0.4 , rely= 0.5)
        self.vector_borrar_widgets.append(self.etiqueta_centro_Origen)

        self.etiqueta_grado_Destino = customtkinter.CTkLabel(self, text="Grado Origen: "+str(resultado[2]), font=("Segoe UI", 14))
        self.etiqueta_grado_Destino.place(relx=0.05 , rely= 0.6)
        self.vector_borrar_widgets.append(self.etiqueta_grado_Destino)

        self.etiqueta_centro_Destino = customtkinter.CTkLabel(self, text="Centro Destino: "+str(resultado[3]), font=("Segoe UI", 14))
        self.etiqueta_centro_Destino.place(relx=0.4 , rely= 0.6)
        self.vector_borrar_widgets.append(self.etiqueta_centro_Destino)

        self.etiqueta_curso = customtkinter.CTkLabel(self, text="Curso: "+str(resultado[4]), font=("Segoe UI", 14))
        self.etiqueta_curso.place(relx=0.05 , rely= 0.7)
        self.vector_borrar_widgets.append(self.etiqueta_curso)

        self.etiqueta_duracion = customtkinter.CTkLabel(self, text="Duracion: "+str(resultado[5]), font=("Segoe UI", 14))
        self.etiqueta_duracion.place(relx=0.05 , rely= 0.8)
        self.vector_borrar_widgets.append(self.etiqueta_duracion)

        self.etiqueta_duracion = customtkinter.CTkButton(self, text="Anular inscripción ", command=lambda: self.inscripcion_anulada(seleccion), font=("Segoe UI", 14))
        self.etiqueta_duracion.place(relx=0.4 , rely= 0.8)
        self.vector_borrar_widgets.append(self.etiqueta_duracion)

    def inscripcion_anulada(self, seleccion):

        conexion = sqlite3.connect('BaseDeDatos.db')
        cursorBD = conexion.cursor()

        cursorBD.execute('SELECT * FROM inscripciones WHERE idInscripcion = ? AND idUser = ? AND estado = ?', (seleccion, self.idUsuario, "Activa"))
        resultado = cursorBD.fetchone()  # Devuelve la primera fila si existe, o None si no existe

        if resultado:
            cursorBD.execute('UPDATE inscripciones SET estado = ? WHERE idInscripcion = ?', ("Anulada", seleccion))
            conexion.commit()
            messagebox.showinfo("Anulación correcta", "Se ha anulado la inscripción correctamente", parent=self)
        else:
            messagebox.showerror("Error al anular", "No quedan inscripciones para anular", parent=self)
            conexion.close()
        conexion.close()
        


class EspacioConsultarAsignaturas(customtkinter.CTkToplevel):
    def __init__(self, EspacioEstudiante, seleccion):
        super().__init__(EspacioEstudiante)
        self.EspacioEstudiante = EspacioEstudiante
        self.seleccion = seleccion
        self.title("Equivalencias de Asignaturas")
        self.geometry("1000x500")
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.resizable(False, False)

        # Mensaje 
        self.etiqueta = customtkinter.CTkLabel(self, text="Las asignaturas que se convalidan son las siguientes:", font=("Segoe UI", 20))
        self.etiqueta.pack(padx=20, pady=20)

        conexion = sqlite3.connect("BaseDeDatos.db")
        cursor = conexion.cursor()

        cursor.execute('SELECT  duracion FROM convenios WHERE idConvenio = ?', (seleccion))
        duracion = cursor.fetchone()

        cursor.execute('''SELECT 
                            asignaturas_origen.nombre AS AsignaturaOrigen,
                            asignaturas_destino.nombre AS AsignaturaDestino
                        FROM 
                            equivalenciasAsignaturas
                        JOIN asignaturas AS asignaturas_origen ON equivalenciasAsignaturas.idAsignaturaOrigen = asignaturas_origen.idAsignatura
                        JOIN asignaturas AS asignaturas_destino ON equivalenciasAsignaturas.idAsignaturaDestino = asignaturas_destino.idAsignatura
                        WHERE 
                            equivalenciasAsignaturas.idConvenio = ?;''', (seleccion,))
        resultados = cursor.fetchall()
        conexion.close()

        if duracion == "curso_completo":
            self.geometry("1000x700")

        if not resultados:
            self.frame_resultados = customtkinter.CTkLabel(self, text="No se han encontrado asignaturas equivalentes",font=("Segoe UI", 16)).pack()

        # Mostrar las asignaturas
        cont=0
        for origen, destino in resultados:
            cont=cont+1
            texto = f"Origen: {origen} --------------- Asignatura {cont} --------------- Destino: {destino}"
            self.frame_resultados = customtkinter.CTkLabel(self, text=texto,font=("Segoe UI", 16)).pack(padx=10, pady=10)

        self.boton_confirmar = customtkinter.CTkButton(self, text="Confirmar inscripción", command=lambda: self.confirmar_inscripcion(seleccion), font=("Segoe UI", 12),)
        self.boton_confirmar.pack(padx=40, pady=40)
        
        self.boton_atras = customtkinter.CTkButton(self, text="Volver atrás", command= lambda: self.volver_atras(), font=("Segoe UI", 12),)
        self.boton_atras.pack()
    
    def volver_atras(self):

        self.destroy()
        self.EspacioEstudiante.deiconify()

    def confirmar_inscripcion(self, seleccion):

        conexion = sqlite3.connect("BaseDeDatos.db")
        cursor = conexion.cursor()

        cursor.execute('SELECT count(idInscripcion) FROM inscripciones')
        resultado=cursor.fetchone()
        cont = resultado[0]
        cont=cont+1

        cursor.execute('SELECT * FROM inscripciones WHERE idUser=? AND idConvenio=?', (self.EspacioEstudiante.idUsuario, seleccion))
        resultado=cursor.fetchone()

        if resultado:
            messagebox.showerror("Error al inscribirse", "Ya existe una inscripción a ese plan o está anulada")
            conexion.close()
        else:
            cursor.execute('''INSERT INTO inscripciones(idInscripcion, idUser, idConvenio, estado)
                            VALUES(?, ?, ?, ?)''', (cont, self.EspacioEstudiante.idUsuario, seleccion, "Activa"))
            conexion.commit()
            messagebox.showinfo("Inscripción registrada", "Se ha almacenado la inscripción correctamente")
            conexion.close()
            self.volver_atras()


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
