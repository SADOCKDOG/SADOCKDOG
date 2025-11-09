#!/usr/bin/env python3
"""
Test Suite para SADOCKDOG Manager v2.0
Verifica que todos los componentes adicionales estén correctamente integrados.
"""

import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Prueba de importación del manager."""
    print("\n" + "="*70)
    print("  🧪 PRUEBA 1: Importación del Manager")
    print("="*70)
    
    try:
        from sadockdog_manager import SADOCKDOGManager, Colors
        print(f"  {Colors.GREEN}✅ Importación exitosa{Colors.END}")
        return True, SADOCKDOGManager, Colors
    except Exception as e:
        print(f"  ❌ Error de importación: {e}")
        return False, None, None

def test_initialization(SADOCKDOGManager):
    """Prueba de inicialización."""
    print("\n" + "="*70)
    print("  🧪 PRUEBA 2: Inicialización del Manager")
    print("="*70)
    
    try:
        manager = SADOCKDOGManager()
        print(f"  ✅ Manager inicializado correctamente")
        return True, manager
    except Exception as e:
        print(f"  ❌ Error de inicialización: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_standalone_scripts(manager, Colors):
    """Prueba de scripts autónomos."""
    print("\n" + "="*70)
    print("  🧪 PRUEBA 3: Scripts Python Autónomos")
    print("="*70)
    
    expected_count = 5
    actual_count = len(manager.standalone_scripts)
    
    print(f"  📊 Scripts esperados: {expected_count}")
    print(f"  📊 Scripts encontrados: {actual_count}")
    
    if actual_count == expected_count:
        print(f"  {Colors.GREEN}✅ Cantidad correcta de scripts{Colors.END}")
        
        print(f"\n  {Colors.BOLD}Scripts disponibles:{Colors.END}")
        for i, script in enumerate(manager.standalone_scripts, 1):
            print(f"    {i}. {script['name']:30} - {script['description']}")
            print(f"       Categoría: {script['category']}")
        
        return True
    else:
        print(f"  {Colors.RED}❌ Cantidad incorrecta de scripts{Colors.END}")
        return False

def test_autogpt_libs(manager, Colors):
    """Prueba de AutoGPT Libs."""
    print("\n" + "="*70)
    print("  🧪 PRUEBA 4: AutoGPT Libs")
    print("="*70)
    
    if hasattr(manager, 'autogpt_libs_info'):
        print(f"  {Colors.GREEN}✅ autogpt_libs_info existe{Colors.END}")
        
        print(f"\n  {Colors.BOLD}Información:{Colors.END}")
        print(f"    Descripción: {manager.autogpt_libs_info['description']}")
        print(f"    Ruta: {manager.autogpt_libs_info['path']}")
        print(f"    Nota: {manager.autogpt_libs_info['note']}")
        
        return True
    else:
        print(f"  {Colors.RED}❌ autogpt_libs_info no existe{Colors.END}")
        return False

def test_services(manager, Colors):
    """Prueba de servicios."""
    print("\n" + "="*70)
    print("  🧪 PRUEBA 5: Servicios Gestionados")
    print("="*70)
    
    expected_services = ['supabase_studio', 'meta']
    found_services = []
    
    for service in expected_services:
        if service in manager.services:
            found_services.append(service)
            service_info = manager.services[service]
            print(f"  {Colors.GREEN}✅{Colors.END} {service:20} - {service_info.get('url', 'N/A')}")
    
    if len(found_services) == len(expected_services):
        print(f"\n  {Colors.GREEN}✅ Todos los servicios esperados están presentes{Colors.END}")
        return True
    else:
        print(f"\n  {Colors.RED}❌ Faltan servicios{Colors.END}")
        return False

def test_methods(manager, Colors):
    """Prueba de métodos implementados."""
    print("\n" + "="*70)
    print("  🧪 PRUEBA 6: Métodos Implementados")
    print("="*70)
    
    expected_methods = [
        'additional_components_menu',
        'run_standalone_script',
        'show_autogpt_libs_info',
        'open_supabase_studio',
        'show_meta_service_info',
        'show_all_components_info'
    ]
    
    found_methods = []
    
    for method in expected_methods:
        if hasattr(manager, method):
            found_methods.append(method)
            print(f"  {Colors.GREEN}✅{Colors.END} {method}")
        else:
            print(f"  {Colors.RED}❌{Colors.END} {method} - NO ENCONTRADO")
    
    if len(found_methods) == len(expected_methods):
        print(f"\n  {Colors.GREEN}✅ Todos los métodos implementados{Colors.END}")
        return True
    else:
        print(f"\n  {Colors.RED}❌ Faltan métodos{Colors.END}")
        return False

def run_all_tests():
    """Ejecutar todas las pruebas."""
    print("\n╔" + "="*68 + "╗")
    print("║" + " "*20 + "SADOCKDOG MANAGER v2.0" + " "*26 + "║")
    print("║" + " "*25 + "TEST SUITE" + " "*33 + "║")
    print("╚" + "="*68 + "╝")
    
    results = []
    
    # Prueba 1: Importación
    success, SADOCKDOGManager, Colors = test_imports()
    results.append(("Importación", success))
    
    if not success:
        print(f"\n{Colors.RED}❌ PRUEBAS FALLIDAS: No se pudo importar el manager{Colors.END}")
        return False
    
    # Prueba 2: Inicialización
    success, manager = test_initialization(SADOCKDOGManager)
    results.append(("Inicialización", success))
    
    if not success:
        print(f"\n{Colors.RED}❌ PRUEBAS FALLIDAS: No se pudo inicializar el manager{Colors.END}")
        return False
    
    # Prueba 3: Scripts autónomos
    success = test_standalone_scripts(manager, Colors)
    results.append(("Scripts Autónomos", success))
    
    # Prueba 4: AutoGPT Libs
    success = test_autogpt_libs(manager, Colors)
    results.append(("AutoGPT Libs", success))
    
    # Prueba 5: Servicios
    success = test_services(manager, Colors)
    results.append(("Servicios", success))
    
    # Prueba 6: Métodos
    success = test_methods(manager, Colors)
    results.append(("Métodos", success))
    
    # Resumen
    print("\n" + "="*70)
    print("  📊 RESUMEN DE PRUEBAS")
    print("="*70 + "\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{Colors.GREEN}✅ PASS{Colors.END}" if result else f"{Colors.RED}❌ FAIL{Colors.END}"
        print(f"  {status}  {test_name}")
    
    print("\n" + "="*70)
    
    if passed == total:
        print(f"  {Colors.GREEN}{Colors.BOLD}✅ TODAS LAS PRUEBAS PASARON ({passed}/{total}){Colors.END}")
        print("="*70 + "\n")
        return True
    else:
        print(f"  {Colors.RED}{Colors.BOLD}❌ ALGUNAS PRUEBAS FALLARON ({passed}/{total}){Colors.END}")
        print("="*70 + "\n")
        return False

if __name__ == "__main__":
    try:
        # Importar Colors para uso global
        from sadockdog_manager import Colors
        
        # Ejecutar pruebas
        success = run_all_tests()
        
        # Retornar código de salida
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"\n❌ ERROR FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
