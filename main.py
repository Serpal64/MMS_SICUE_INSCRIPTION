from interfaz import App
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent / "Paquete"))
from Paquete import *

if __name__ == "__main__":
    app = App()
    app.mainloop()
