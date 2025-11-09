#!/usr/bin/env python3
"""
Script para crear automáticamente el agente Android App Developer
usando un access token obtenido del navegador.
"""

import json
import sys
from pathlib import Path

import requests


def get_token_from_input() -> str:
    """Obtener token desde input del usuario."""
    print("\n📋 NECESITAS TU ACCESS TOKEN:")
    print("   1. Abre las DevTools del navegador (F12)")
    print("   2. Ve a la pestaña 'Application' o 'Almacenamiento'")
    print("   3. En 'Local Storage' → 'http://localhost:3000'")
    print("   4. Busca la clave que contiene 'access_token' o similar")
    print("   5. Copia el valor del token\n")
    
    token = input("🔑 Pega tu access token aquí: ").strip()
    
    if not token:
        print("❌ No se proporcionó token")
        sys.exit(1)
    
    return token


def get_github_credentials(access_token: str) -> str:
    """Obtener el ID de las credenciales OAuth de GitHub."""
    
    creds_url = "http://localhost:8006/api/credentials"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    print("🔍 Buscando credenciales de GitHub...")
    
    try:
        response = requests.get(creds_url, headers=headers, timeout=10)
        response.raise_for_status()
        credentials = response.json()
        
        # Buscar credenciales de GitHub OAuth2
        github_creds = [
            cred for cred in credentials 
            if cred.get("provider") == "github" and cred.get("type") == "oauth2"
        ]
        
        if not github_creds:
            print("⚠️  No se encontraron credenciales OAuth de GitHub")
            print("   Deberás configurarlas manualmente después de importar el agente")
            return None
        
        cred_id = github_creds[0]["id"]
        print(f"✅ Credencial GitHub encontrada: {cred_id}")
        return cred_id
        
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Error al obtener credenciales: {e}")
        print("   Continuando sin credenciales (configurar manualmente después)")
        return None


def create_agent(access_token: str, github_cred_id: str = None):
    """Crear el agente Android App Developer."""
    
    api_url = "http://localhost:8006/api/graphs"
    template_file = Path(__file__).parent / "graph_templates" / "Android_App_Developer_v2.json"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    print(f"\n📂 Cargando template desde: {template_file}")
    
    try:
        with open(template_file, "r", encoding="utf-8") as f:
            agent_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró {template_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error al parsear JSON: {e}")
        sys.exit(1)
    
    # Si tenemos credenciales, configurarlas en los bloques de GitHub
    if github_cred_id:
        print(f"🔧 Configurando credenciales OAuth en bloques de GitHub...")
        github_blocks = [
            "create-repo", "file-gradle", "file-manifest", 
            "file-kotlin", "file-layout", "file-readme"
        ]
        
        for node in agent_data["nodes"]:
            if node["id"] in github_blocks:
                if "input_default" not in node:
                    node["input_default"] = {}
                node["input_default"]["credentials"] = {
                    "id": github_cred_id,
                    "type": "oauth2",
                    "provider": "github"
                }
                print(f"   ✓ Configurado: {node['id']}")
    
    print(f"\n🚀 Creando agente: {agent_data['name']}")
    print(f"   Descripción: {agent_data['description']}")
    print(f"   Nodos: {len(agent_data['nodes'])}")
    print(f"   Enlaces: {len(agent_data['links'])}")
    
    # Preparar datos para la API (remover campos de template)
    api_data = {
        "name": agent_data["name"],
        "description": agent_data["description"],
        "nodes": agent_data["nodes"],
        "links": agent_data["links"],
        "is_active": True,
        "is_template": False
    }
    
    try:
        response = requests.post(api_url, json=api_data, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        agent_id = result.get("id")
        
        print(f"\n✅ ¡Agente creado exitosamente!")
        print(f"\n📋 DETALLES:")
        print(f"   ID: {agent_id}")
        print(f"   Nombre: {result.get('name')}")
        print(f"   Versión: {result.get('version', 1)}")
        
        if github_cred_id:
            print(f"\n✅ Credenciales OAuth configuradas automáticamente")
        else:
            print(f"\n⚠️  IMPORTANTE: Configura las credenciales OAuth manualmente:")
            print(f"   1. Ve a: http://localhost:3000/build?flowID={agent_id}")
            print(f"   2. Abre cada bloque 'GitHub Create...'")
            print(f"   3. Selecciona tus credenciales OAuth en el campo 'Credentials'")
            print(f"   4. Guarda el agente")
        
        print(f"\n🎯 PRÓXIMOS PASOS:")
        print(f"   1. Ve a Chat SADOCKDOG: http://localhost:3000/sadockdog")
        print(f"   2. Selecciona 'Android App Developer'")
        print(f"   3. Cambia los valores de input:")
        print(f"      - input-name: MiAppAndroid")
        print(f"      - input-desc: Descripción de tu app")
        print(f"      - input-feat: características separadas por comas")
        print(f"   4. Ejecuta y observa la creación del repo GitHub!")
        
        print(f"\n📝 También puedes editarlo en:")
        print(f"   http://localhost:3000/build?flowID={agent_id}")
        
        return agent_id
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al backend en http://localhost:8006")
        print("   Verifica que Docker Compose esté corriendo: docker compose ps")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"❌ Error HTTP {e.response.status_code}")
        print(f"   Respuesta: {e.response.text}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)


def main():
    """Función principal."""
    print("=" * 70)
    print("🤖 CREADOR AUTOMÁTICO DE AGENTE ANDROID APP DEVELOPER")
    print("=" * 70)
    
    # Paso 1: Obtener token del usuario
    access_token = get_token_from_input()
    
    # Paso 2: Obtener credenciales GitHub (opcional)
    github_cred_id = get_github_credentials(access_token)
    
    # Paso 3: Crear el agente
    agent_id = create_agent(access_token, github_cred_id)
    
    print("\n" + "=" * 70)
    print("✅ PROCESO COMPLETADO")
    print("=" * 70)


if __name__ == "__main__":
    main()
