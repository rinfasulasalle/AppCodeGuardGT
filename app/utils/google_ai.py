import google.generativeai as genai
import logging
from typing import Optional

class GoogleGenerativeAI:
    def __init__(self) -> None:
        # Lista de tokens
        self.tokens = [
            "AIzaSyANSLNAc0Ns_FUsHLNyURaCb2rDSX3xJKA",
            "AIzaSyBbHCm0O81x0MgKBG28wc6LOOeR1mSYxAY",
            "AIzaSyBd6gAea93C8wsUFpbZQnyPl6_TVtGun9c"
        ]
        self.token_index = 0  # Índice actual del token a usar
        self.model_name = "gemini-1.5-flash"
        
        # Configura el primer token
        self._set_token(self.tokens[self.token_index])

    def _set_token(self, token: str):
        """
        Configura el token actual para la sesión.
        """
        genai.configure(api_key=token)

    def _rotate_token(self):
        """
        Cambia al siguiente token en caso de fallo.
        """
        self.token_index = (self.token_index + 1) % len(self.tokens)
        self._set_token(self.tokens[self.token_index])
        logging.info(f"Cambiado al token {self.token_index + 1}")

    def generate_content(self, prompt: str) -> Optional[str]:
        """
        Genera contenido usando el prompt dado. Si un token falla, se intenta con el siguiente.
        :param prompt: El texto de entrada para la generación de contenido.
        :return: Texto generado o None si todos los tokens fallan.
        """
        for _ in range(len(self.tokens)):  # Intentar con todos los tokens disponibles
            try:
                model = genai.GenerativeModel(self.model_name)
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                logging.error(f"Error al generar contenido: {e}")
                self._rotate_token()

        logging.error("Todos los tokens fallaron en generar el contenido.")
        return None  # Si todos los tokens fallan, retornar None
def ask_to_ia_google(prompt_total: str) -> Optional[str]:
    """
    Función para interactuar con la IA generativa.
    :param prompt_total: El texto completo (prompt) con la consulta para la IA.
    :return: Respuesta generada por la IA o None si falla.
    """
    gen_ai = GoogleGenerativeAI()  # Instanciamos la clase
    response = gen_ai.generate_content(prompt_total)
    return response