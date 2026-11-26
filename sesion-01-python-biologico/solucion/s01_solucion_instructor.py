# %% [markdown]
# # Sesión 1: Python Biológico desde Cero
#
# ### Preparación inicial en Terminal (ejecutar una sola vez antes de iniciar):
# 1. Abre la terminal en VS Code (`Terminal -> New Terminal`).
# 2. Crea y activa tu entorno virtual:
#    * **Windows (PowerShell):** `python -m venv .venv` y luego `.venv\Scripts\Activate.ps1`
#    * **Mac / Linux / Git Bash:** `python3 -m venv .venv` y luego `source .venv/bin/activate`
# 3. En la esquina superior derecha de este archivo, haz clic en **Select Kernel** y elige **`.venv`**.
# 4. Presiona **`Ctrl + Enter`** dentro de cada celda (`# %%`) para ejecutar paso a paso.

# %%
# ==============================================================================
# BLOQUE 0: VERIFICACIÓN DE ENTORNO VIRTUAL E INSTALACIÓN DE PAQUETES
# ==============================================================================
import sys
import subprocess
import importlib.util

# 1. Comprobar que el alumno seleccionó el entorno virtual (.venv) en VS Code
if sys.prefix == sys.base_prefix:
    print("ADVERTENCIA: No estas dentro de un entorno virtual (.venv).")
    print(" -> Crea .venv en la terminal y seleccionalo en 'Select Kernel' (arriba a la derecha).")
else:
    print(f"Entorno virtual activo: {sys.prefix}")

# 2. Verificar e instalar dependencias faltantes dentro del .venv
paquetes_requeridos = {
    "Bio": "biopython",
    "pandas": "pandas",
    "seaborn": "seaborn",
    "matplotlib": "matplotlib"
}

print("\nVerificando paquetes necesarios en tu entorno...\n")

for modulo, paquete_pip in paquetes_requeridos.items():
    if importlib.util.find_spec(modulo) is None:
        print(f"Instalando '{paquete_pip}'...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", paquete_pip])
        print(f" -> '{paquete_pip}' instalado correctamente.")
    else:
        print(f" -> '{paquete_pip}' ya se encuentra instalado.")

import Bio
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

print("\n--- ENTORNO LISTO PARA TRABAJAR ---")
print(f"Python:     {sys.version.split()[0]}")
print(f"Biopython:  {Bio.__version__}")
print(f"Pandas:     {pd.__version__}")
print(f"Seaborn:    {sns.__version__}")
print(f"Matplotlib: {matplotlib.__version__}")

# %%
# ==============================================================================
# BLOQUE 1: DE TEXTO PLANO A BIOPYTHON (LO MÁS BÁSICO)
# ==============================================================================
from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction, molecular_weight

adn_texto = "ATGGAGGAGCCGCAGTCAGATCCTAGCGTCGAGCCCCCTCTGTGA"
print("Tipo en Python básico:", type(adn_texto))

adn_bio = Seq(adn_texto)
print("Tipo en Biopython:    ", type(adn_bio))

complementaria = adn_bio.complement()
reversa_comp   = adn_bio.reverse_complement()
arn_mensajero  = adn_bio.transcribe()
proteina       = adn_bio.translate(to_stop=True)
porcentaje_gc  = round(gc_fraction(adn_bio) * 100, 2)

print("\n--- RESULTADOS DEL ANÁLISIS BÁSICO ---")
print(f"ADN (5'->3'):       {adn_bio}")
print(f"Complementaria:     {complementaria}")
print(f"Reversa Comp.:      {reversa_comp}")
print(f"ARNm transcrito:    {arn_mensajero}")
print(f"Proteína traducida: {proteina} ({len(proteina)} aminoácidos)")
print(f"Contenido GC:       {porcentaje_gc}%")

