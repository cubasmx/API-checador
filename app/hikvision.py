import requests
from requests.auth import HTTPDigestAuth
from datetime import datetime

HIK_CONFIG = {
    "ip": "10.10.2.250",
    "port": "8081",
    "user": "admin",
    "pass": "Ensa2025"
}

def obtener_eventos_recientes(max_results=250):
    url = f"http://{HIK_CONFIG['ip']}:{HIK_CONFIG['port']}/ISAPI/AccessControl/AcsEvent?format=json"

    # Basado en tus capacidades, usaremos el formato ISO 8601 estricto con la 'Z'
    # Asegúrate de haber sincronizado el reloj del checador con la PC antes.
    hoy = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
    ahora = datetime.now().strftime("%Y-%m-%dT23:59:59Z")

    payload = {
        "AcsEventCond": {
            "searchID": "1",
            "searchResultPosition": 0,
            "maxResults": max_results,
            "major": 0,  # Eventos de acceso
            "minor": 0, # Acceso concedido
	    "timeReverseOrder": True
        }
    }

    try:
        print(f"--- Consultando eventos v5.0 a {url} ---")
        response = requests.post(
            url,
            auth=HTTPDigestAuth(HIK_CONFIG['user'], HIK_CONFIG['pass']),
            json=payload,
            timeout=10
        )

        print(f"Status del equipo: {response.status_code}")

        if response.status_code == 200:
            datos = response.json()
            # En v5.0, la estructura de respuesta es AcsEvent -> InfoList (que es una lista)
            # Tus capacidades dicen que InfoList es el contenedor de los datos
            eventos = datos.get("AcsEvent", {}).get("InfoList", [])
            print(f"¡ÉXITO! Recibidos {len(eventos)} eventos.")
            return eventos
        else:
            print(f"Fallo del equipo: {response.text}")
            return None
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return None
