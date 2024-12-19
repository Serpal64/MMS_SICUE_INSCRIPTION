import sqlite3
#Para conectarse a la base de datos BaseDeDatos.db y si no existe se vcrea una con ese nombre
conexion = sqlite3.connect('BaseDeDatos.db')

#Se crea el cursor para poder realizar las consultas sobre la base de datos
cursorBD = conexion.cursor()

#Para borrar todas las tablas de esta base de datos
cursorBD.execute(''' DROP TABLE universidades  ''')
cursorBD.execute(''' DROP TABLE centros  ''')
cursorBD.execute(''' DROP TABLE asignaturas  ''')
cursorBD.execute(''' DROP TABLE grados  ''')
cursorBD.execute(''' DROP TABLE convenios  ''')
cursorBD.execute(''' DROP TABLE usuarios  ''')
cursorBD.execute(''' DROP TABLE equivalenciasAsignaturas  ''')
cursorBD.execute(''' DROP TABLE inscripciones  ''')

#Se crea la tabla de universidades SI NO EXISTE
cursorBD.execute(''' CREATE TABLE IF NOT EXISTS universidades(
                 idUni INTEGER PRIMARY KEY AUTOINCREMENT,
                 nombre TEXT NOT NULL,
                 ciudad TEXT NOT NULL) ''')

#Se crea la tabla de centros SI NO EXISTE
cursorBD.execute(''' CREATE TABLE IF NOT EXISTS centros(
                 idCentro INTEGER PRIMARY KEY AUTOINCREMENT,
                 nombre TEXT NOT NULL,
                 idUni INTEGER NOT NULL,
                 FOREIGN KEY (idUni) REFERENCES universidades(idUni)) ''')

#Se crea la tabla de grados SI NO EXISTE
cursorBD.execute(''' CREATE TABLE IF NOT EXISTS grados(
                 idGrado INTEGER PRIMARY KEY AUTOINCREMENT,
                 nombre TEXT NOT NULL,
                 idCentro INTEGER NOT NULL,
                 FOREIGN KEY (idCentro) REFERENCES centros(idCentro)) ''')

#Se crea la tabla de asignaturas SI NO EXISTE
cursorBD.execute(''' CREATE TABLE IF NOT EXISTS asignaturas(
                 idAsignatura INTEGER PRIMARY KEY AUTOINCREMENT,
                 nombre TEXT NOT NULL,
                 idGrado INTEGER NOT NULL,
                 curso INT NOT NULL,
                 FOREIGN KEY (idGrado) REFERENCES grados(idGrado)) ''')

#Se crea la tabla de convenios SI NO EXISTE
cursorBD.execute(''' CREATE TABLE IF NOT EXISTS convenios(
                 idConvenio INTEGER PRIMARY KEY AUTOINCREMENT,
                 idGradoOrigen INTEGER NOT NULL,
                 idGradoDestino INTEGER NOT NULL,
                 curso INT NOT NULL,
                 duracion VARCHAR(20) CHECK (duracion IN('curso_completo', '1_cuatri', '2_cuatri')) NOT NULL,
                 FOREIGN KEY (idGradoOrigen) REFERENCES grados(idGrado),
                 FOREIGN KEY (idGradoDestino) REFERENCES grados(idGrado)) ''')

#Se crea la tabla de equivalencias entre asignaturas SI NO EXISTE
cursorBD.execute('''CREATE TABLE IF NOT EXISTS equivalenciasAsignaturas(
                 idEquivalencia INTEGER PRIMARY KEY AUTOINCREMENT,
                 idConvenio INT NOT NULL,
                 idAsignaturaOrigen INT NOT NULL,
                 idAsignaturaDestino INT NOT NULL,
                 FOREIGN KEY (idConvenio) REFERENCES convenios(idConvenio),
                 FOREIGN KEY (idAsignaturaOrigen) REFERENCES asignaturas(idAsignatura),
                 FOREIGN KEY (idAsignaturaDestino) REFERENCES asignaturas(idAsignatura)) ''')

