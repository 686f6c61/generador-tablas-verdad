from openai import OpenAI
import os

def get_explanation(variables, expression, df):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    prompt = f"""
    Explica paso a paso la siguiente tabla de verdad:
    Variables: {', '.join(variables)}
    Expresión: {expression}
    
    Tabla:
    {df.to_string()}
    
    Por favor, proporciona una explicación detallada siguiendo esta estructura:
    
    1. Análisis de la Expresión
    - Explica el significado de cada variable
    - Describe los operadores utilizados
    - Descompón la expresión en subexpresiones si es compleja
    
    2. Evaluación por Filas
    - Analiza cada fila de la tabla
    - Explica cómo se obtiene el resultado
    - Usa el formato "Fila N:" para cada explicación
    
    3. Conclusiones
    - Patrones observados
    - Casos particulares importantes
    - Equivalencias o propiedades lógicas relevantes
    
    Formato requerido:
    - Usa los símbolos ∧, ∨, ¬, →, ↔ para operadores
    - Usa V y F para valores de verdad
    - Separa cada sección con líneas en blanco
    - Enumera las secciones como "1.", "2.", "3."
    - Para cada fila usa "Fila N:"
    - No uses markdown ni formato especial
    """
    
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{
            "role": "user", 
            "content": prompt
        }],
        temperature=0.7,
        max_tokens=2000
    )
    
    explanation = response.choices[0].message.content
    
    # Limpiar y formatear la explicación
    explanation = (explanation
        .replace('**', '')
        .replace('*', '')
        .replace('###', '')
        .replace('#', '')
        .replace('\n\n\n', '\n\n')  # Eliminar espacios excesivos
    )
    
    return explanation