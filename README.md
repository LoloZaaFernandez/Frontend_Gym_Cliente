#Cómo usarlo

Crea un entorno virtual (recomendado):

python -m venv venv


Actívalo:

En Windows:

venv\Scripts\activate


En Linux/macOS:

source venv/bin/activate


Instala las dependencias:

pip install -r requirements.txt


Ejecuta tu proyecto con:

uvicorn main:app --reload
