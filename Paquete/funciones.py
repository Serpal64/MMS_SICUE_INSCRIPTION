import sqlite3
from tkinter import messagebox

def Universidades(botonUniversidad):
    conexion = sqlite3.connect('BaseDeDatos.db')
    cursorBD = conexion.cursor()

    cursorBD.execute('SELECT nombre FROM universidades WHERE idUni != 1')
    universidades = cursorBD.fetchall()

    conexion.close()

    opciones = ["Seleccione una opción"] + [universidad[0] for universidad in universidades]

    botonUniversidad.configure(values=opciones)

def Centros(botonCentro, universidad):
    conexion = sqlite3.connect('BaseDeDatos.db')
    cursorBD = conexion.cursor()

    cursorBD.execute('''SELECT c.nombre 
                     FROM centros c
                     JOIN universidades u ON u.idUni=c.idUni
                     WHERE u.nombre=?''', (universidad,))
    universidades = cursorBD.fetchall()

    conexion.close()

    opciones = ["Seleccione una opción"] + [universidad[0] for universidad in universidades]

    botonCentro.configure(values=opciones)

def Grados(botonGrado, centro):
    conexion = sqlite3.connect('BaseDeDatos.db')
    cursorBD = conexion.cursor()

    cursorBD.execute('''SELECT g.nombre 
                     FROM grados g
                     JOIN centros c ON c.idCentro=g.idCentro
                     WHERE c.nombre=?''', (centro,))
    universidades = cursorBD.fetchall()

    conexion.close()

    opciones = ["Seleccione una opción"] + [universidad[0] for universidad in universidades]

    botonGrado.configure(values=opciones)

def crearAsignaturas(Asignaturas, gradoOrigen, gradoDestino, nAsignaturas, curso):
    conexion = sqlite3.connect('BaseDeDatos.db')
    cursorBD = conexion.cursor()

    # Obtener el id de los grados
    cursorBD.execute('''SELECT idGrado 
                     FROM grados
                     WHERE nombre=? OR nombre=?
                     ORDER BY idGrado''', (gradoOrigen, gradoDestino))
    idGrado = cursorBD.fetchall()

    idAsignaturas = []

    for i in range(nAsignaturas):
        #Para comprobar si existen las asignaturas
        if i < (nAsignaturas/2):
            grado = idGrado[0][0]
        else:
            grado = idGrado[1][0]
        cursorBD.execute('''SELECT a.idAsignatura 
                         FROM asignaturas a
                         JOIN grados g ON g.idGrado=a.idGrado
                         JOIN centros c ON c.idCentro=g.idCentro
                         JOIN universidades u ON u.idUni=c.idUni
                         WHERE a.curso=? AND a.nombre=? AND a.idGrado=?''', (curso, Asignaturas[i], grado))
        resultado = cursorBD.fetchone()

        # Para crearlas en caso de que no existan
        if not resultado:
            if i < (nAsignaturas/2):
                cursorBD.execute('INSERT INTO asignaturas(nombre, idGrado, curso) VALUES(?,?,?)', (Asignaturas[i], idGrado[0][0], curso))
                idAsignaturas.append(cursorBD.lastrowid)
            else:
                cursorBD.execute('INSERT INTO asignaturas(nombre, idGrado, curso) VALUES(?,?,?)', (Asignaturas[i], idGrado[1][0], curso))
                idAsignaturas.append(cursorBD.lastrowid)
        else:
            idAsignaturas.append(resultado[0])

    conexion.commit()
    conexion.close()

    return idAsignaturas

def crearConvenio(gradoOrigen, gradoDestino, curso, duracion):
    conexion = sqlite3.connect('BaseDeDatos.db')
    cursorBD = conexion.cursor()

    # Obtener el id de los grados
    cursorBD.execute('''SELECT idGrado 
                     FROM grados
                     WHERE nombre=? OR nombre=?
                     ORDER BY idGrado''', (gradoOrigen, gradoDestino))
    idGrado = cursorBD.fetchall()

    cursorBD.execute('''SELECT idConvenio 
                     FROM convenios 
                     WHERE idGradoOrigen=? AND idGradoDestino=? AND curso=? AND duracion=?''', (idGrado[0][0], idGrado[1][0], curso, duracion))
    idConvenio = cursorBD.fetchone()

    # Si no existe el convenio, se crea
    if not idConvenio:
        cursorBD.execute('''INSERT INTO convenios(idGradoOrigen, idGradoDestino, curso, duracion) 
                         VALUES(?,?,?,?)''', (idGrado[0][0], idGrado[1][0], curso, duracion))
        messagebox.showinfo("Plan de Convalidación Creado", "El Plan de Convalidación se ha creado exitosamente")
        id = cursorBD.lastrowid
    else:
        messagebox.showwarning("Plan de Convalidación Creado Previamente", "Este Plan de Convalidación ya ha sido ceado previamente")
        id = 0
    
    conexion.commit()
    conexion.close()

    return id

def equivalenciasAsignaturas(idConvenio, IdAsignaturas, nAsignaturas):
    conexion = sqlite3.connect('BaseDeDatos.db')
    cursorBD = conexion.cursor()

    for i in range(nAsignaturas//2):
        cursorBD.execute('''SELECT idEquivalencia 
                         FROM equivalenciasAsignaturas 
                         WHERE idConvenio=? AND idAsignaturaOrigen=? AND idAsignaturaDestino=?''', 
                         (idConvenio, IdAsignaturas[i], IdAsignaturas[i + (nAsignaturas//2)]))
        idEquivalencia = cursorBD.fetchone()

        # Si no existe la equivalencia, se crea
        if not idEquivalencia:
            cursorBD.execute('''INSERT INTO equivalenciasAsignaturas(idConvenio, idAsignaturaOrigen, idAsignaturaDestino) VALUES(?,?,?)''', 
                             (idConvenio, IdAsignaturas[i], IdAsignaturas[i + (nAsignaturas//2)]))
    
    conexion.commit()
    conexion.close()