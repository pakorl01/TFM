# Script que toma el fichero "fichero_probabilidad.src.xml" como plantilla para crear en la 
# carpeta "output_probability_files" variaciones cambiando el valor de "value=100" por los definidos 

import xml.etree.ElementTree as ET
import itertools
import os

# Leer el fichero XML original
input_file = 'fichero_probabilidad.src.xml'
tree = ET.parse(input_file)
root = tree.getroot()

# Valores posibles para las variaciones del campo "value"
valores_posibles = [1, 20, 40, 60, 80, 100] 

# Encontrar todos los edges con value=100
edges_a_modificar = [edge for edge in root.findall('.//edge') if edge.get('value') == '100.00']

# Generar todas las combinaciones posibles de los valores
combinaciones = list(itertools.product(valores_posibles, repeat=len(edges_a_modificar)))

# Generar nuevas versiones del fichero
output_dir = 'output_probability_files'
os.makedirs(output_dir, exist_ok=True)

for i, combinacion in enumerate(combinaciones):
    # Crear una copia del árbol original
    tree_copy = ET.ElementTree(ET.fromstring(ET.tostring(root)))
    root_copy = tree_copy.getroot()

    # Aplicar la combinación de valores a los edges
    for edge, nuevo_valor in zip(root_copy.findall('.//edge'), combinacion):
        if edge.get('value') == '100.00':
            edge.set('value', f'{nuevo_valor:.2f}')

    # Guardar el nuevo fichero con la combinación aplicada
    output_file = os.path.join(output_dir, f'edgedata_variacion_{i}.src.xml')
    tree_copy.write(output_file)

print(f'Se han generado {len(combinaciones)} archivos en el directorio "{output_dir}".')
