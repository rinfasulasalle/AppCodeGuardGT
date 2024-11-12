from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import json


### 1. PREPROCESAMIENTO DEL CÓDIGO SQL
def preprocess_sql(code):
    """Elimina comentarios, convierte a minúsculas y tokeniza el código SQL."""
    code = re.sub(r"--.*?(\n|$)|/\*.*?\*/", "", code, flags=re.DOTALL)  # Eliminar comentarios
    code = code.lower().strip()  # Convertir a minúsculas y eliminar espacios innecesarios
    tokens = re.findall(r"\b\w+\b", code)  # Tokenizar el código
    return " ".join(tokens)  # Convertir tokens a un string

### 2. APLICAR TF-IDF
def calculate_tfidf_matrix(codes):
    """Calcula la matriz TF-IDF para una lista de códigos SQL."""
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words=['select', 'from', 'where', 'and'])
    tfidf_matrix = vectorizer.fit_transform(codes)
    return tfidf_matrix

### 3. CALCULAR SIMILITUD DE COSENO
def calculate_cosine_similarity(tfidf_matrix):
    """Calcula la matriz de similitud de coseno entre los vectores TF-IDF."""
    return cosine_similarity(tfidf_matrix)

### 4. DETECTAR PLAGIO Y PREPARAR SALIDA JSON DETALLADA
def detect_plagiarism(data, threshold=0.8):
    """Detecta casos de plagio y devuelve una salida detallada en un diccionario."""
    # Comprobar si hay datos suficientes
    n = len(data)
    if n == 0:
        return {"error": "No hay códigos para analizar."}
    elif n == 1:
        return {"message": "Solo hay un código para analizar, no se puede comparar."}

    # Preprocesar los códigos SQL
    codes = [preprocess_sql(item['codigo_sql']) for item in data]
    tfidf_matrix = calculate_tfidf_matrix(codes)
    sim_matrix = calculate_cosine_similarity(tfidf_matrix)

    plagiarism_cases = []

    # Detectar plagio comparando cada código con los demás
    for i in range(n):
        for j in range(i + 1, n):
            similarity = sim_matrix[i, j]
            if similarity >= threshold:
                plagiarism_cases.append({
                    "codigo_a": {
                        "id_codigo": data[i]["id_codigo"],
                        "estudiante": data[i]["estudiante"],
                        "url_codigo": data[i]["url_codigo"]
                    },
                    "codigo_b": {
                        "id_codigo": data[j]["id_codigo"],
                        "estudiante": data[j]["estudiante"],
                        "url_codigo": data[j]["url_codigo"]
                    },
                    "similarity_score": round(similarity, 2)
                })

    # Formatear la salida en diccionario
    result = {
        "total_codes_analyzed": n,
        "threshold": threshold,
        "plagiarism_detected": len(plagiarism_cases) > 0,
        "plagiarism_cases": plagiarism_cases,
        "comparisons": [
            {
                "codigo_a": {
                    "id_codigo": data[i]["id_codigo"],
                    "estudiante": data[i]["estudiante"],
                },
                "codigo_b": {
                    "id_codigo": data[j]["id_codigo"],
                    "estudiante": data[j]["estudiante"],
                },
                "similarity_score": round(sim_matrix[i, j], 2)
            }
            for i in range(n) for j in range(i + 1, n)
        ]
    }

    return result  # Devuelve un diccionario, no un JSON

### 5. FUNCIÓN PRINCIPAL
def plagiarism_checker(datos, threshold=0.8):
    """Función principal para verificar plagio y retornar el resultado en JSON."""
    return detect_plagiarism(datos, threshold)
