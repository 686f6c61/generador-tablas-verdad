from datetime import datetime
from dotenv import load_dotenv
import os
from utils.table_generator import generate_truth_table
from utils.gpt_explainer import get_explanation
from jinja2 import Environment, FileSystemLoader
import pandas as pd
from markdown2 import Markdown

load_dotenv()

def main():
    print("\nSímbolos lógicos disponibles:")
    print("∧ : AND")
    print("∨ : OR")
    print("¬ : NOT")
    print("→ : Implicación")
    print("↔ : Bicondicional")
    print("\nEjemplo: (P∧Q)∨¬Q\n")
    
    # Obtener input del usuario y normalizar las variables
    variables = [var.upper() for var in input("Ingresa las variables (separadas por espacios): ").split()]
    expression = input("Ingresa la expresión lógica usando las variables ingresadas: ")
    title = input("Ingresa un título para la tabla (opcional, presiona Enter para usar timestamp): ").strip()
    
    # Generar título por defecto si no se proporciona
    if not title:
        title = f"Tabla de Verdad - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # Generar tabla de verdad
    df = generate_truth_table(variables, expression)
    
    # Obtener explicación de GPT-4
    explanation = get_explanation(variables, expression, df)
    
    # Guardar resultados en HTML
    save_results(df, explanation, title)
    
    # Mostrar resultados en consola
    print("\nTabla de Verdad:")
    print(df)
    print("\nExplicación:")
    print(explanation)

def save_results(df, explanation, title):
    # Asegurarse de que el directorio 'results' existe
    os.makedirs('results', exist_ok=True)
    
    # Asegurarse de que el directorio 'templates' existe y contiene result.html
    if not os.path.exists('templates'):
        os.makedirs('templates')
        
    # Configurar Jinja2
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('templates/result.html')
    
    # Sanitizar el título para usarlo como nombre de archivo
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).strip()
    safe_title = safe_title.replace(' ', '_')
    
    # Generar timestamp actual
    current_timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    
    # Añadir índice numerado empezando desde 1
    df_display = df.copy()
    df_display.index = range(1, len(df_display) + 1)
    df_display.index.name = '#'
    
    # Convertir valores booleanos a "V" y "F"
    df_display = df_display.replace({True: 'V', False: 'F'})
    
    # Convertir Markdown a HTML
    markdowner = Markdown(extras=['tables'])
    explanation_html = markdowner.convert(explanation)
    
    # Limpiar cualquier formato residual y aplicar estilos personalizados
    explanation_html = (explanation_html
        .replace('<strong>', '<span class="step">')
        .replace('</strong>', '</span>')
        .replace('<em>', '')
        .replace('</em>', '')
        .replace('###', '')
        .replace('##', '')
        .replace('#', ''))
    
    # Renderizar el template con estilos mejorados
    html_content = template.render(
        title=title,
        table=df_display.to_html(
            classes='table table-striped table-hover',
            index=True
        ),
        explanation=explanation_html,
        timestamp=current_timestamp
    )
    
    # Guardar en el directorio 'results'
    filename = f"results/tabla_verdad_{safe_title}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\nResultados guardados en: {filename}")

if __name__ == "__main__":
    main()
