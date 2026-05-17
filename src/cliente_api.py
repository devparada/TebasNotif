import json
import urllib.error
import urllib.request


class ClienteHayFutbol:
    def __init__(self, url: str = "https://hayahora.futbol/estado/data.json", timeout: int = 5):
        self.url = url
        self.timeout = timeout

    def comprobar_estado_global(self) -> str:
        """
        Analiza el JSON de la API a nivel global.
        Si el estado más reciente de CUALQUIER elemento es False, se considera que está BLOQUEADO.
        """
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            peticion = urllib.request.Request(self.url, headers=headers)

            with urllib.request.urlopen(peticion, timeout=self.timeout) as respuesta:
                if respuesta.status == 200:
                    json_data = json.loads(respuesta.read().decode('utf-8'))

                    for item in json_data.get("data", []):
                        cambios = item.get("stateChanges", [])

                        if cambios:
                            ultimo_estado = cambios[-1].get("state")

                            if ultimo_estado is False:
                                return "BLOQUEADO"
                    return "LIBRE"
                return "ERROR"

        except urllib.error.HTTPError:
            return "ERROR"
