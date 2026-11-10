import ipaddress
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request


class ClienteHayFutbol:

    def __init__(self, base_url: str = "https://hayahora.futbol/estado/"):
        self.base_url = base_url.rstrip("/") + "/"

        # Archivos de control de bloqueo de los principales operadores
        self.archivos_operadores = {
            "DIGI": "blocked-digi.txt",
            "MásMóvil": "blocked-masmovil.txt",
            "Movistar": "blocked-movistar.txt",
            "Orange": "blocked-orange.txt",
            "Vodafone": "blocked-vodafone.txt"
        }

    @staticmethod
    def _extraer_ips(contenido: str) -> set[str]:
        """
        Extrae y valida las direcciones IP del contenido.
        Elimina comentarios, líneas vacías y duplicados.
        """

        ips = set()

        for linea in contenido.splitlines():
            ip = linea.split("#", 1)[0].strip()

            if not ip:
                continue

            try:
                ip_normalizada = str(ipaddress.ip_address(ip))
                ips.add(ip_normalizada)

            except ValueError as e:
                raise ValueError(f"IP no válida: {ip}") from e

        return ips

    def comprobar_estado_global(self, timeout: int = 5) -> str:
        """
        Comprueba el estado global de Internet mediante
        los archivos de bloqueo de los operadores.

        LIBRE: menos de la mayoría de operadores afectados.
        BLOQUEADO: mayoría absoluta de operadores afectados.
        ERROR: fallo durante alguna consulta o validación.
        """

        headers = {"User-Agent": "Mozilla/5.0"}
        operadores_afectados = 0
        total_operadores = len(self.archivos_operadores)

        if total_operadores == 0:
            return "ERROR"

        for archivo in self.archivos_operadores.values():
            url_archivo = f"{self.base_url}{archivo}"

            try:
                peticion = Request(url_archivo, headers=headers)

                with urlopen(peticion, timeout=timeout) as respuesta:
                    if respuesta.status != 200:
                        return "ERROR"

                    contenido = respuesta.read().decode("utf-8")

            except (HTTPError, URLError, TimeoutError, OSError, UnicodeError):
                return "ERROR"

            try:
                ips_bloqueadas = self._extraer_ips(contenido)

            except ValueError:
                return "ERROR"

            # Cada operador cuenta como máximo una vez
            if ips_bloqueadas:
                operadores_afectados += 1

        # Mayoría absoluta de operadores
        mayoria = (total_operadores // 2) + 1

        if operadores_afectados >= mayoria:
            return "BLOQUEADO"

        return "LIBRE"
