import pandas as pd
import itertools

def generate_truth_table(variables, expression):
    # Crear todas las combinaciones posibles de valores de verdad
    combinations = list(itertools.product([True, False], repeat=len(variables)))
    
    # Crear un diccionario para almacenar los resultados
    results = []
    
    # Para cada combinación de valores de verdad
    for combo in combinations:
        # Crear un diccionario con los valores de las variables
        values = dict(zip(variables, combo))
        
        # Crear una copia local de la expresión para evaluación
        expr = expression
        
        # Reemplazar cada variable con su valor booleano
        for var, val in values.items():
            expr = expr.replace(var, str(val))
            
        # Normalizar operadores lógicos
        expr = (expr
            .replace('∧', 'and')
            .replace('∨', 'or')
            .replace('¬', 'not ')
            .replace('→', '<=')
            .replace('↔', '=='))
        
        # Crear un entorno seguro para eval()
        safe_dict = {
            'True': True,
            'False': False,
            'and': lambda x, y: x and y,
            'or': lambda x, y: x or y,
            'not': lambda x: not x
        }
        
        try:
            # Evaluar la expresión en el entorno seguro
            result = eval(expr, {"__builtins__": {}}, safe_dict)
            values['Resultado'] = result
            results.append(values)
        except Exception as e:
            print(f"Error evaluando la expresión: {e}")
            print(f"Expresión original: {expression}")
            print(f"Expresión procesada: {expr}")
            print(f"Variables y valores: {values}")
            raise ValueError(f"Error al evaluar la expresión: {str(e)}")
    
    # Crear DataFrame con los resultados
    df = pd.DataFrame(results)
    
    # Reordenar las columnas para que el resultado esté al final
    cols = variables + ['Resultado']
    df = df[cols]
    
    return df