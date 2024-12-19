import unittest
from unittest.mock import patch, MagicMock
from Paquete.funciones import crearConvenio

class TestCrearConvenio (unittest.TestCase):
    @patch('Paquete.funciones.sqlite3.connect')
    def test_crear_convenio_correcto(self, mock_connect):
        #Datos de prueba válidos
        gradoOrigen = "Grado 1"
        gradoDestino = "Grado 2"
        curso = "2º"
        duracion = "1º Cuatrimestre"

        #Simula la conexion a la Base de Datos
        mock_conexion = MagicMock()
        mock_connect.retrun_value = mock_conexion
        mock_cursor = MagicMock()
        mock_conexion.cursor.return_value = mock_cursor

        #Simula la inserción del convenio
        #mock_cursor.execute.return_value = None
        # Simula que se ha creado un nuevo convenio y devuelve un idConvenio=1
        mock_cursor.lastrowid = 123
        

        #Ejecuta la función a probar
        idConvenio = crearConvenio(gradoOrigen, gradoDestino, curso, duracion)

        print(idConvenio)
        #Verifica que el id del convenio sea diferente de 0 (indica que se creó correctamente)
        self.assertNotEqual(idConvenio, 0)

        mock_cursor.execute.assert_called_with(
            '''INSERT INTO convenios(idGradoOrigen, idGradoDestino, curso, duracion) VALUES(?,?,?,?)''',
            (mock_cursor.lastrowid, 456, curso, duracion)
        )

class TestCrearConvenioMensajeExitoso(unittest.TestCase):
    @patch('tkinter.messagebox.showinfo')
    @patch('Paquete.funciones.sqlite3.connect')
    def test_mostrar_mensaje_exito(self, mock_connect, mock_shoinfo):
        gradoOrigen = "Grado en Ingeniería Eléctrica"
        gradoDestino = "Grado en Ingeniería Eléctrica"
        curso = "2º"
        duracion = "1º Cuatrimestre"

        #Simula la conexion a la Base de Datos
        mock_conexion = MagicMock()
        mock_connect.retrun_value = mock_conexion
        mock_cursor = MagicMock()
        mock_conexion.cursor.return_value = mock_cursor

        #Simula la inserción del convenio
        mock_cursor.execute.return_value = None
        # Simula que se ha creado un nuevo convenio y devuelve un idConvenio=1
        mock_cursor.lastrowid = 1

        crearConvenio(gradoOrigen, gradoDestino, curso, duracion)

        mock_shoinfo.assert_called_with("Plan de Convalidación Creado", "El Plan de Convalidación se ha creado exitosamente")
        
        

if __name__ == "__main__":
    unittest.main()