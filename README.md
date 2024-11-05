# Generador de Tablas de Verdad 🎯

Un generador de tablas de verdad interactivo con explicaciones detalladas generadas por GPT-4 Turbo. Esta herramienta educativa permite crear, visualizar y entender tablas de verdad para expresiones lógicas.

![Interfaz del Generador de Tablas de Verdad](/img/tablas-verdad.png)

## 🌟 Características

- Interfaz web intuitiva para construir expresiones lógicas
- Soporte para múltiples operadores lógicos (∧, ∨, ¬, →, ↔)
- Generación automática de tablas de verdad
- Explicaciones detalladas paso a paso usando GPT-4 Turbo
- Exportación a HTML y TXT
- Diseño responsivo y amigable
- Impresión optimizada de resultados

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3.x, Flask
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **IA**: OpenAI GPT-4 Turbo
- **Dependencias Principales**:
  - `pandas`: Manipulación de datos y generación de tablas
  - `openai`: Integración con GPT-4 Turbo
  - `python-dotenv`: Gestión de variables de entorno
  - `jinja2`: Motor de plantillas
  - `markdown2`: Formateo de texto

## 📋 Requisitos Previos

1. Python 3.x instalado
2. Una clave API de OpenAI
3. pip (gestor de paquetes de Python)

## 🚀 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/686f6c61/generador-tablas-verdad.git
cd generador-tablas-verdad
```

2. Crear y activar entorno virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
# Crear archivo .env
OPENAI_API_KEY=tu_api_key_aquí
```

## 💻 Uso

1. Iniciar el servidor:
```bash
python3 app.py
```

2. Abrir en el navegador:
```
http://localhost:5000
```

3. Usar la interfaz para:
   - Seleccionar variables (P, Q, R)
   - Construir expresiones lógicas
   - Generar tablas de verdad
   - Ver explicaciones detalladas
   - Exportar resultados

## 📁 Estructura del Proyecto

```
generador-tablas-verdad/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias del proyecto
├── .env                  # Variables de entorno (no incluido en git)
├── templates/            # Plantillas HTML
│   ├── input.html       # Página principal
│   ├── result.html      # Página de resultados
│   └── error.html       # Página de error
├── utils/               # Utilidades
│   ├── __init__.py
│   ├── table_generator.py  # Generador de tablas
│   └── gpt_explainer.py   # Integración con GPT-4
├── img/
│   ├── tablas-verdad.png        # Captura de la interfaz principal
│   └── tabla-verdad-resultados.png  # Captura de los resultados
└── results/             # Resultados generados (no incluido en git)
```

## 🔍 Características Detalladas

### Operadores Soportados
- `∧` : AND (Conjunción)
- `∨` : OR (Disyunción)
- `¬` : NOT (Negación)
- `→` : Implicación
- `↔` : Bicondicional

### Funcionalidades
1. **Generación de Tablas**
   - Evaluación automática de expresiones
   - Formato visual mejorado
   - Valores V/F coloreados

2. **Explicaciones GPT-4**
   - Análisis de la expresión
   - Evaluación por filas
   - Conclusiones y patrones

3. **Exportación**
   - Formato HTML con estilos
   - Versión TXT plana
   - Impresión optimizada

![Resultados y Explicación](/img/tabla-verdad-resultados.png)

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Haz Fork del proyecto
2. Crea una rama para tu característica
3. Realiza tus cambios
4. Envía un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.


---
Desarrollado con ❤️ por [686f6c61](https://www.686f6c61.dev/)
