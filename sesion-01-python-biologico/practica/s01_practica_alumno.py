# %% [markdown]
# # Sesión 1: Python Biológico desde Cero (Práctica Interactiva)
# **Nombre del alumno:** [Escribe tu nombre aquí]
#
# ### Instrucciones:
# 1. Verifica que arriba a la derecha (**Select Kernel**) esté seleccionado **`.venv`**.
# 2. Ejecuta cada bloque (`# %%`) de arriba hacia abajo presionando **`Ctrl + Enter`**.
# 3. En cada **`# TODO`**, borra únicamente el símbolo **`# `** al inicio de la línea indicada (o presiona `Ctrl + }` / `Ctrl + /`) y vuelve a ejecutar el bloque con **`Ctrl + Enter`** para ver el cambio.

# %%
# ==============================================================================
# BLOQUE 0: VERIFICACIÓN DE ENTORNO Y PAQUETES (Presiona Ctrl + Enter)
# ==============================================================================
import sys
import subprocess
import importlib.util

if sys.prefix == sys.base_prefix:
    print("ADVERTENCIA: Selecciona '.venv' arriba a la derecha (Select Kernel).")
else:
    print(f"Entorno virtual activo: {sys.prefix}")

paquetes_requeridos = {
    "Bio": "biopython",
    "pandas": "pandas",
    "seaborn": "seaborn",
    "matplotlib": "matplotlib"
}

for modulo, paquete_pip in paquetes_requeridos.items():
    if importlib.util.find_spec(modulo) is None:
        print(f"Instalando '{paquete_pip}'...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", paquete_pip])

import Bio
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

print(f"\nTodo listo. Python {sys.version.split()[0]} | Biopython {Bio.__version__} | Pandas {pd.__version__}")

# %%
# ==============================================================================
# BLOQUE 1: CALENTAMIENTO CON BIOPYTHON (Presiona Ctrl + Enter y observa)
# ==============================================================================
from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction, molecular_weight

adn_tp53 = Seq("ATGGAGGAGCCGCAGTCAGATCCTAGCGTCGAGCCCCCTCTGTGA")

complementaria = adn_tp53.complement()
reversa_comp   = adn_tp53.reverse_complement()
arn_mensajero  = adn_tp53.transcribe()
proteina       = adn_tp53.translate(to_stop=True)
porcentaje_gc  = round(gc_fraction(adn_tp53) * 100, 2)

print("--- RESULTADOS DEL DOGMA CENTRAL ---")
print("ADN original:      ", adn_tp53)
print("Complementaria:    ", complementaria)
print("Reversa comp.:     ", reversa_comp)
print("ARNm transcrito:   ", arn_mensajero)
print("Proteína obtenida: ", proteina)
print("Contenido GC (%):  ", porcentaje_gc)

# %%
# ==============================================================================
# BLOQUE 2: TU PRIMERA CLASE EN PYTHON ('Secuencia')
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
            raise ValueError(f"Error en '{self.id_gen}': letras no válidas {caracteres_raros}")
        
        self.seq = Seq(secuencia_limpia)

    def calcular_gc(self) -> float:
        return round(gc_fraction(self.seq) * 100, 2)

    def transcribir(self) -> str:
        # TODO 1: Borra el '#' de la siguiente línea para activar la transcripción a ARNm:
        # return str(self.seq.transcribe())
        return "Pendiente (activa el TODO 1)"

    def traducir(self) -> str:
        if len(self.seq) % 3 != 0:
            raise ValueError(f"Error en '{self.id_gen}': la longitud no es múltiplo de 3.")
        # TODO 2: Borra el '#' de la siguiente línea para activar la traducción a proteína:
        # return str(self.seq.translate(to_stop=True))
        return "Pendiente (activa el TODO 2)"

    def peso_kda(self) -> float:
        return round(molecular_weight(self.seq, seq_type="DNA") / 1000, 2)

    def exportar_fila(self) -> dict:
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

# Probamos nuestro molde con un gen de ejemplo:
gen_ejemplo = Secuencia("TP53_demo", "ATGGAGGAGCCGCAGTCAGATCCTAGCGTCGAGCCCCCTCTGTGA", "Supresor Tumoral")
print("Objeto creado: ", gen_ejemplo)
print("ARNm obtenido: ", gen_ejemplo.transcribir())
print("Proteína:      ", gen_ejemplo.traducir())

# %%
# ==============================================================================
# BLOQUE 3: LECTURA DE UN ARCHIVO FASTA Y TABLA EN PANDAS
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
    mis_genes.append(
        Secuencia(id_gen=nombre, secuencia_str=str(registro.seq), categoria=rol.replace("_", " "))
    )

tabla_genes = pd.DataFrame([g.exportar_fila() for g in mis_genes])

# TODO 3: Borra el '#' de la siguiente línea para ordenar la tabla de mayor a menor %GC:
# tabla_genes = tabla_genes.sort_values(by="Porcentaje_GC", ascending=False).reset_index(drop=True)

print("--- TABLA DE RESULTADOS GENÓMICOS ---")
print(tabla_genes.to_string(index=False))

# %%
# ==============================================================================
# BLOQUE 4: VISUALIZACIÓN CIENTÍFICA CON SEABORN
# ==============================================================================
from pathlib import Path

