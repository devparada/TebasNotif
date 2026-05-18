from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request


class ClienteHayFutbol:
    def __init__(self, base_url: str = "https://hayahora.futbol/estado/"):
        self.base_url = base_url.rstrip('/') + '/'
        # Lista de archivos de control de bloqueo de los principales operadores
        self.archivos_operadores = [
            "blocked-digi.txt",
            "blocked-masmovil.txt",
            "blocked-movistar.txt",
            "blocked-orange.txt",
            "blocked-vodafone.txt"
        ]

    def comprobar_estado_global(self, timeout: int = 5) -> str:
        """
        Determina si internet está libre comprobando el contenido de los archivos de bloqueo.
        Si todos están vacíos o no se encuentran bloqueos activos, la red está LIBRE.
        """
        headers = {"User-Agent": "Mozilla/5.0"}
        bloqueo_detectado = False
        peticiones_correctas = 0

        for archivo in self.archivos_operadores:
            url_archivo = f"{self.base_url}{archivo}"
            try:
                peticion = Request(url_archivo, headers=headers)
                with urlopen(peticion, timeout=timeout) as respuesta:
                    if respuesta.status == 200:
                        peticiones_correctas += 1
                        # Leemos el contenido limpiando espacios y saltos de línea
                        contenido = respuesta.read().decode("utf-8").strip()

                        if contenido:
                            bloqueo_detectado = True
                            break

            except HTTPError as e:
                if e.code == 404:
                    peticiones_correctas += 1
                    continue
                return "ERROR"
            except (URLError, TimeoutError):
                return "ERROR"

        if peticiones_correctas == 0:
            return "ERROR"

        if bloqueo_detectado:
            return "BLOQUEADO"

        return "LIBRE"
