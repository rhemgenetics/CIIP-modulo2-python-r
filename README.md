# Módulo 2: Programación Científica en Python y R para Bioestadística

**Docente:** Dr. Eric Jonathan Maciel Cruz

Repositorio oficial de materiales prácticos, scripts reproducibles y reportes del Módulo 2.

## Estructura del Repositorio

* `sesion-01-python-biologico/`: Programación Orientada a Objetos (POO), Biopython, Pandas y Seaborn.
* `sesion-02-r-tidyverse/`: Manipulación de datos clínicos con `dplyr` y visualización científica con `ggplot2`.
* `sesion-03-quarto-github/`: Reportes dinámicos reproducibles en Quarto / R Markdown y control de versiones en GitHub.

---

## Paso 1: Configuración del Entorno Virtual (Terminal en VS Code)

Antes de ejecutar cualquier código en Python, abre la carpeta `CIIP-modulo2-python-r` en **VS Code**, abre la terminal integrada (`Terminal -> New Terminal`) y ejecuta los comandos según tu sistema operativo:

### Windows (PowerShell)

python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

> **Nota:** Si PowerShell bloquea la activación por permisos, ejecuta primero 
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` 
> y vuelve a correr 
> `.venv\Scripts\Activate.ps1`.

### macOS / Linux (o Git Bash en Windows)

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

## Paso 2: Selección del Kernel y Ejecución

1. Abre `sesion-01-python-biologico/practica/s01_practica_alumno.py`.
2. En la esquina superior derecha del editor de VS Code, haz clic en **Select Kernel** (`Seleccionar kernel`) -> **Python Environments** y elige **`.venv`**.
3. Posiciona el cursor en la primera celda (`# %%`) y presiona **`Ctrl + Enter`** para avanzar bloque por bloque.