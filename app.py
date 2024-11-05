from flask import Flask, render_template, request
from datetime import datetime
import pandas as pd
import itertools
import os
from utils.gpt_explainer import get_explanation  # Importamos la función
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def generate_truth_table(variables, expression):
    try:
        # Crear todas las combinaciones posibles
        combinations = list(itertools.product([True, False], repeat=len(variables)))
        results = []
        
        for combo in combinations:
            # Crear diccionario de valores para las variables
            values = dict(zip(variables, combo))
            row_result = values.copy()
            
            # Crear expresión evaluable
            expr = expression
            for var, val in values.items():
                expr = expr.replace(var, str(val))
            
            # Reemplazar operadores lógicos
            expr = (expr.replace('∧', ' and ')
                       .replace('∨', ' or ')
                       .replace('¬', ' not ')
                       .replace('→', ' <= ')
                       .replace('↔', ' == '))
            
            print(f"Evaluando expresión: {expr}")  # Debug
            
            # Evaluar la expresión de forma segura
            try:
                safe_dict = {
                    "True": True,
                    "False": False,
                    "and": lambda x, y: x and y,
                    "or": lambda x, y: x or y,
                    "not": lambda x: not x
                }
                result = eval(expr, {"__builtins__": {}}, safe_dict)
                row_result['Resultado'] = result
                results.append(row_result)
            except Exception as e:
                print(f"Error en evaluación: {str(e)}")
                raise
        
        # Crear DataFrame
        df = pd.DataFrame(results)
        return df[variables + ['Resultado']]
    except Exception as e:
        print(f"Error en generate_truth_table: {str(e)}")
        raise

@app.route('/')
def index():
    return render_template('input.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        expression = request.form.get('expression', '').strip()
        title = request.form.get('title', '').strip()
        print(f"Expresión recibida: {expression}")
        print(f"Título recibido: {title}")
        
        if not expression:
            raise ValueError("La expresión está vacía")
        
        variables = sorted(list({char for char in expression if char.isalpha() and char.isupper()}))
        print(f"Variables detectadas: {variables}")
        
        if not variables:
            raise ValueError("No se detectaron variables en la expresión")
        
        df = generate_truth_table(variables, expression)
        print("Tabla generada")
        
        df_display = df.copy()
        df_display = df_display.replace({True: 'V', False: 'F'})
        
        explanation = get_explanation(variables, expression, df)
        print("Explicación GPT generada")
        
        # Usar el título del formulario o generar uno por defecto
        display_title = title if title else f"Tabla de Verdad - {expression}"
        file_title = title if title else f"tabla_{expression.replace(' ', '_')}"
        
        # Sanitizar el título del archivo
        safe_file_title = "".join(c for c in file_title if c.isalnum() or c in ('_', '-')).strip()
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        
        # Crear directorio results si no existe
        os.makedirs('results', exist_ok=True)
        
        # Generar el contenido HTML
        html_content = render_template(
            'result.html',
            title=display_title,
            file_title=safe_file_title,
            expression=expression,
            variables=', '.join(variables),
            table=df_display.to_html(
                classes='table table-striped table-hover',
                index=True
            ),
            explanation=explanation,
            timestamp=timestamp
        )
        
        # Guardar el HTML en la carpeta results
        html_filename = f"results/tabla_verdad_{safe_file_title}.html"
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML guardado en: {html_filename}")
        
        return html_content
    
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        return render_template('error.html', error=error_msg)

if __name__ == '__main__':
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️ ADVERTENCIA: No se encontró OPENAI_API_KEY en las variables de entorno")
    print("Iniciando aplicación Flask...")
    app.run(debug=True, host='0.0.0.0', port=5000)