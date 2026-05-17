import sys

from PyQt6.QtWidgets import QApplication

from src.cliente_api import ClienteHayFutbol
from src.interfaz import VentanaPrincipal


def main():
    app = QApplication(sys.argv)
    servicio_red = ClienteHayFutbol()

    # Crea la ventana y añade el resultado de la lógica
    ventana = VentanaPrincipal(servicio_red)
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
