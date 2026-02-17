import requests

from requests.auth import HTTPDigestAuth

from datetime import datetime

import time


HIK_CONFIG = {

    "ip": "10.10.2.250",

    "port": "8081",

    "user": "admin",

    "pass": "Ensa2025"

}

def obtener_eventos_recientes(max_results=250):
    url = f"http://{HIK_CONFIG['ip']}:{HIK_CONFIG['port']}/ISAPI/AccessControl/AcsEvent?format=json"
    
    nuevo_id = str(int(time.time()))
    
    # Forzamos un rango de hoy para que no haya duda
    # Usamos -06:00 que es tu zona horaria según los logs anteriores
    payload = {
        "AcsEventCond": {
            "searchID": nuevo_id,
            "searchResultPosition": 0,
            "maxResults": max_results,
            "major": 5,
            "minor": 0,
            "startTime": "2026-02-17T00:00:00-06:00",
            "endTime": "2026-02-17T23:59:59-06:00",
            "timeReverseOrder": True
        }
    }

    try:
        response = requests.post(
            url,
            auth=HTTPDigestAuth(HIK_CONFIG['user'], HIK_CONFIG['pass']),
            json=payload,
            timeout=15
        )
        
        datos = response.json()
        # Intentamos extraer de 'data' o de la estructura estándar
        eventos = datos.get("data") or datos.get("AcsEvent", {}).get("InfoList", [])
        total = datos.get("total") or datos.get("AcsEvent", {}).get("totalMatches", 0)
        
        print(f"Resultado: {len(eventos)} eventos encontrados.")
        return eventos
    except Exception as e:
        print(f"Error: {e}")
        return []