# %%
# ==============================================================================
# BLOQUE 2: PROGRAMACIÓN ORIENTADA A OBJETOS (POO) APLICADA A SECUENCIAS
# ==============================================================================
class Secuencia:
    """Molde para representar y analizar una secuencia codificante de ADN (CDS)."""
    
    BASES_VALIDAS = {"A", "T", "C", "G", "N"}

    def __init__(self, id_gen: str, secuencia_str: str, categoria: str = "Sin clasificar"):
        self.id_gen = id_gen.strip()
        self.categoria = categoria.strip()
        
        secuencia_limpia = secuencia_str.upper().replace(" ", "").replace("\n", "")
        caracteres_raros = set(secuencia_limpia) - self.BASES_VALIDAS
        if caracteres_raros:
            raise ValueError(f"Error en '{self.id_gen}': caracteres no válidos {caracteres_raros}")
        
        self.seq = Seq(secuencia_limpia)

    def calcular_gc(self) -> float:
        return round(gc_fraction(self.seq) * 100, 2)

    def transcribir(self) -> str:
        return str(self.seq.transcribe())

    def traducir(self) -> str:
        if len(self.seq) % 3 != 0:
            raise ValueError(f"Error en '{self.id_gen}': la longitud ({len(self.seq)} pb) no es múltiplo de 3.")
        return str(self.seq.translate(to_stop=True))

    def peso_kda(self) -> float:
        return round(molecular_weight(self.seq, seq_type="DNA") / 1000, 2)

    def exportar_fila(self) -> dict:
        """Empaqueta los resultados del objeto en un diccionario para Pandas."""
        peptido = self.traducir()
        return {
            "Gen": self.id_gen,
            "Categoria": self.categoria,
            "Longitud_pb": len(self),
            "Longitud_aa": len(peptido),
            "Porcentaje_GC": self.calcular_gc(),
            "Peso_kDa": self.peso_kda(),
            "Peptido_Inicio": peptido[:6] + "..."
        }

    def __len__(self) -> int:
        return len(self.seq)

    def __repr__(self) -> str:
        return f"<Secuencia '{self.id_gen}' | {self.categoria} | {len(self)} pb | GC={self.calcular_gc()}%>"

gen_ejemplo = Secuencia("TP53_demo", "ATGGAGGAGCCGCAGTCAGATCCTAGCGTCGAGCCCCCTCTGTGA", "Supresor Tumoral")
print("Objeto creado:", gen_ejemplo)
print("Longitud con len():", len(gen_ejemplo), "pares de bases")
print("Proteína:", gen_ejemplo.traducir())

# %%
# ==============================================================================
# BLOQUE 3: LECTURA DE ARCHIVOS FASTA Y CONSOLIDACIÓN EN PANDAS
# ==============================================================================
import io
from Bio import SeqIO

fasta_clinico = """
>TP53_DBD|Supresor_Tumoral
ATGGAGGAGCCGCAGTCAGATCCTAGCGTCGAGCCCCCTCTGAGTCAGGAAACATTTTCAGACCTATGGAAACTACTTCCTGAAAACAACGTTCTGTCCCCCTTGTGA
>BRCA1_RING|Supresor_Tumoral
ATGGATTTATCTGCTCTTCGCGTTGAAGAAGTACAAAATGTCATTAATGCTATGCAGAAAATCTTAGAGTGTCCCATCTGTCTGGAGTTGATCAAGTAA
>APC_MCR|Supresor_Tumoral
ATGGCTGCAGCTTCATATGATCAGTTGTTAAAGCAAGTTGAGGCACTGAAGATGGAGAACTCAAATCTTCGACAAGAGCTAGAAGATTAA
>KRAS_G12|Oncogen
ATGACTGAATATAAACTTGTGGTAGTTGGAGCTGGTGGCGTAGGCAAGAGTGCCTTGACGATACAGCTAATTCAGAATCATTTTGTGTAG
>BRAF_V600|Oncogen
ATGGCGGCGCTGAGCGGTGGCGGTGGTGGCGGCGCGGAGCCGGGCCAGGCTCTGTTCAACGGGGACATGGAGCCCGAGGCCGGCGCCTGA
>EGFR_TK|Oncogen
ATGCGACCCTCCGGGACGGCCGGGGCAGCGCTCCTGGCGCTGCTGGCTGCGCTCTGCCCGGCGAGTCGGGCTCTGGAGGAAAAGAAAGTTTGCCAATAA
>PIK3CA_H1047|Oncogen
ATGCCTCCACGACCATCATCAGGTGAACTGTGGGGCATCCACTTGATGCCCCCAAGAATCCTAGTAGAATGTTTACTATGA
>CYP2D6_PGx|Farmacogen
ATGGGGCTAGAAGCACTGGTGCCCCTGGCCGTGATAGTGGCCATCTTCCTGCTCCTGGTGGACCTGATGCACCGGCGCCAACGCTGGGCTGCACGCTGA
""".strip()

