import unittest
from unittest.mock import MagicMock, patch
from tkinter import messagebox
from Paquete.modulos import EspacioAsignaturas

class TestCrearPlan(unittest.TestCase):
    def setUp(self):
        # Crear un objeto simulado para self.EspacioAdmin
        self.mock_EspacioAdmin = MagicMock()
        self.mock_EspacioAdmin.entrada_grado_O.get.return_value = "Grado Origen"
        self.mock_EspacioAdmin.entrada_grado_D.get.return_value = "Grado Destino"
        self.mock_EspacioAdmin.opcion_curso.get.return_value = "2º"
        self.mock_EspacioAdmin.opcion_tiempo.get.return_value = "1º Cuatrimestre"
        
        # Crear una instancia del objeto con el método CrearPlan
        class MockAdmin:
            def __init__(self, EspacioAdmin):
                self.EspacioAdmin = EspacioAdmin
                # Crear una lista de 10 asignaturas
                self.listaAsignaturas = [
                    MagicMock(get=MagicMock(return_value=f"Asignatura {i+1}")) for i in range(10)
                ]
                self.nAsignaturas = 10
            CrearPlan = EspacioAsignaturas.CrearPlan  # Copiar el método a la clase simulada
        
        self.objeto_prueba = MockAdmin(self.mock_EspacioAdmin)

    @patch("Paquete.crearAsignaturas")
    @patch("Paquete.equivalenciasAsignaturas")
    @patch("Paquete.crearConvenio")
    @patch("tkinter.messagebox.showwarning")
    def test_campos_incompletos(self, mock_showwarning, mock_crearConvenio, mock_equivalencias, mock_crearAsignaturas):
        # Simular que una de las asignaturas tiene un campo vacío
        self.objeto_prueba.listaAsignaturas[5].get.return_value = ""
        
        # Ejecutar el método CrearPlan
        self.objeto_prueba.CrearPlan()
        
        # Verificar que muestra una advertencia
        mock_showwarning.assert_called_once_with('Campos incompletos', 'Por favor, rellene todos los campos')
        
        # Verificar que las funciones externas no se llamaron
        mock_crearConvenio.assert_not_called()
        mock_crearAsignaturas.assert_not_called()
        mock_equivalencias.assert_not_called()

    @patch("Paquete.crearAsignaturas", return_value=list(range(10)))
    @patch("Paquete.equivalenciasAsignaturas")
    @patch("Paquete.crearConvenio", return_value=1)
    def test_crear_plan_exitoso(self, mock_crearConvenio, mock_equivalencias, mock_crearAsignaturas):
        self.objeto_prueba.destroy = MagicMock()

        # Ejecutar el método CrearPlan
        self.objeto_prueba.CrearPlan()
        
        # Verificar que se llamó a crearConvenio con los valores correctos
        mock_crearConvenio.assert_called_once_with(
            "Grado Origen", "Grado Destino", "2º", "1_cuatri"
        )
        
        # Verificar que se llamó a crearAsignaturas con los valores correctos
        mock_crearAsignaturas.assert_called_once_with(
            [f"Asignatura {i+1}" for i in range(10)], "Grado Origen", "Grado Destino", 10, "2º"
        )
        
        # Verificar que se llamó a equivalenciasAsignaturas con los valores correctos
        mock_equivalencias.assert_called_once_with(1, list(range(10)), 10)

        # Verificar que se llamó a deiconify
        self.mock_EspacioAdmin.deiconify.assert_called_once()

        # Verificar que se llamó a destroy en el propio objeto
        self.objeto_prueba.destroy.assert_called_once()
        

if __name__ == "main":
    unittest.main()