# Importa la clase App del fichero llamado interfaz.py para crear la instancia de la clase App()
from interfaz import App

# Cuando Python ejecuta un archivo, crea automáticamente una variable especial llamada __name__. 
# Esta variable puede tomar dos valores principales: 
# "__main__": Si el archivo se está ejecutando directamente como el programa principal.
# El nombre del módulo: Si el archivo está siendo importado en otro archivo.
# Se usa para que cierta parte del código, como la inicialización del programa o las pruebas, 
# se ejecute solo cuando el archivo se ejecuta directamente, pero no cuando el archivo se importa como un módulo.
if __name__ == "__main__":
    app = App()
    app.mainloop()
