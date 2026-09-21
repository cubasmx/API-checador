import os

import requests
from requests.auth import HTTPDigestAuth

def probar_puerto(port):
    if not (os.getenv("HIK_IP") and os.getenv("HIK_USER") and os.getenv("HIK_PAS")):
        raise SystemExit("Faltan HIK_IP / HIK_USER / HIK_PAS en el entorno (.env)")

    ip = os.getenv("HIK_IP", "")
    user = os.getenv("HIK_USER", "")
    password = os.getenv("HIK_PAS", "")
    url = f"http://{ip}:{port}/ISAPI/System/deviceInfo"
    
    print(f"--- Probando puerto {port} ---")
    try:
        response = requests.get(
            url, 
            auth=HTTPDigestAuth(user, password), 
            timeout=5
        )
        if response.status_code == 200:
            print(f"✅ ¡ÉXITO! El equipo respondió en el puerto {port}")
            print("Datos del equipo:")
            print(response.text[:200]) # Muestra el inicio del XML/JSON
            return True
        else:
            print(f"❌ Error {response.status_code}: Credenciales incorrectas o ISAPI desactivado.")
    except Exception as e:
        print(f"🚫 No se pudo conectar al puerto {port}: {e}")
    return False

# Probar ambos
for p in [80, 8080, 8081]:
    if probar_puerto(p):
        break
