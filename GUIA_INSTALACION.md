# Guía de Instalación y Configuración desde Cero (VS Code + Python + Git)

**Visual Studio Code (VS Code)** es un editor de código, pero necesita tener instalados los motores de cada lenguaje en tu computadora para ejecutar tus análisis. Sigue estos pasos en orden exacto.

---

## Paso 1: Instalar los Motores Base (Python y Git)

Antes de instalar VS Code, instala estos dos programas fundamentales:

### 1.1 Python (versión 3.11 o 3.12 recomendada)
1. Descarga el instalador desde **[python.org/downloads](https://www.python.org/downloads/)**.
2. **En Windows (Paso crítico):** Al abrir el instalador, **marca obligatoriamente la casilla inferior `"Add python.exe to PATH"`** antes de hacer clic en *Install Now*. Si omites esta casilla, la terminal no reconocerá el comando `python`.
3. **En macOS:** Ejecuta el paquete `.pkg` descargado y sigue las instrucciones estándar.

### 1.2 Git (Control de versiones y terminal Bash)
1. Descarga el instalador desde **[git-scm.com/downloads](https://git-scm.com/downloads)**.
2. **En Windows:** Instala con todas las opciones predeterminadas (*Next* en todas las pantallas). Esto también instalará **Git Bash**, una terminal muy útil.
3. **En macOS:** Abre la aplicación **Terminal** y ejecuta `git --version`; si no está instalado, macOS abrirá una ventana para instalar las herramientas de línea de comandos automáticamente.

> **Nota para las Sesiones 2 y 3:** Más adelante necesitarás instalar **R** desde [cran.r-project.org](https://cran.r-project.org/) y **Quarto CLI** desde [quarto.org](https://quarto.org/docs/get-started/).

---

## Paso 2: Instalar Visual Studio Code

1. Descarga VS Code desde **[code.visualstudio.com](https://code.visualstudio.com/)**.
2. **En Windows:** Durante la instalación, cuando aparezca la pantalla *"Seleccionar tareas adicionales"*, marca todas las casillas disponibles:
   * `[x]` Agregar la acción "Abrir con Code" al menú contextual del explorador de archivos.
   * `[x]` Registrar Code como editor para tipos de archivo admitidos.
   * `[x]` **Agregar a PATH** (requiere reiniciar el shell).
3. **En macOS:** Descomprime el archivo descargado y arrastra **Visual Studio Code.app** hacia tu carpeta **Aplicaciones**.

---

## Paso 3: Instalar las Extensiones Indispensables

Abre VS Code y ve al panel de **Extensiones** haciendo clic en el ícono de los cuatro cuadros en la barra lateral izquierda (o presionando **`Ctrl + Shift + X`** en Windows / **`Cmd + Shift + X`** en Mac). Busca e instala las siguientes extensiones oficiales:

| Extensión | Publicador | Identificador | Función en el curso |
| :--- | :--- | :--- | :--- |
| **Python** | Microsoft | `ms-python.python` | Ejecución de scripts, autocompletado (Pylance) y detección de entornos `.venv`. |
| **Jupyter** | Microsoft | `ms-toolsai.jupyter` | Permite ejecutar celdas `# %%` con `Ctrl + Enter` y abrir notebooks `.ipynb`. |
| **Quarto** | Posit | `quarto.quarto` | Compilación de presentaciones y reportes científicos reproducibles (Sesión 3). |
| **R** | REditorSupport | `REditorSupport.r` | Soporte de sintaxis y ejecución de scripts `.R` (Sesión 2). |

### Instalación rápida en 1 paso (Opcional por terminal)
Si abres una terminal dentro de VS Code (**`Ctrl + ñ`** o menú superior **`Terminal -> New Terminal`**), puedes instalar las 4 extensiones simultáneamente ejecutando:

```bash
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
code --install-extension quarto.quarto
code --install-extension REditorSupport.r
```

---

## Paso 4: Activar Características Clave en VS Code

Configura estas tres funciones para evitar los errores más comunes durante las sesiones prácticas:

### 4.1 Activar el Auto-guardado (*Auto Save*)
Evita el error clásico de modificar el código y ejecutar una versión anterior sin guardar:
1. Ve al menú superior **`File`** (Archivo) y haz clic en **`Auto Save`** para que aparezca una palomita (`✓`) a su lado.

### 4.2 Verificar el soporte nativo de Notebooks (`ipynb`)
1. Presiona **`Ctrl + Shift + X`** (Extensiones).
2. En el buscador superior escribe exactamente: **`@builtin ipynb`**.
3. Verifica que las extensiones **Jupyter Notebook Renderers** e **ipynb** aparezcan habilitadas (si alguna dice *Enable*, haz clic en ella).

### 4.3 Habilitar permisos de entornos virtuales en Windows (Solo usuarios Windows)
Por seguridad, Windows bloquea la activación de entornos virtuales en PowerShell la primera vez. Para habilitarlo:
1. Abre la terminal en VS Code (**`Terminal -> New Terminal`**).
2. Pega y ejecuta este comando una sola vez:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

---

## Paso 5: Descargar el Material y Verificar todo en 2 Minutos

1. **Obtener el repositorio del curso:**
   * **Opción A (Con Git en terminal):**
     ```bash
     git clone [https://github.com/rhemgenetics/CIIP-modulo2-python-r.git](https://github.com/rhemgenetics/CIIP-modulo2-python-r.git)
     ```
   * **Opción B (Sin terminal):** Entra a [github.com/rhemgenetics/CIIP-modulo2-python-r](https://github.com/rhemgenetics/CIIP-modulo2-python-r), haz clic en el botón verde **`<> Code` -> `Download ZIP`** y descomprime la carpeta en tus Documentos.

2. **Abrir el proyecto:** En VS Code ve a **`File -> Open Folder...`** y selecciona la carpeta **`CIIP-modulo2-python-r`**.

3. **Crear y activar el entorno virtual (`.venv`):** Abre la terminal integrada (**`Terminal -> New Terminal`**) y ejecuta:
   * **Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     pip install -r requirements.txt
     ```
   * **macOS / Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     pip install -r requirements.txt
     ```

4. **Probar la ejecución interactiva:**
   * Abre `sesion-01-python-biologico/practica/s01_practica_alumno.py` (o su versión `.ipynb` si está disponible).
   * Observa que arriba de cada bloque `# %%` aparece el botón **`Run Cell`** (o coloca el cursor dentro de la celda y presiona **`Ctrl + Enter`**).
   * Al ejecutar el **Bloque 0**, se abrirá a la derecha la **Ventana Interactiva de Python** confirmando que el entorno virtual y las librerías (`Biopython`, `Pandas`, `Seaborn`) están listos.