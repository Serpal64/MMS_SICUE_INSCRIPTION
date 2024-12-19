# Estas son las funciones que se van a importar del fichero modulos.py
from .modulos import EspacioAdmin, EspacioAsignaturas, EspacioEstudiante
from .funciones import Universidades, Centros, Grados, crearAsignaturas, equivalenciasAsignaturas, crearConvenio

__all__=["verificar_credenciales", "Universidades", "Centros", "Grados", "equivalenciasAsignaturas", "crearConvenio"]