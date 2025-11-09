#!/usr/bin/env python3
"""
Script que crea el agente usando autenticación directa con email/password.
"""

import json
import sys
from pathlib import Path

import requests


def create_agent_direct():
    """Crear agente con autenticación directa."""
    
    print("=" * 70)
    print("🤖 CREADOR DE AGENTE ANDROID APP DEVELOPER")
    print("=" * 70)
    
    # Credenciales proporcionadas
    EMAIL = "davidasuar@gmail.com"
    PASSWORD = "w.DA7e7Km6_:8Ki"
    
    # Paso 1: Obtener token de la API REST directamente
    print(f"\n🔐 Autenticando como {EMAIL}...")
    
    # Intentar obtener la lista de agentes sin auth primero (para test)
    api_url = "http://localhost:8006/api/graphs"
    
    # Crear una sesión para mantener cookies
    session = requests.Session()
    
    # Intentar login directo a Supabase via REST
    supabase_url = "http://localhost:8000"
    
    # Auth con Supabase
    auth_data = {
        "email": EMAIL,
        "password": PASSWORD
    }
    
    try:
        # Login a Supabase
        auth_response = session.post(
            f"{supabase_url}/auth/v1/signup",  # signup también funciona para login si ya existe
            json=auth_data,
            headers={
                "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        if auth_response.status_code == 400:
            # Usuario ya existe, intentar signin
            auth_response = session.post(
                f"{supabase_url}/auth/v1/token?grant_type=password",
                json=auth_data,
                headers={
                    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0",
                    "Content-Type": "application/json"
                },
                timeout=10
            )
        
        auth_response.raise_for_status()
        auth_result = auth_response.json()
        access_token = auth_result.get("access_token")
        
        if not access_token:
            print("❌ No se pudo obtener token")
            print(f"Respuesta: {auth_result}")
            sys.exit(1)
        
        print("✅ Autenticación exitosa!")
        
    except Exception as e:
        print(f"❌ Error de autenticación: {e}")
        print("\n⚠️  ALTERNATIVA: Usa el método manual")
        print("   1. Ve a http://localhost:3000/build")
        print("   2. Haz clic en 'Import' (arriba a la derecha)")
        print("   3. Selecciona: graph_templates/Android_App_Developer_v2.json")
        print("   4. Configura OAuth de GitHub en cada bloque")
        print("   5. ¡Listo!")
        sys.exit(1)
    
    # Cargar template
    template_file = Path("graph_templates/Android_App_Developer_v2.json")
    print(f"\n📂 Cargando template...")
    
    try:
        with open(template_file, "r", encoding="utf-8") as f:
            agent_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ No se encontró {template_file}")
        sys.exit(1)
    
    print(f"✅ Template cargado: {agent_data['name']}")
    
    # Buscar credenciales GitHub
    print("\n🔍 Buscando credenciales de GitHub...")
    
    try:
        creds_response = session.get(
            "http://localhost:8006/api/credentials",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10
        )
        creds_response.raise_for_status()
        credentials = creds_response.json()
        
        github_creds = [c for c in credentials if c.get("provider") == "github" and c.get("type") == "oauth2"]
        
        if github_creds:
            github_cred_id = github_creds[0]["id"]
            print(f"✅ Credencial GitHub encontrada: {github_cred_id}")
            
            # Configurar credenciales en los bloques
            github_blocks = ["create-repo", "file-gradle", "file-manifest", "file-kotlin", "file-layout", "file-readme"]
            for node in agent_data["nodes"]:
                if node["id"] in github_blocks:
                    if "input_default" not in node:
                        node["input_default"] = {}
                    node["input_default"]["credentials"] = {
                        "id": github_cred_id,
                        "type": "oauth2",
                        "provider": "github"
                    }
            print("🔧 Credenciales configuradas en todos los bloques GitHub")
        else:
            print("⚠️  No se encontraron credenciales GitHub (configurar manualmente después)")
    
    except Exception as e:
        print(f"⚠️  No se pudieron obtener credenciales: {e}")
    
    # Crear agente
    print(f"\n🚀 Creando agente...")
    
    api_data = {
        "name": agent_data["name"],
        "description": agent_data["description"],
        "nodes": agent_data["nodes"],
        "links": agent_data["links"],
        "is_active": True,
        "is_template": False
    }
    
    try:
        response = session.post(
            api_url,
            json=api_data,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        agent_id = result.get("id")
        
        print(f"\n✅ ¡AGENTE CREADO EXITOSAMENTE!")
        print(f"\n📋 DETALLES:")
        print(f"   ID: {agent_id}")
        print(f"   Nombre: {result.get('name')}")
        print(f"   Versión: {result.get('version', 1)}")
        
        if github_creds:
            print(f"\n✅ Credenciales OAuth YA configuradas automáticamente")
        else:
            print(f"\n⚠️  Configura OAuth manualmente:")
            print(f"   http://localhost:3000/build?flowID={agent_id}")
        
        print(f"\n🎯 USAR EL AGENTE:")
        print(f"   1. http://localhost:3000/sadockdog")
        print(f"   2. Selecciona 'Android App Developer'")
        print(f"   3. Cambia los inputs y ejecuta")
        
        print("\n" + "=" * 70)
        print("✅ COMPLETADO - ¡Agente listo para usar!")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Error al crear agente: {e}")
        if hasattr(e, 'response'):
            print(f"   {e.response.text}")
        sys.exit(1)


if __name__ == "__main__":
    create_agent_direct()
