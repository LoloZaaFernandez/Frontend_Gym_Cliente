"""
Script de pruebas de integración Frontend-Backend
Valida todos los endpoints y la conexión completa del sistema
"""

import requests
import json
from datetime import datetime

API_BASE_URL = "http://localhost:8000"

def print_test(name, success, details=""):
    """Imprimir resultado de prueba"""
    status = "[OK]" if success else "[FAIL]"
    print(f"{status} {name}")
    if details:
        print(f"    {details}")
    print()

def test_health():
    """Probar endpoint de salud"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        success = response.status_code == 200 and response.json().get("status") == "healthy"
        print_test("Health Check", success, f"Status: {response.status_code}")
        return success
    except Exception as e:
        print_test("Health Check", False, f"Error: {str(e)}")
        return False

def test_admin_login():
    """Probar login de administrador"""
    try:
        data = {"username": "admin", "password": "admin123"}
        response = requests.post(f"{API_BASE_URL}/api/auth/login-admin", json=data, timeout=5)
        success = response.status_code == 200 and response.json().get("success")
        user = response.json().get("user", {}) if success else {}
        print_test("Admin Login", success, f"Usuario: {user.get('nombre', 'N/A')}")
        return success
    except Exception as e:
        print_test("Admin Login", False, f"Error: {str(e)}")
        return False

def test_client_login():
    """Probar login de cliente"""
    try:
        response = requests.post(f"{API_BASE_URL}/api/auth/login-client?dni=12345678", timeout=5)
        success = response.status_code == 200 and response.json().get("success")
        user = response.json().get("user", {}) if success else {}
        print_test("Client Login", success, f"Cliente: {user.get('nombre', 'N/A')}")
        return success
    except Exception as e:
        print_test("Client Login", False, f"Error: {str(e)}")
        return False

def test_list_clients():
    """Probar listado de clientes"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/clientes", timeout=5)
        success = response.status_code == 200
        clients = response.json() if success else []
        print_test("List Clients", success, f"Clientes encontrados: {len(clients)}")
        return success
    except Exception as e:
        print_test("List Clients", False, f"Error: {str(e)}")
        return False

def test_get_client_by_dni():
    """Probar obtener cliente por DNI (mediante listado)"""
    try:
        # El backend no tiene endpoint /dni/{dni}, usamos el listado y filtramos
        response = requests.get(f"{API_BASE_URL}/api/clientes", timeout=5)
        success = response.status_code == 200
        if success:
            clients = response.json()
            client = next((c for c in clients if c.get('dni') == '72788702'), None)
            success = client is not None
            print_test("Get Client by DNI", success, f"Cliente: {client.get('nombre', 'N/A') if client else 'N/A'}")
        else:
            print_test("Get Client by DNI", False, "No se pudo obtener listado")
        return success
    except Exception as e:
        print_test("Get Client by DNI", False, f"Error: {str(e)}")
        return False

def test_create_client():
    """Probar creación de cliente"""
    try:
        test_dni = f"TEST{datetime.now().strftime('%H%M%S')}"
        data = {
            "dni": test_dni,
            "nombre": "Cliente",
            "apellidos": "Prueba Integracion",
            "correo": f"test{test_dni}@test.com",
            "telefono": "999999999",
            "usuario_creacion": "admin"
        }
        response = requests.post(f"{API_BASE_URL}/api/clientes", json=data, timeout=5)
        success = response.status_code == 200 or response.status_code == 201
        print_test("Create Client", success, f"DNI: {test_dni}")
        return success, test_dni if success else None
    except Exception as e:
        print_test("Create Client", False, f"Error: {str(e)}")
        return False, None

def test_update_client(client_id):
    """Probar actualización de cliente"""
    try:
        data = {
            "nombre": "Cliente",
            "apellidos": "Actualizado Test",
            "correo": f"updated{client_id}@test.com",
            "telefono": "888888888",
            "usuario_modificacion": "admin"
        }
        response = requests.put(f"{API_BASE_URL}/api/clientes/{client_id}", json=data, timeout=5)
        success = response.status_code == 200
        print_test("Update Client", success, f"ID: {client_id}")
        return success
    except Exception as e:
        print_test("Update Client", False, f"Error: {str(e)}")
        return False

def test_register_attendance():
    """Probar registro de asistencia"""
    try:
        # Usar DNI con membresía activa
        data = {"dni": "29480466", "usuario_creacion": "admin"}
        response = requests.post(f"{API_BASE_URL}/api/asistencias", json=data, timeout=5)
        success = response.status_code == 200 or response.status_code == 201
        if success:
            attendance = response.json()
            print_test("Register Attendance", True, f"Cliente: {attendance.get('nombre_cliente', 'N/A')}")
        else:
            error_detail = response.json().get('detail', 'Error desconocido')
            print_test("Register Attendance", False, f"Error: {error_detail}")
        return success
    except Exception as e:
        print_test("Register Attendance", False, f"Error: {str(e)}")
        return False

def test_list_attendance():
    """Probar listado de asistencias"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/asistencias?fecha=2025-11-05", timeout=5)
        success = response.status_code == 200
        attendances = response.json() if success else []
        print_test("List Attendance", success, f"Registros: {len(attendances)}")
        return success
    except Exception as e:
        print_test("List Attendance", False, f"Error: {str(e)}")
        return False

def test_get_products():
    """Probar listado de productos"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/productos", timeout=5)
        success = response.status_code == 200
        products = response.json() if success else []
        print_test("List Products", success, f"Productos: {len(products)}")
        return success
    except Exception as e:
        print_test("List Products", False, f"Error: {str(e)}")
        return False

def run_all_tests():
    """Ejecutar todas las pruebas"""
    print("="*60)
    print("BLESSED GYM - PRUEBAS DE INTEGRACION")
    print("="*60)
    print()

    results = []

    # Pruebas básicas
    print("--- PRUEBAS BASICAS ---")
    results.append(test_health())

    # Autenticación
    print("--- AUTENTICACION ---")
    results.append(test_admin_login())
    results.append(test_client_login())

    # Clientes
    print("--- GESTION DE CLIENTES ---")
    results.append(test_list_clients())
    results.append(test_get_client_by_dni())

    create_success, test_dni = test_create_client()
    results.append(create_success)

    if create_success and test_dni:
        # Obtener ID del cliente creado para actualizarlo
        try:
            response = requests.get(f"{API_BASE_URL}/api/clientes/dni/{test_dni}", timeout=5)
            if response.status_code == 200:
                client_id = response.json().get("id")
                results.append(test_update_client(client_id))
        except:
            results.append(False)

    # Asistencias
    print("--- CONTROL DE ASISTENCIA ---")
    results.append(test_register_attendance())
    results.append(test_list_attendance())

    # Productos
    print("--- PRODUCTOS ---")
    results.append(test_get_products())

    # Resumen
    print("="*60)
    print("RESUMEN")
    print("="*60)
    total = len(results)
    passed = sum(results)
    failed = total - passed

    print(f"Total de pruebas: {total}")
    print(f"Exitosas: {passed}")
    print(f"Fallidas: {failed}")
    print(f"Porcentaje de exito: {(passed/total)*100:.1f}%")
    print()

    if failed == 0:
        print("INTEGRACION COMPLETA Y FUNCIONAL!")
    else:
        print(f"ATENCION: {failed} prueba(s) fallaron")

    return failed == 0

if __name__ == "__main__":
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nPruebas interrumpidas por el usuario")
        exit(1)
    except Exception as e:
        print(f"\nError fatal: {str(e)}")
        exit(1)
