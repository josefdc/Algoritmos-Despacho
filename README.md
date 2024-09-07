# Algoritmos de Despacho

Este proyecto implementa algoritmos de despacho de procesos con una interfaz gráfica utilizando PyQt5 y OpenAI.

## Requisitos

- Python 3.7 o superior

## Instalación

Siga los siguientes pasos para configurar y ejecutar el proyecto en su máquina local:

### 1. Clonar el Repositorio

```bash
git clone https://github.com/josefdc/Algoritmos-Despacho.git
cd Algoritmos-Despacho
```
### 2. Crear un Entorno Virtual

Cree un entorno virtual para mantener las dependencias del proyecto aisladas del sistema global.

**En linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```
### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```


### 4. Configurar las Variables de Entorno

Cree un archivo `.env` en la raíz del proyecto para almacenar su clave de API de OpenAI:

```bash

OPENAI_API_KEY=su_clave_de_api_aqui
```

Asegúrese de reemplazar `su_clave_de_api_aqui` con su clave de API real de OpenAI.

### 5. Ejecutar la Aplicación

Ejecute el archivo `main.py` para iniciar la aplicación:

```bash
python src/main.py
```

### 6. Ejecutar Pruebas

Para ejecutar las pruebas unitarias y verificar que todo funcione correctamente, use:

```bash
python -m unittest discover tests
```


## Notas

- Asegúrese de tener configurado el entorno virtual siempre que trabaje en el proyecto.
- No comparta su archivo `.env` ni su clave de API en repositorios públicos.

## Licencia

Este proyecto está bajo la Licencia MIT - vea el archivo [LICENSE](LICENSE) para más detalles.
