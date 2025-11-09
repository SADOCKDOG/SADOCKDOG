#!/usr/bin/env python3
"""
Project Sync - Sincronizador de cambios del proyecto principal
Detecta y permite incorporar cambios relevantes del proyecto principal al manager.
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Optional


class ProjectSync:
    """Sincronizador de cambios del proyecto principal."""
    
    def __init__(self):
        self.run_dir = Path(__file__).parent
        self.project_root = self.run_dir.parent
        self.sync_state_file = self.run_dir / "logs" / "sync_state.json"
        self.change_log = self.run_dir / "logs" / "project_changes.log"
        
        # Archivos del proyecto principal a monitorear
        self.monitored_files = [
            "README.md",
            "ARCHITECTURE.md",
            "DEPLOYMENT.md",
            "TESTING.md",
            "SECURITY.md",
            "CONTRIBUTING.md",
            "autogpt_platform/README.md",
            "autogpt_platform/docker-compose.yml",
            "autogpt_platform/frontend/package.json",
            "autogpt_platform/backend/pyproject.toml",
            ".github/workflows/*.yml",
        ]
        
        # Patrones de cambios relevantes para el manager
        self.relevant_patterns = {
            "services": ["docker", "service", "port", "container", "compose"],
            "dependencies": ["version", "requirement", "package", "install"],
            "config": ["environment", "env", "configuration", "settings"],
            "security": ["security", "auth", "credentials", "password", "token"],
            "infrastructure": ["database", "redis", "rabbitmq", "postgres", "supabase"],
            "api": ["endpoint", "api", "route", "url", "http"],
        }
        
        self.sync_state_file.parent.mkdir(exist_ok=True)
        self.change_log.parent.mkdir(exist_ok=True)
    
    def get_file_hash(self, file_path: Path) -> str:
        """Calcula hash SHA256 de un archivo."""
        if not file_path.exists():
            return ""
        
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def load_sync_state(self) -> Dict:
        """Carga el estado previo de sincronización."""
        if not self.sync_state_file.exists():
            return {}
        
        try:
            with open(self.sync_state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def save_sync_state(self, state: Dict):
        """Guarda el estado de sincronización."""
        with open(self.sync_state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
    
    def get_monitored_files(self) -> List[Path]:
        """Obtiene lista de archivos monitoreados que existen."""
        files = []
        
        for pattern in self.monitored_files:
            if '*' in pattern:
                # Patrón con wildcard
                base_dir = self.project_root / pattern.split('*')[0]
                if base_dir.exists():
                    files.extend(base_dir.glob('*' + pattern.split('*')[1]))
            else:
                file_path = self.project_root / pattern
                if file_path.exists():
                    files.append(file_path)
        
        return files
    
    def detect_changes(self) -> Dict[str, Dict]:
        """Detecta cambios en archivos monitoreados."""
        current_state = self.load_sync_state()
        changes = {}
        
        for file_path in self.get_monitored_files():
            current_hash = self.get_file_hash(file_path)
            relative_path = str(file_path.relative_to(self.project_root))
            
            stored_hash = current_state.get(relative_path, {}).get('hash', '')
            
            if current_hash != stored_hash:
                changes[relative_path] = {
                    'path': str(file_path),
                    'old_hash': stored_hash,
                    'new_hash': current_hash,
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    'size': file_path.stat().st_size,
                    'new_file': stored_hash == ''
                }
        
        return changes
    
    def analyze_changes(self, changes: Dict[str, Dict]) -> Dict[str, List]:
        """Analiza cambios y los categoriza por relevancia."""
        categorized = {
            "critical": [],      # Cambios críticos (seguridad, infraestructura)
            "important": [],     # Cambios importantes (servicios, dependencias)
            "relevant": [],      # Cambios relevantes (config, APIs)
            "informational": []  # Cambios informativos (docs)
        }
        
        for file_path, change_info in changes.items():
            file_content = ""
            try:
                with open(change_info['path'], 'r', encoding='utf-8') as f:
                    file_content = f.read().lower()
            except Exception:
                pass
            
            # Analizar contenido para categorizar
            priority = "informational"
            matched_patterns = []
            
            for category, patterns in self.relevant_patterns.items():
                if any(pattern in file_content for pattern in patterns):
                    matched_patterns.append(category)
            
            # Determinar prioridad
            if "security" in matched_patterns or "credentials" in file_content:
                priority = "critical"
            elif "infrastructure" in matched_patterns or "services" in matched_patterns:
                priority = "important"
            elif "dependencies" in matched_patterns or "config" in matched_patterns or "api" in matched_patterns:
                priority = "relevant"
            
            change_info['matched_patterns'] = matched_patterns
            categorized[priority].append({
                'file': file_path,
                'info': change_info
            })
        
        return categorized
    
    def get_change_diff(self, file_path: str, lines_context: int = 5) -> List[str]:
        """Obtiene un resumen de los cambios en un archivo."""
        # Simplificado: obtener últimas líneas modificadas
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return lines[-lines_context:] if len(lines) > lines_context else lines
        except Exception:
            return []
    
    def mark_as_synced(self, files: List[str] = None):
        """Marca archivos como sincronizados."""
        current_state = self.load_sync_state()
        
        files_to_sync = files if files else [
            str(f.relative_to(self.project_root)) for f in self.get_monitored_files()
        ]
        
        for file_path in files_to_sync:
            full_path = self.project_root / file_path
            if full_path.exists():
                current_state[file_path] = {
                    'hash': self.get_file_hash(full_path),
                    'last_sync': datetime.now().isoformat()
                }
        
        self.save_sync_state(current_state)
        
        # Registrar en log
        with open(self.change_log, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"Sincronización: {datetime.now().isoformat()}\n")
            f.write(f"Archivos: {len(files_to_sync)}\n")
            f.write(f"{'='*80}\n")
    
    def get_change_summary(self) -> str:
        """Genera resumen de cambios pendientes."""
        changes = self.detect_changes()
        
        if not changes:
            return "✅ No hay cambios pendientes en el proyecto principal."
        
        categorized = self.analyze_changes(changes)
        
        summary = []
        summary.append(f"\n📊 RESUMEN DE CAMBIOS DETECTADOS")
        summary.append(f"{'='*80}")
        summary.append(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Critical
        if categorized['critical']:
            summary.append(f"🔴 CAMBIOS CRÍTICOS ({len(categorized['critical'])})")
            for change in categorized['critical']:
                summary.append(f"  • {change['file']}")
                summary.append(f"    Patrones: {', '.join(change['info']['matched_patterns'])}")
        
        # Important
        if categorized['important']:
            summary.append(f"\n🟡 CAMBIOS IMPORTANTES ({len(categorized['important'])})")
            for change in categorized['important']:
                summary.append(f"  • {change['file']}")
                summary.append(f"    Patrones: {', '.join(change['info']['matched_patterns'])}")
        
        # Relevant
        if categorized['relevant']:
            summary.append(f"\n🟢 CAMBIOS RELEVANTES ({len(categorized['relevant'])})")
            for change in categorized['relevant']:
                summary.append(f"  • {change['file']}")
        
        # Informational
        if categorized['informational']:
            summary.append(f"\n🔵 CAMBIOS INFORMATIVOS ({len(categorized['informational'])})")
            for change in categorized['informational']:
                summary.append(f"  • {change['file']}")
        
        summary.append(f"\n{'='*80}")
        summary.append(f"Total de archivos modificados: {len(changes)}")
        
        return '\n'.join(summary)
    
    def extract_service_changes(self, changes: Dict[str, Dict]) -> List[Dict]:
        """Extrae cambios relacionados con servicios para actualizar el manager."""
        service_changes = []
        
        # Buscar en docker-compose.yml
        docker_compose = self.project_root / "autogpt_platform" / "docker-compose.yml"
        if docker_compose.exists():
            try:
                with open(docker_compose, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Detectar nuevos servicios o puertos
                    # (Implementación simplificada - se puede mejorar con parser YAML)
                    if "ports:" in content:
                        service_changes.append({
                            'type': 'service_update',
                            'file': 'docker-compose.yml',
                            'description': 'Cambios en configuración de servicios Docker'
                        })
            except Exception:
                pass
        
        return service_changes
    
    def generate_sync_report(self, output_file: Optional[str] = None) -> str:
        """Genera reporte detallado de sincronización."""
        changes = self.detect_changes()
        categorized = self.analyze_changes(changes)
        
        report = []
        report.append("# REPORTE DE SINCRONIZACIÓN - PROYECTO PRINCIPAL")
        report.append(f"\nGenerado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"\n{'='*80}\n")
        
        # Estadísticas
        report.append("## 📊 ESTADÍSTICAS")
        report.append(f"- Total archivos monitoreados: {len(self.get_monitored_files())}")
        report.append(f"- Archivos con cambios: {len(changes)}")
        report.append(f"- Cambios críticos: {len(categorized['critical'])}")
        report.append(f"- Cambios importantes: {len(categorized['important'])}")
        report.append(f"- Cambios relevantes: {len(categorized['relevant'])}")
        report.append(f"- Cambios informativos: {len(categorized['informational'])}")
        
        # Detalle de cambios
        if changes:
            report.append(f"\n## 📝 DETALLE DE CAMBIOS\n")
            
            for priority in ['critical', 'important', 'relevant', 'informational']:
                if categorized[priority]:
                    report.append(f"\n### {priority.upper()}\n")
                    for change in categorized[priority]:
                        report.append(f"**{change['file']}**")
                        report.append(f"- Modificado: {change['info']['modified']}")
                        report.append(f"- Tamaño: {change['info']['size']} bytes")
                        if change['info']['matched_patterns']:
                            report.append(f"- Categorías: {', '.join(change['info']['matched_patterns'])}")
                        report.append("")
        
        # Recomendaciones
        report.append("\n## 💡 RECOMENDACIONES\n")
        if categorized['critical']:
            report.append("⚠️  **ACCIÓN INMEDIATA REQUERIDA**: Hay cambios críticos de seguridad o infraestructura")
        if categorized['important']:
            report.append("⚡ **REVISAR PRONTO**: Hay cambios importantes en servicios o dependencias")
        if not changes:
            report.append("✅ Sistema sincronizado - No se requieren acciones")
        
        report_content = '\n'.join(report)
        
        # Guardar reporte si se especifica archivo
        if output_file:
            output_path = self.run_dir / "logs" / output_file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
        
        return report_content


if __name__ == "__main__":
    """Ejecución standalone para pruebas."""
    syncer = ProjectSync()
    print(syncer.get_change_summary())
