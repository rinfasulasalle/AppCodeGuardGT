from typing import Optional, List
import logging
import requests


class ApisNetPe:

    BASE_URL = "https://api.apis.net.pe"

    def __init__(self) -> None:
        # Lista de tokens
        self.tokens = [
            "apis-token-10860.JIwQ9MIQQz0AzC99pmwetyKHEQK66hud",
            "apis-token-10810.AcH3agg0sVn8d84foxDjh45dD9wERtYm",
            "apis-token-10855.FoF5KUEfmeM3zOBfbde5vFCduxLf2YsE",
            "apis-token-10856.FxwthmERw5U92rZq4eTmncSQKLBPhHIM",
            "apis-token-10857.dvPV1vUtEkTQHDGbnwW6IVX2blUVqEVz",
            "apis-token-10858.bRHY8dTBB07ICMuH1Lf0nIa9lOZVjKYN",
            "apis-token-10860.JIwQ9MIQQz0AzC99pmwetyKHEQK66hud"
        ]
        self.token_index = 0  # Índice actual del token a usar

    def _get(self, path: str, params: dict):
        url = f"{self.BASE_URL}{path}"

        for _ in range(len(self.tokens)):  # Intentar con todos los tokens
            current_token = self.tokens[self.token_index]

            headers = {
                "Authorization": current_token,
                "Referer": "https://apis.net.pe/api-tipo-cambio.html"
            }

            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                return response.json()

            elif response.status_code == 401:
                logging.warning(f"{response.url} - Invalid token or limited. Trying next token.")
            elif response.status_code == 403:
                logging.warning(f"{response.url} - IP blocked. Trying next token.")
            elif response.status_code == 429:
                logging.warning(f"{response.url} - Too many requests. Add delay and retry.")
            elif response.status_code == 422:
                logging.warning(f"{response.url} - Invalid parameter")
                logging.warning(response.text)
                break  # No sirve seguir con otros tokens, el parámetro es inválido.
            else:
                logging.warning(f"{response.url} - Server Error status_code={response.status_code}")
                break  # Error del servidor, no intentamos otros tokens.

            # Cambiar al siguiente token en la lista
            self.token_index = (self.token_index + 1) % len(self.tokens)

        return None  # Si todos los tokens fallan, retornar None

    def get_person(self, dni: str) -> Optional[dict]:
        """Fetches information about a person using their DNI."""
        response = self._get("/v2/reniec/dni", {"numero": dni})

        if response is None:
            logging.error("No se pudo obtener respuesta de la API.")
            return None

        # Puedes agregar un registro para ver el contenido de la respuesta
        logging.info(f"Respuesta de la API para DNI {dni}: {response}")

        return response
