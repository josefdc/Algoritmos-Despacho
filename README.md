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


## Prompts de Demostración para Presentación

1. **Comparación entre Algoritmos de Planificación:**
   - **Prompt:** `¿Cuál es la diferencia en el tiempo de espera total y promedio cuando se utiliza el algoritmo FIFO en comparación con SJF y Prioridad para los procesos actuales? ¿Cuál es más eficiente en términos de tiempo de espera?`
   
2. **Análisis de Resultados en Detalle:**
   - **Prompt:** `Explica cómo se ejecutan los procesos en el diagrama de Gantt cuando se utiliza el algoritmo de planificación Prioridad. ¿Qué impacto tiene esto en el tiempo de finalización y de espera?`

3. **Sugerencias para Optimización del Algoritmo:**
   - **Prompt:** `Dado el conjunto de procesos actuales y sus tiempos de llegada y ejecución, ¿cuál es el algoritmo de planificación más óptimo y por qué?`

4. **Predicción de Comportamiento con Cambios en los Procesos:**
   - **Prompt:** `Si el tiempo de llegada del proceso P3 se retrasa en 4 unidades de tiempo, ¿cómo cambiaría el diagrama de Gantt y el tiempo de espera total utilizando el algoritmo SJF?`

5. **Impacto Visual del Diagrama de Gantt:**
   - **Prompt:** `Describe el diagrama de Gantt actual en detalle y explica cómo la ejecución secuencial de los procesos afecta el tiempo de finalización de cada uno.`

6. **Reflexión sobre la Eficiencia del Sistema:**
   - **Prompt:** `Basado en los resultados de los algoritmos de planificación que hemos probado, ¿qué conclusiones se pueden sacar sobre la eficiencia de nuestro sistema para gestionar procesos de alta prioridad?`

7. **Evaluación del Tiempo de Ejecución de Procesos:**
   - **Prompt:** `¿Cuál es el efecto de cambiar la prioridad de P1 a 1 (la más alta) en el tiempo total de ejecución y cómo afecta a los otros procesos en el algoritmo de Prioridad?`

8. **Estrategias de Mejoramiento:**
   - **Prompt:** `¿Qué estrategias podríamos considerar para mejorar el tiempo de espera promedio de los procesos utilizando algoritmos de planificación más avanzados o ajustando los parámetros actuales?`

