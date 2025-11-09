#!/usr/bin/env python3
"""
Platform Discovery - Detección automática de componentes de AutoGPT Platform
Escanea y registra todos los componentes, servicios y configuraciones.
"""

import os
import json
import yaml
import re
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime


class PlatformDiscovery:
    """Descubridor automático de componentes de la plataforma."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.platform_dir = self.project_root / "autogpt_platform"
        self.run_dir = Path(__file__).parent
        self.discovery_cache = self.run_dir / "logs" / "platform_components.json"
        self.discovery_cache.parent.mkdir(exist_ok=True)
        
        self.components = {
            "services": {},
            "libraries": {},
            "scripts": {},
            "configs": {},
            "databases": {},
            "frontend_routes": [],
            "backend_routes": [],
            "dependencies": {},
            "environment_vars": set(),
        }
    
    def discover_all(self) -> Dict:
        """Ejecuta descubrimiento completo de la plataforma."""
        print("🔍 Iniciando descubrimiento de componentes...")
        
        self.discover_docker_services()
        self.discover_libraries()
        self.discover_python_scripts()
        self.discover_configs()
        self.discover_databases()
        self.discover_frontend_routes()
        self.discover_backend_routes()
        self.discover_dependencies()
        self.discover_environment_vars()
        
        self.save_discovery()
        
        return self.components
    
    def discover_docker_services(self):
        """Descubre servicios de Docker Compose."""
        compose_files = [
            self.platform_dir / "docker-compose.yml",
            self.platform_dir / "docker-compose.platform.yml",
            self.project_root / "db" / "docker" / "docker-compose.yml"
        ]
        
        for compose_file in compose_files:
            if not compose_file.exists():
                continue
            
            try:
                with open(compose_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                
                services = config.get('services', {})
                for service_name, service_config in services.items():
                    ports = []
                    if 'ports' in service_config:
                        for port in service_config['ports']:
                            if isinstance(port, str):
                                ports.append(port.split(':')[0])
                            elif isinstance(port, int):
                                ports.append(str(port))
                    
                    self.components['services'][service_name] = {
                        'file': str(compose_file.relative_to(self.project_root)),
                        'image': service_config.get('image', ''),
                        'build': service_config.get('build', ''),
                        'ports': ports,
                        'environment': service_config.get('environment', {}),
                        'volumes': service_config.get('volumes', []),
                        'depends_on': service_config.get('depends_on', []),
                        'profiles': service_config.get('profiles', []),
                        'healthcheck': 'healthcheck' in service_config
                    }
            except Exception as e:
                print(f"⚠️  Error procesando {compose_file}: {e}")
    
    def discover_libraries(self):
        """Descubre librerías en autogpt_libs."""
        libs_dir = self.platform_dir / "autogpt_libs"
        if not libs_dir.exists():
            return
        
        for lib_path in libs_dir.iterdir():
            if lib_path.is_dir() and not lib_path.name.startswith('.'):
                pyproject = lib_path / "pyproject.toml"
                readme = lib_path / "README.md"
                
                self.components['libraries'][lib_path.name] = {
                    'path': str(lib_path.relative_to(self.project_root)),
                    'has_pyproject': pyproject.exists(),
                    'has_readme': readme.exists(),
                    'description': self._extract_description(readme) if readme.exists() else ""
                }
    
    def discover_python_scripts(self):
        """Descubre scripts Python no gestionados."""
        script_files = []
        
        # Buscar en directorio principal de platform
        for py_file in self.platform_dir.glob("*.py"):
            if py_file.is_file():
                script_files.append(py_file)
        
        # Buscar en cli
        cli_dir = self.platform_dir / "cli"
        if cli_dir.exists():
            for py_file in cli_dir.rglob("*.py"):
                script_files.append(py_file)
        
        for script in script_files:
            with open(script, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Detectar si es ejecutable
            is_executable = content.startswith('#!') or '__main__' in content
            
            self.components['scripts'][script.name] = {
                'path': str(script.relative_to(self.project_root)),
                'executable': is_executable,
                'description': self._extract_docstring(content)
            }
    
    def discover_configs(self):
        """Descubre archivos de configuración."""
        config_patterns = ['*.yml', '*.yaml', '*.json', '*.toml', '.env*']
        
        for pattern in config_patterns:
            for config_file in self.platform_dir.rglob(pattern):
                if config_file.is_file() and 'node_modules' not in str(config_file):
                    self.components['configs'][config_file.name] = {
                        'path': str(config_file.relative_to(self.project_root)),
                        'type': config_file.suffix,
                        'size': config_file.stat().st_size
                    }
    
    def discover_databases(self):
        """Descubre configuraciones de bases de datos."""
        # PostgreSQL
        if self.components['services'].get('supabase-db') or self.components['services'].get('db'):
            self.components['databases']['postgresql'] = {
                'type': 'PostgreSQL',
                'default_port': 5432,
                'service': 'supabase-db',
                'management_ui': None
            }
        
        # Redis
        if self.components['services'].get('redis'):
            self.components['databases']['redis'] = {
                'type': 'Redis',
                'default_port': 6379,
                'service': 'redis',
                'management_ui': None
            }
        
        # Supabase Studio
        if self.components['services'].get('supabase-studio'):
            if 'postgresql' in self.components['databases']:
                self.components['databases']['postgresql']['management_ui'] = {
                    'name': 'Supabase Studio',
                    'port': 54323,
                    'url': 'http://localhost:54323'
                }
    
    def discover_frontend_routes(self):
        """Descubre rutas del frontend Next.js."""
        frontend_dir = self.platform_dir / "frontend" / "src" / "app"
        if not frontend_dir.exists():
            return
        
        routes = []
        for route_dir in frontend_dir.rglob("page.tsx"):
            route_path = route_dir.parent.relative_to(frontend_dir)
            route_str = '/' + str(route_path).replace('\\', '/').replace('(', '').replace(')', '')
            if route_str != '/.':
                routes.append(route_str)
        
        self.components['frontend_routes'] = sorted(routes)
    
    def discover_backend_routes(self):
        """Descubre rutas del backend FastAPI."""
        backend_dir = self.platform_dir / "backend"
        if not backend_dir.exists():
            return
        
        routes = []
        for py_file in backend_dir.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Buscar decoradores de FastAPI
                route_matches = re.findall(r'@\w+\.(get|post|put|delete|patch)\(["\']([^"\']+)', content)
                for method, path in route_matches:
                    routes.append({
                        'method': method.upper(),
                        'path': path,
                        'file': str(py_file.relative_to(self.project_root))
                    })
            except Exception:
                pass
        
        self.components['backend_routes'] = routes
    
    def discover_dependencies(self):
        """Descubre dependencias de Python y Node.js."""
        # Python - pyproject.toml
        pyproject_files = list(self.platform_dir.rglob("pyproject.toml"))
        for pyproject in pyproject_files:
            try:
                with open(pyproject, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Simplificado - en producción usar toml parser
                    self.components['dependencies'][str(pyproject.relative_to(self.project_root))] = {
                        'type': 'python',
                        'manager': 'poetry'
                    }
            except Exception:
                pass
        
        # Node.js - package.json
        package_files = list(self.platform_dir.rglob("package.json"))
        for package in package_files:
            if 'node_modules' in str(package):
                continue
            
            try:
                with open(package, 'r', encoding='utf-8') as f:
                    pkg_data = json.load(f)
                    self.components['dependencies'][str(package.relative_to(self.project_root))] = {
                        'type': 'nodejs',
                        'manager': 'npm' if (package.parent / 'package-lock.json').exists() else 'pnpm',
                        'name': pkg_data.get('name', ''),
                        'version': pkg_data.get('version', '')
                    }
            except Exception:
                pass
    
    def discover_environment_vars(self):
        """Descubre variables de entorno utilizadas."""
        env_vars = set()
        
        # Buscar en archivos .env
        for env_file in self.platform_dir.rglob(".env*"):
            if env_file.is_file():
                try:
                    with open(env_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#') and '=' in line:
                                var_name = line.split('=')[0].strip()
                                env_vars.add(var_name)
                except Exception:
                    pass
        
        # Buscar en archivos Python
        for py_file in self.platform_dir.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Buscar os.environ, os.getenv, etc.
                    matches = re.findall(r'os\.(?:environ|getenv)\[["\']([^"\']+)', content)
                    env_vars.update(matches)
                    matches = re.findall(r'os\.getenv\(["\']([^"\']+)', content)
                    env_vars.update(matches)
            except Exception:
                pass
        
        self.components['environment_vars'] = sorted(list(env_vars))
    
    def _extract_description(self, readme_path: Path) -> str:
        """Extrae descripción de un README."""
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # Tomar primera línea que no sea título
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        return line[:200]
        except Exception:
            pass
        return ""
    
    def _extract_docstring(self, content: str) -> str:
        """Extrae docstring de contenido Python."""
        match = re.search(r'"""([^"]+)"""', content)
        if match:
            return match.group(1).strip()[:200]
        return ""
    
    def save_discovery(self):
        """Guarda resultados del descubrimiento."""
        # Convertir set a list para JSON
        components_json = dict(self.components)
        components_json['environment_vars'] = list(components_json['environment_vars'])
        components_json['discovery_timestamp'] = datetime.now().isoformat()
        
        with open(self.discovery_cache, 'w', encoding='utf-8') as f:
            json.dump(components_json, f, indent=2)
    
    def load_discovery(self) -> Optional[Dict]:
        """Carga descubrimiento previo."""
        if not self.discovery_cache.exists():
            return None
        
        try:
            with open(self.discovery_cache, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None
    
    def generate_report(self) -> str:
        """Genera reporte de descubrimiento."""
        report = []
        report.append("# REPORTE DE DESCUBRIMIENTO - AUTOGPT PLATFORM")
        report.append(f"\nGenerado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"\n{'='*80}\n")
        
        # Servicios
        report.append(f"## 🐳 SERVICIOS DOCKER ({len(self.components['services'])})")
        for name, info in sorted(self.components['services'].items()):
            report.append(f"\n### {name}")
            if info['ports']:
                report.append(f"- Puertos: {', '.join(info['ports'])}")
            if info['image']:
                report.append(f"- Imagen: {info['image']}")
            if info['profiles']:
                report.append(f"- Profiles: {', '.join(info['profiles'])}")
        
        # Librerías
        if self.components['libraries']:
            report.append(f"\n## 📚 LIBRERÍAS ({len(self.components['libraries'])})")
            for name, info in sorted(self.components['libraries'].items()):
                report.append(f"- **{name}**: {info['description'][:100] if info['description'] else 'Sin descripción'}")
        
        # Scripts
        if self.components['scripts']:
            report.append(f"\n## 📜 SCRIPTS PYTHON ({len(self.components['scripts'])})")
            executables = [name for name, info in self.components['scripts'].items() if info['executable']]
            report.append(f"- Ejecutables: {len(executables)}")
            for name in executables:
                report.append(f"  - {name}")
        
        # Bases de datos
        if self.components['databases']:
            report.append(f"\n## 💾 BASES DE DATOS ({len(self.components['databases'])})")
            for name, info in self.components['databases'].items():
                report.append(f"- **{info['type']}**: Puerto {info['default_port']}")
                if info['management_ui']:
                    report.append(f"  - UI: {info['management_ui']['url']}")
        
        # Rutas Frontend
        if self.components['frontend_routes']:
            report.append(f"\n## 🎨 RUTAS FRONTEND ({len(self.components['frontend_routes'])})")
            for route in self.components['frontend_routes'][:10]:
                report.append(f"- {route}")
            if len(self.components['frontend_routes']) > 10:
                report.append(f"- ... y {len(self.components['frontend_routes']) - 10} más")
        
        # Rutas Backend
        if self.components['backend_routes']:
            report.append(f"\n## ⚙️ RUTAS BACKEND ({len(self.components['backend_routes'])})")
            for route in self.components['backend_routes'][:10]:
                report.append(f"- {route['method']} {route['path']}")
            if len(self.components['backend_routes']) > 10:
                report.append(f"- ... y {len(self.components['backend_routes']) - 10} más")
        
        # Variables de entorno
        if self.components['environment_vars']:
            report.append(f"\n## 🔐 VARIABLES DE ENTORNO ({len(self.components['environment_vars'])})")
            report.append("(Primeras 20)")
            for var in self.components['environment_vars'][:20]:
                report.append(f"- {var}")
        
        return '\n'.join(report)


if __name__ == "__main__":
    """Ejecución standalone."""
    discovery = PlatformDiscovery()
    discovery.discover_all()
    print(discovery.generate_report())
    print(f"\n✅ Resultados guardados en: {discovery.discovery_cache}")
