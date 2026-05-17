from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar

from src.hilo_red import HiloVerificador


class VentanaPrincipal(QMainWindow):
    # Diccionario estático para evitar la duplicación de hojas de estilo en memoria
    ESTILOS_ESTADO = {
        "PROCESANDO": "background-color: #e0e0e0; color: #333333;",
        "LIBRE": "background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb;",
        "BLOQUEADO": "background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;",
        "ERROR": "background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba;"
    }

    def __init__(self, servicio_red):
        super().__init__()
        self.bar_progress = None
        self.btn_check = None
        self.lbl_status = None
        self.servicio_red = servicio_red
        self.worker = None

        self.setWindowTitle("Monitor de Red HayFutbol")
        self.setFixedSize(420, 260)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Hoja de estilo base común para la etiqueta de estado
        self.lbl_status = QLabel("Estado: Iniciando comprobación...")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_status.setStyleSheet("""
            QLabel {
                font-size: 13px; font-weight: bold; padding: 15px; border-radius: 5px;
                background-color: #f0f0f0; color: #333333;
            }
        """)
        layout.addWidget(self.lbl_status)

        # Barra de progreso indeterminada
        self.bar_progress = QProgressBar()
        self.bar_progress.setRange(0, 0)
        layout.addWidget(self.bar_progress)

        self.btn_check = QPushButton("Recomprobar Estado")
        self.btn_check.setEnabled(False)
        self.btn_check.clicked.connect(self.ejecutar_tarea_red)
        layout.addWidget(self.btn_check)

        self.ejecutar_tarea_red()

    def _actualizar_vista_estado(self, clave_estilo: str, texto: str):
        """Reutiliza la lógica de estilos y textos"""
        self.lbl_status.setText(texto)
        self.lbl_status.setStyleSheet(f"""
            QLabel {{
                font-size: 13px; font-weight: bold; padding: 15px; border-radius: 5px;
                {self.ESTILOS_ESTADO[clave_estilo]}
            }}
        """)

    def ejecutar_tarea_red(self):
        """Prepara la interfaz y gestiona el ciclo de vida del hilo de red."""
        self._actualizar_vista_estado("PROCESANDO", "Consultando API...")
        self.btn_check.setEnabled(False)
        self.bar_progress.show()

        # Si el trabajador existe y sigue activo, abortamos la nueva petición
        if self.worker and self.worker.isRunning():
            return

        self.worker = HiloVerificador(self.servicio_red)

        # Conectamos las señales
        self.worker.resultado_recibido.connect(self.mostrar_resultado)
        self.worker.finished.connect(self._limpiar_worker)

        # Arrancamos el hilo secundario
        self.worker.start()

    def _limpiar_worker(self):
        """Elimina de forma segura la referencia al hilo finalizado cuando lanza la señal finished."""
        self.worker = None

    def mostrar_resultado(self, estado: str):
        self.bar_progress.hide()
        self.btn_check.setEnabled(True)

        if estado == "LIBRE":
            self._actualizar_vista_estado("LIBRE", "✔ ACCESO LIBRE")
        elif estado == "BLOQUEADO":
            self._actualizar_vista_estado("BLOQUEADO", "❌ INTERNET BLOQUEADO")
        else:
            self._actualizar_vista_estado("ERROR", "⚠ ERROR DE CONEXIÓN / DATOS NO DISPONIBLES")
