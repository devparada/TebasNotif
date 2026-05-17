from PyQt6.QtCore import QThread, pyqtSignal


class HiloVerificador(QThread):
    resultado_recibido = pyqtSignal(str)

    def __init__(self, servicio_red):
        super().__init__()
        self.servicio_red = servicio_red

    def run(self):
        resultado = self.servicio_red.comprobar_estado_global()
        self.resultado_recibido.emit(resultado)
