import sqlite3
import unittest

class TestElegirPlan(unittest.TestCase):
    def setUp(self):
        """
        Configura una base de datos en memoria con las tablas y datos necesarios para las pruebas.
        """
        self.conexion = sqlite3.connect(":memory:")
        self.cursorBD = self.conexion.cursor()

        # Crear tablas
        self.cursorBD.execute("CREATE TABLE convenios (idConvenio INTEGER PRIMARY KEY, idGradoOrigen INTEGER, idGradoDestino INTEGER, curso TEXT, duracion TEXT)")
        self.cursorBD.execute("CREATE TABLE grados (idGrado INTEGER PRIMARY KEY, nombre TEXT, idCentro INTEGER)")
        self.cursorBD.execute("CREATE TABLE centros (idCentro INTEGER PRIMARY KEY, nombre TEXT)")
        self.cursorBD.execute("CREATE TABLE equivalenciasAsignaturas (idConvenio INTEGER, idAsignaturaOrigen INTEGER, idAsignaturaDestino INTEGER)")
        self.cursorBD.execute("CREATE TABLE asignaturas (idAsignatura INTEGER PRIMARY KEY, nombre TEXT)")
        self.cursorBD.execute("CREATE TABLE inscripciones (idInscripcion INTEGER PRIMARY KEY, idUser INTEGER, idConvenio INTEGER, estado TEXT)")

        # Insertar datos de prueba
        self.cursorBD.execute("INSERT INTO convenios (idConvenio, idGradoOrigen, idGradoDestino, curso, duracion) VALUES (1, 1, 2, '2024', '6 meses')")
        self.cursorBD.execute("INSERT INTO grados (idGrado, nombre, idCentro) VALUES (1, 'Grado A', 1)")
        self.cursorBD.execute("INSERT INTO grados (idGrado, nombre, idCentro) VALUES (2, 'Grado B', 2)")
        self.cursorBD.execute("INSERT INTO centros (idCentro, nombre) VALUES (1, 'Centro A')")
        self.cursorBD.execute("INSERT INTO centros (idCentro, nombre) VALUES (2, 'Centro B')")
        self.cursorBD.execute("INSERT INTO equivalenciasAsignaturas (idConvenio, idAsignaturaOrigen, idAsignaturaDestino) VALUES (1, 1, 2)")
        self.cursorBD.execute("INSERT INTO asignaturas (idAsignatura, nombre) VALUES (1, 'Asignatura A')")
        self.cursorBD.execute("INSERT INTO asignaturas (idAsignatura, nombre) VALUES (2, 'Asignatura B')")

        self.conexion.commit()

    def tearDown(self):
        """
        Cierra la conexión a la base de datos después de cada prueba.
        """
        self.conexion.close()

    def test_obtener_datos_planes(self):
        """
        Verifica que los datos de un plan específico se obtienen correctamente.
        """
        seleccion = 1
        self.cursorBD.execute('''SELECT 
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
                                    convenios.idConvenio = ?;''', (seleccion,))
        resultado = self.cursorBD.fetchone()

        self.assertIsNotNone(resultado, "Deberían obtenerse datos para el plan seleccionado")
        self.assertEqual(resultado[0], "Grado A", "El grado origen no coincide")
        self.assertEqual(resultado[1], "Centro A", "El centro origen no coincide")
        self.assertEqual(resultado[2], "Grado B", "El grado destino no coincide")
        self.assertEqual(resultado[3], "Centro B", "El centro destino no coincide")

    def test_inscripcion_a_plan(self):
        """
        Verifica que un usuario puede inscribirse en un plan correctamente.
        """
        seleccion = 1
        idUsuario = 1

        # Insertar inscripción
        self.cursorBD.execute("INSERT INTO inscripciones (idInscripcion, idUser, idConvenio, estado) VALUES (?, ?, ?, ?)", 
                              (1, idUsuario, seleccion, "Activa"))
        self.conexion.commit()

        # Verificar inscripción
        self.cursorBD.execute("SELECT * FROM inscripciones WHERE idUser=? AND idConvenio=?", (idUsuario, seleccion))
        resultado = self.cursorBD.fetchone()

        self.assertIsNotNone(resultado, "El usuario debería estar inscrito en el plan seleccionado")
        self.assertEqual(resultado[3], "Activa", "El estado de la inscripción debería ser 'Activa'")

# Ejecutar pruebas
if __name__ == "__main__":
    unittest.main()