archivo_memoria = io.StringIO(fasta_clinico)
mis_genes = []

for registro in SeqIO.parse(archivo_memoria, "fasta"):
    nombre, rol = registro.id.split("|")
    objeto_gen = Secuencia(
        id_gen=nombre,
        secuencia_str=str(registro.seq),
        categoria=rol.replace("_", " ")
    )
    mis_genes.append(objeto_gen)

print(f"Se cargaron {len(mis_genes)} genes como objetos Secuencia:\n")
for g in mis_genes:
    print(" ", g)

tabla_genes = pd.DataFrame([g.exportar_fila() for g in mis_genes])
tabla_genes = tabla_genes.sort_values(by="Porcentaje_GC", ascending=False).reset_index(drop=True)

print("\n--- TABLA DE RESULTADOS GENÓMICOS ---")
print(tabla_genes.to_string(index=False))

resumen_grupos = (
    tabla_genes
    .groupby("Categoria", as_index=False)
    .agg(
        Total_Genes=("Gen", "count"),
        Media_GC=("Porcentaje_GC", "mean"),
        Media_Aminoacidos=("Longitud_aa", "mean")
    )
    .round(2)
)

print("\n--- RESUMEN POR ROL FUNCIONAL ---")
print(resumen_grupos.to_string(index=False))

# %%
# ==============================================================================
# BLOQUE 4: VISUALIZACIÓN CIENTÍFICA CON SEABORN
# ==============================================================================
from pathlib import Path

sns.set_theme(style="whitegrid", context="notebook", palette="colorblind")

fig, axes = plt.subplots(1, 2, figsize=(13, 5), dpi=150)

# Gráfico 1: Contenido GC por gen ordenado
sns.barplot(
    data=tabla_genes,
    x="Porcentaje_GC",
    y="Gen",
    hue="Categoria",
    dodge=False,
    ax=axes[0]
)
media_gc = tabla_genes["Porcentaje_GC"].mean()
axes[0].axvline(media_gc, color="#D55E00", linestyle="--", linewidth=1.5, label=f"Media ({media_gc:.1f}%)")
axes[0].set_title("A. Contenido GC (%) por Locus", fontweight="bold", loc="left")
axes[0].set_xlabel("Contenido Guanina-Citosina (%)")
axes[0].set_ylabel("Gen Analizado")
axes[0].set_xlim(0, 85)
axes[0].legend(title="Categoría", loc="lower right")

# Gráfico 2: Relación entre Peso Molecular (kDa) y Contenido GC (%)
sns.scatterplot(
    data=tabla_genes,
    x="Peso_kDa",
    y="Porcentaje_GC",
    hue="Categoria",
    style="Categoria",
    s=130,
    ax=axes[1]
)
for _, fila in tabla_genes.iterrows():
    axes[1].text(
        fila["Peso_kDa"] + 0.3,
        fila["Porcentaje_GC"] + 0.4,
        fila["Gen"].split("_")[0],
        fontsize=9
    )

axes[1].set_title("B. Peso Molecular vs. Contenido GC", fontweight="bold", loc="left")
axes[1].set_xlabel("Peso Molecular ADN (kDa)")
axes[1].set_ylabel("Contenido GC (%)")
axes[1].set_xlim(23, 35)
axes[1].set_ylim(35, 80)
axes[1].legend(title="Categoría", loc="lower right")

sns.despine(top=True, right=True)
plt.tight_layout()

# Detección automática de la carpeta output/ sin importar desde dónde ejecute VS Code
if Path("sesion-01-python-biologico/output").exists():
    ruta_salida = Path("sesion-01-python-biologico/output/resultado_sesion1_genomica.png")
elif Path("../output").exists():
    ruta_salida = Path("../output/resultado_sesion1_genomica.png")
else:
    ruta_salida = Path("resultado_sesion1_genomica.png")

plt.savefig(ruta_salida, dpi=300)
print(f"Gráfico guardado exitosamente en: {ruta_salida}")
plt.show()