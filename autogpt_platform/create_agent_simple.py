#!/usr/bin/env python3
"""
Script simple para crear el agente Android usando tu API Key.
"""

import json
import sys
from pathlib import Path

import requests


def create_agent_with_api_key():
    """Crear el agente usando una API Key."""
    
    api_url = "http://localhost:8006/api/graphs"
    template_file = Path("graph_templates/Android_App_Developer_v2.json")
    
    print("=" * 70)
    print("🤖 CREADOR DE AGENTE ANDROID APP DEVELOPER")
    print("=" * 70)
    
    # Solicitar API Key
    print("\n🔑 Necesitas tu API Key de AutoGPT:")
    print("   1. Ve a: http://localhost:3000/profile")
    print("   2. Pestaña 'API Keys'")
    print("   3. Crea una nueva API Key con permiso 'WRITE_GRAPH'")
    print("   4. Copia la key")
    
    api_key = input("\n📋 Pega tu API Key aquí: ").strip()
    
    if not api_key:
        print("❌ No se proporcionó API Key")
        sys.exit(1)
    
    # Cargar template
    print(f"\n📂 Cargando template...")
    try:
        with open(template_file, "r", encoding="utf-8") as f:
            agent_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ No se encontró {template_file}")
        sys.exit(1)
    
    print(f"✅ Template cargado: {agent_data['name']}")
    
    # Preparar datos
    api_data = {
        "name": agent_data["name"],
        "description": agent_data["description"],
        "nodes": agent_data["nodes"],
        "links": agent_data["links"],
        "is_active": True,
        "is_template": False
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print(f"\n🚀 Creando agente en el servidor...")
    
    try:
        response = requests.post(api_url, json=api_data, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        agent_id = result.get("id")
        
        print(f"\n✅ ¡AGENTE CREADO EXITOSAMENTE!")
        print(f"\n📋 DETALLES:")
        print(f"   ID: {agent_id}")
        print(f"   Nombre: {result.get('name')}")
        
        print(f"\n⚠️  IMPORTANTE - Configura GitHub OAuth:")
        print(f"   1. Ve a: http://localhost:3000/build?flowID={agent_id}")
        print(f"   2. Abre cada bloque que dice 'GitHub Create...'")
        print(f"   3. En el campo 'Credentials', selecciona tu OAuth2 de GitHub")
        print(f"   4. Guarda el agente (botón Save arriba a la derecha)")
        
        print(f"\n🎯 USAR EL AGENTE:")
        print(f"   1. Ve a: http://localhost:3000/sadockdog")
        print(f"   2. Selecciona 'Android App Developer'")
        print(f"   3. Cambia los inputs:")
        print(f"      - input-name: NombreDeTuApp")
        print(f"      - input-desc: Descripción de tu app")
        print(f"      - input-feat: características separadas por comas")
        print(f"   4. ¡Ejecuta y observa cómo crea tu app Android!")
        
        print("\n" + "=" * 70)
        print("✅ COMPLETADO")
        print("=" * 70)
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al backend")
        print("   Verifica: docker compose ps")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"❌ Error HTTP {e.response.status_code}")
        print(f"   {e.response.text}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    create_agent_with_api_key()
