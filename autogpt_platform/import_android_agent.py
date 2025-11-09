#!/usr/bin/env python3
"""
Script para importar el agente de desarrollo Android a AutoGPT Platform.
Uso: python import_android_agent.py
"""

import json
import os
import sys
from pathlib import Path

import requests


def import_agent():
    """Importa el agente Android desde el archivo JSON."""
    
    # Configuración
    api_url = "http://localhost:8006/api/graphs"
    template_file = Path(__file__).parent / "graph_templates" / "Android_App_Developer_Agent.json"
    
    # Obtener API key desde variable de entorno
    api_key = os.getenv("AUTOGPT_API_KEY")
    if not api_key:
        print("❌ Error: No se encontró AUTOGPT_API_KEY en las variables de entorno")
        print("\n💡 Obtén tu API key desde: http://localhost:3000/profile")
        print("   Luego ejecuta: $env:AUTOGPT_API_KEY='tu-api-key-aqui'")
        sys.exit(1)
    
    # Cargar el template
    print(f"📂 Cargando template desde: {template_file}")
    try:
        with open(template_file, "r", encoding="utf-8") as f:
            agent_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {template_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error al parsear JSON: {e}")
        sys.exit(1)
    
    print(f"✅ Template cargado: {agent_data['name']}")
    print(f"   Descripción: {agent_data['description']}")
    print(f"   Nodos: {len(agent_data['nodes'])}")
    print(f"   Enlaces: {len(agent_data['links'])}")
    
    # Crear el agente via API
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print(f"\n🚀 Importando agente a {api_url}...")
    
    try:
        response = requests.post(
            api_url,
            json=agent_data,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        agent_id = result.get("id")
        
        print(f"\n✅ ¡Agente importado exitosamente!")
        print(f"   ID: {agent_id}")
        print(f"   Nombre: {result.get('name')}")
        print(f"\n🎯 Próximos pasos:")
        print(f"   1. Ve a Chat SADOCKDOG: http://localhost:3000/sadockdog")
        print(f"   2. Selecciona el agente 'Android App Developer'")
        print(f"   3. Prueba con estos datos:")
        print(f"      - app_name: CalculadoraSimple")
        print(f"      - app_description: Calculadora básica con operaciones matemáticas")
        print(f"      - features: suma, resta, multiplicación, división, interfaz Material Design")
        print(f"\n📝 También puedes editarlo en: http://localhost:3000/build?graph={agent_id}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al backend en http://localhost:8006")
        print("   Asegúrate que Docker Compose esté corriendo: docker compose ps")
    except requests.exceptions.HTTPError as e:
        print(f"❌ Error HTTP {e.response.status_code}: {e.response.text}")
        if e.response.status_code == 401:
            print("   Tu API key puede ser inválida. Obtén una nueva desde http://localhost:3000/profile")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("=" * 60)
    print("🤖 Importador de Agente Android para AutoGPT Platform")
    print("=" * 60)
    import_agent()