#Se crea la tabla de los usuarios del programa SI NO EXISTE
cursorBD.execute(''' CREATE TABLE IF NOT EXISTS usuarios(
                 idUser INTEGER PRIMARY KEY AUTOINCREMENT,
                 usuario TEXT UNIQUE NOT NULL,
                 contrasena TEXT NOT NULL,
                 rol TEXT NOT NULL CHECK(rol IN('Alumno', 'Administrador', 'Profesor')),
                 idGrado INTEGER,
                 curso INTEGER,
                 FOREIGN KEY (idGrado) REFERENCES grados(idGrado)) ''')

#Se crea la tabla de las inscripciones de los alumnos SI NO EXISTE
cursorBD.execute(''' CREATE TABLE IF NOT EXISTS inscripciones(
                 idInscripcion INTEGER PRIMARY KEY AUTOINCREMENT,
                 idUser INTEGER,
                 idConvenio INTEGER,
                 estado TEXT NOT NULL CHECK(estado IN ('Activa', 'Anulada')),
                 FOREIGN KEY (idUser) REFERENCES usuarios(idUser),
                 FOREIGN KEY (idConvenio) REFERENCES convenios(idConvenio)) ''')

#Para introducir los usuarios de la UCO
cursorBD.execute(''' SELECT COUNT(idUser) FROM usuarios''')
resultado = cursorBD.fetchone()
if resultado[0]==0:
    usuariosPredefinidos = [
        ('1', '1', 'Administrador',None,None),
        ('2', '2', 'Alumno', '1', '2'),
        ('3', '3', 'Profesor', '1', None) 
    ]
    cursorBD.executemany(''' INSERT INTO usuarios(usuario, contrasena, rol, idGrado, curso) VALUES (?,?,?,?,?) ''', usuariosPredefinidos)

#Para introducir las universidades
cursorBD.execute(''' SELECT COUNT(idUni) FROM universidades''')
resultado = cursorBD.fetchone()
if resultado[0]==0:
    UniversidadesPredefinidas = [
        ('1', 'Universidad de Córdoba (UCO)', 'Córdoba'),
        ('2', 'Universidad de Jaén (UJA)', 'Jaén'),
        ('3', 'Universidad de Huelva (UHU)', 'Huelva'),
        ('4', 'Universidad de Oviedo (UniOvi)', 'Oviedo')
    ]
    cursorBD.executemany(''' INSERT INTO universidades(idUni, nombre, ciudad) VALUES (?,?,?) ''', UniversidadesPredefinidas)

#Para introducir los centros
cursorBD.execute(''' SELECT COUNT(idCentro) FROM centros''')
resultado = cursorBD.fetchone()
if resultado[0]==0:
    CentrosPredefinidos = [
        ('1', 'Escuela Politécnica Superior de Córdoba (EPSC)', '1'),
        ('2', 'Escuela Técnica Superior de Ingeniería', '3'),
        ('3', 'Escuela Politécnica Superior de Jaén (EPS Jaén)', '2'),
        ('4', 'Escuela de Ingeniería Informática', '4')
    ]
    cursorBD.executemany(''' INSERT INTO centros(idCentro, nombre, idUni) VALUES (?,?,?) ''', CentrosPredefinidos)

#Para introducir los grados
cursorBD.execute(''' SELECT COUNT(idgrado) FROM grados''')
resultado = cursorBD.fetchone()
if resultado[0]==0:
    GradosPredefinidos = [
        ('1', 'Grado en Ingeniería Informática', '1'),
        ('2', 'Grado en Ingeniería Informática', '2'),
        ('3', 'Grado en Ingeniería Eléctrica', '1'),
        ('4', 'Grado en Ingeniería Eléctrica', '3'),
        ('5', 'Grado en Ingeniería Informática del Software', '4'),
    ]
    cursorBD.executemany(''' INSERT INTO grados(idGrado, nombre, idCentro) VALUES (?,?,?) ''', GradosPredefinidos)

#Para guardar los cambios realizados en la base de datos
conexion.commit()

#Para cerrar la base de datos
conexion.close()