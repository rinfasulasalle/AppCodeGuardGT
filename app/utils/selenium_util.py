import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException, WebDriverException,
    InvalidArgumentException, SessionNotCreatedException
)

def setup_chrome_driver():
    """Configura el driver de Chrome con las opciones necesarias."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar en modo headless
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def extract_sql_code_from_url(url: str) -> str:
    """
    Extrae el código SQL del textarea de una página dada por la URL.
    
    Args:
        url (str): La URL de la página a procesar.

    Returns:
        str: El contenido del código SQL extraído.

    Raises:
        ValueError: Si la URL no contiene un ID válido.
        Exception: Para errores inesperados durante la extracción.
    """
    try:
        # Extraer el ID de la URL
        url_id = url.split('=')[-1]
    except IndexError:
        raise ValueError("La URL proporcionada no contiene un ID válido.")

    try:
        # Inicializar el driver usando un bloque 'with' para cierre automático
        with setup_chrome_driver() as driver:
            try:
                driver.get(url)
            except InvalidArgumentException:
                raise ValueError("La URL proporcionada no es válida.")

            # Esperar que el textarea con ID 'uiP2' esté presente
            textarea = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "uiP2"))
            )

            # Obtener el contenido del textarea y limpiar espacios
            sql_code = textarea.get_attribute("value").strip()

            if not sql_code:
                raise ValueError("El textarea está vacío.")

            return sql_code

    except TimeoutException:
        raise TimeoutException("El textarea no apareció a tiempo.")
    except NoSuchElementException:
        raise NoSuchElementException("No se encontró el elemento con ID 'uiP2'.")
    except SessionNotCreatedException as e:
        raise RuntimeError(f"No se pudo crear la sesión del navegador: {e}")
    except WebDriverException as e:
        raise RuntimeError(f"Error con WebDriver: {e}")
    except Exception as e:
        raise RuntimeError(f"Se produjo un error inesperado: {e}")
