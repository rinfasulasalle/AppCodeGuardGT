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

### 4. DETECTAR PLAGIO CON UMBRAL
def detect_plagiarism(sim_matrix, codes, threshold=0.8):
    """Detecta plagio y prepara la salida en formato JSON."""
    plagiarism_cases = []
    n = len(codes)

    for i in range(n):
        for j in range(i + 1, n):
            similarity = sim_matrix[i, j]
            if similarity >= threshold:
                plagiarism_cases.append({
                    "code_1_index": i,
                    "code_2_index": j,
                    "similarity_score": round(similarity, 2)
                })

    result = {
        "total_codes": n,
        "threshold": threshold,
        "plagiarism_detected": len(plagiarism_cases) > 0,
        "comparisons": [
            {
                "code_1_index": i,
                "code_2_index": j,
                "similarity_score": round(sim_matrix[i, j], 2)
            }
            for i in range(n) for j in range(i + 1, n)
        ],
        "plagiarism_cases": plagiarism_cases
    }

    return json.dumps(result, indent=4)

### 5. FLUJO PRINCIPAL DEL PROGRAMA
def plagiarism_checker(codes, threshold=0.8):
    """Función principal para detectar plagio y devolver salida JSON."""
    preprocessed_codes = [preprocess_sql(code) for code in codes]
    tfidf_matrix = calculate_tfidf_matrix(preprocessed_codes)
    sim_matrix = calculate_cosine_similarity(tfidf_matrix)
    return detect_plagiarism(sim_matrix, codes, threshold)

### EJEMPLO DE USO
if __name__ == "__main__":
    codes_sql = [
        "SELECT id, nombre FROM clientes WHERE edad > 18;",
        "SELECT id_cliente, nombre FROM usuarios WHERE edad > 18;",
        "INSERT INTO clientes (id, nombre) VALUES (1, 'John');",
        "SELECT * FROM clientes;",
        "SELECT nombre FROM usuarios WHERE edad >= 18;",
        "SELECT id, nombre FROM clientes WHERE edad > 18;"
    ]

    json_result = plagiarism_checker(codes_sql, threshold=0.8)
    print(json_result)
