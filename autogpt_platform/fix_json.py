import json
import uuid

# Leer el archivo
with open('graph_templates/Android_App_Developer_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Añadir IDs a todos los links
for link in data['links']:
    link['id'] = str(uuid.uuid4())

# Guardar el archivo arreglado
with open('graph_templates/Android_App_Developer_v2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Archivo arreglado exitosamente!")
print(f"   Links procesados: {len(data['links'])}")
print(f"   Nodos: {len(data['nodes'])}")
