import sqlite3
import unittest

class TestAnularInscripcion(unittest.TestCase):
    def setUp(self):
        """
        Configura una base de datos en memoria con las tablas y datos necesarios para las pruebas.
        """
        self.conexion = sqlite3.connect(":memory:")
        self.cursorBD = self.conexion.cursor()

        # Crear tablas
        self.cursorBD.execute("CREATE TABLE usuarios (idUser INTEGER PRIMARY KEY, usuario TEXT)")
        self.cursorBD.execute("CREATE TABLE inscripciones (idInscripcion INTEGER PRIMARY KEY, idUser INTEGER, idConvenio INTEGER, estado TEXT)")
        self.cursorBD.execute("CREATE TABLE convenios (idConvenio INTEGER PRIMARY KEY, idGradoOrigen INTEGER, idGradoDestino INTEGER, curso TEXT, duracion TEXT)")
        self.cursorBD.execute("CREATE TABLE grados (idGrado INTEGER PRIMARY KEY, nombre TEXT, idCentro INTEGER)")
        self.cursorBD.execute("CREATE TABLE centros (idCentro INTEGER PRIMARY KEY, nombre TEXT)")

        # Insertar datos de prueba
        self.cursorBD.execute("INSERT INTO usuarios (idUser, usuario) VALUES (1, 'usuario_prueba')")
        self.cursorBD.execute("INSERT INTO inscripciones (idInscripcion, idUser, idConvenio, estado) VALUES (1, 1, 1, 'Activa')")
        self.cursorBD.execute("INSERT INTO convenios (idConvenio, idGradoOrigen, idGradoDestino, curso, duracion) VALUES (1, 1, 2, '2024', '6 meses')")
        self.cursorBD.execute("INSERT INTO grados (idGrado, nombre, idCentro) VALUES (1, 'Grado A', 1)")
        self.cursorBD.execute("INSERT INTO grados (idGrado, nombre, idCentro) VALUES (2, 'Grado B', 2)")
        self.cursorBD.execute("INSERT INTO centros (idCentro, nombre) VALUES (1, 'Centro A')")
        self.cursorBD.execute("INSERT INTO centros (idCentro, nombre) VALUES (2, 'Centro B')")

        self.conexion.commit()

    def tearDown(self):
        """
        Cierra la conexión a la base de datos después de cada prueba.
        """
        self.conexion.close()

    def test_anular_inscripcion(self):
        """
        Verifica que una inscripción activa se pueda anular correctamente.
        """
        # Obtener la inscripción activa
        self.cursorBD.execute("SELECT idInscripcion FROM inscripciones WHERE idUser=? AND estado=?", (1, "Activa"))
        inscripcion_id = self.cursorBD.fetchone()[0]

        # Anular la inscripción
        self.cursorBD.execute("UPDATE inscripciones SET estado = ? WHERE idInscripcion = ?", ("Anulada", inscripcion_id))
        self.conexion.commit()

        # Verificar que se anuló correctamente
        self.cursorBD.execute("SELECT estado FROM inscripciones WHERE idInscripcion = ?", (inscripcion_id,))
        estado = self.cursorBD.fetchone()[0]
        self.assertEqual(estado, "Anulada", "La inscripción no se anuló correctamente")

    def test_no_hay_inscripciones_activas(self):
        """
        Verifica que no haya inscripciones activas después de anularlas todas.
        """
        # Anular todas las inscripciones activas
        self.cursorBD.execute("UPDATE inscripciones SET estado = ? WHERE estado = ?", ("Anulada", "Activa"))
        self.conexion.commit()

        # Verificar que no haya inscripciones activas
        self.cursorBD.execute("SELECT idInscripcion FROM inscripciones WHERE estado=?", ("Activa",))
        inscripciones = self.cursorBD.fetchall()
        self.assertFalse(inscripciones, "No deberían quedar inscripciones activas")

# Ejecutar pruebas
if __name__ == "__main__":
    unittest.main()