sns.set_theme(style="whitegrid", context="notebook", palette="colorblind")
fig, axes = plt.subplots(1, 2, figsize=(13, 5), dpi=150)

# Panel izquierdo (axes[0] — ya activo como referencia):
sns.barplot(data=tabla_genes, x="Longitud_pb", y="Gen", hue=None, dodge=False, ax=axes[0])

# TODO 4: Borra el '#' de la siguiente línea para activar el gráfico de %GC por categoría:
# sns.barplot(data=tabla_genes, x="Porcentaje_GC", y="Gen", hue="Categoria", dodge=False, ax=axes[1])

axes[0].set_title("A. Referencia: Longitud (pb) por Gen", fontweight="bold", loc="left")
axes[1].set_title("B. Tu Gráfico: Contenido GC (%) por Rol", fontweight="bold", loc="left")
axes[1].set_xlim(0, 85)

sns.despine(top=True, right=True)
plt.tight_layout()

ruta_salida = Path("sesion-01-python-biologico/output/mi_grafico_s01.png") if Path("sesion-01-python-biologico/output").exists() else Path("mi_grafico_s01.png")
plt.savefig(ruta_salida, dpi=300)
print(f"Gráfico guardado en: {ruta_salida}")
plt.show()

# %%
# ==============================================================================
# BLOQUE 5: DESCARGA DE SECUENCIAS REALES DESDE NCBI REFSEQ (Internet)
# ==============================================================================
import time
from pathlib import Path
from Bio import Entrez
from Bio.SeqRecord import SeqRecord

Entrez.email = "alumno@ciip.edu.mx"

catalogo_ncbi = {
    "NM_000546.6": ("TP53",   "Supresor Tumoral"),
    "NM_007294.4": ("BRCA1",  "Supresor Tumoral"),
    "NM_004985.5": ("KRAS",   "Oncogen"),
    "NM_004333.6": ("BRAF",   "Oncogen"),
    "NM_005228.5": ("EGFR",   "Oncogen"),
    "NM_000106.6": ("CYP2D6", "Farmacogen"),
    # TODO 5: Borra el '#' de la siguiente línea para descargar también el gen supresor APC:
    # "NM_000038.6": ("APC",    "Supresor Tumoral"),
}

carpeta_data = Path("sesion-01-python-biologico/data") if Path("sesion-01-python-biologico/data").exists() else Path("data")
carpeta_data.mkdir(parents=True, exist_ok=True)
archivo_fasta_real = carpeta_data / "refseq_cds_humano.fasta"

registros_cds = []

print("Conectando con NCBI Nucleotide (RefSeq)...\n")
for accesion, (simbolo, rol) in catalogo_ncbi.items():
    handle = Entrez.efetch(db="nucleotide", id=accesion, rettype="gb", retmode="text")
    registro_gb = SeqIO.read(handle, "genbank")
    handle.close()

    for feature in registro_gb.features:
        if feature.type == "CDS":
            secuencia_cds = feature.extract(registro_gb.seq)
            registros_cds.append(
                SeqRecord(secuencia_cds, id=f"{simbolo}_{accesion}|{rol.replace(' ', '_')}", description="")
            )
            print(f" -> Descargado {simbolo} ({accesion}): {len(secuencia_cds)} pb")
            break
    time.sleep(0.5)

SeqIO.write(registros_cds, archivo_fasta_real, "fasta")
print(f"\nArchivo FASTA real guardado en: {archivo_fasta_real}")

# %%
# ==============================================================================
# BLOQUE 6: ANÁLISIS REAL CON TU CLASE 'Secuencia'
# ==============================================================================
genes_reales = []

for reg in SeqIO.parse(archivo_fasta_real, "fasta"):
    gen_id, rol_raw = reg.id.split("|")
    genes_reales.append(
        Secuencia(id_gen=gen_id, secuencia_str=str(reg.seq), categoria=rol_raw.replace("_", " "))
    )

df_ncbi_real = (
    pd.DataFrame([g.exportar_fila() for g in genes_reales])
    .sort_values(by="Porcentaje_GC", ascending=False)
    .reset_index(drop=True)
)

print("\n--- GENES HUMANOS COMPLETOS (NCBI REFSEQ) ---")
print(df_ncbi_real.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(13, 5), dpi=150)

# Panel izquierdo (axes[0] — ya activo como referencia):
sns.scatterplot(data=df_ncbi_real, x="Longitud_pb", y="Peso_kDa", hue="Categoria", s=160, ax=axes[0])

# TODO 6: Borra el '#' de la siguiente línea para comparar tamaño proteico vs %GC:
# sns.scatterplot(data=df_ncbi_real, x="Longitud_aa", y="Porcentaje_GC", hue="Categoria", style="Categoria", s=160, ax=axes[1])

axes[0].set_title("A. Referencia: Longitud (pb) vs. Peso (kDa)", fontweight="bold", loc="left")
axes[1].set_title("B. Tu Gráfico: Aminoácidos vs. %GC", fontweight="bold", loc="left")

sns.despine(top=True, right=True)
plt.tight_layout()

ruta_fig_ncbi = Path("sesion-01-python-biologico/output/mi_grafico_ncbi.png") if Path("sesion-01-python-biologico/output").exists() else Path("mi_grafico_ncbi.png")
plt.savefig(ruta_fig_ncbi, dpi=300)
print(f"Gráfico real guardado en: {ruta_fig_ncbi}")
plt.show()