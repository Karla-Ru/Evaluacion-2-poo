import requests #TOCA INSTALAR (pip install request)

#DIRECCIONES DE LAS API USADAS (METEO) 
#LA API ENTREGA LAS VARIABLES ACTUALES DE TEMPERATURA, HUMEDAD RELATIVA Y CÓDIGO METEREOLÓGICO

API_GEOCODIFICACION = "https://geocoding-api.open-meteo.com/v1/search"
API_CLIMA = "https://api.open-meteo.com/v1/forecast"

#TRADUCIR CODIGOS CLIMÁTICOS

def interpretar_clima(codigo):

    estados = {
        0: "Despejado",
        1: "Principalmente despejado",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Niebla",
        48: "Niebla con escarcha",
        51: "Llovizna ligera",
        53: "Llovizna moderada",
        55: "Llovizna intensa",
        61: "Lluvia ligera",
        63: "Lluvia moderada",
        65: "Lluvia intensa",
        71: "Nevada ligera",
        73: "Nevada moderada",
        75: "Nevada intensa",
        80: "Chubascos ligeros",
        81: "Chubascos moderados",
        82: "Chubascos intensos",
        95: "Tormenta electrica",
        96: "Tormenta con granizo ligero",
        99: "Tormenta con granizo intenso"
    }

    return estados.get(codigo, "Estado del tiempo no identificado")

#CONSULTAR COORDENADAS DE UNA CIUDAD

def obtener_coordenadas(ciudad, pais=None):

    if not isinstance(ciudad, str) or not ciudad.strip():
        print("[WARNING] Debe ingresar una ciudad valida.")
        return None

    parametros = {
        "name": ciudad.strip(),
        "count": 10,
        "language": "es",
        "format": "json"
    }

    try:
        respuesta = requests.get(
            API_GEOCODIFICACION,
            params=parametros,
            timeout=10
        )

        respuesta.raise_for_status()
        datos = respuesta.json()

        resultados = datos.get("results", [])

        if pais:
            resultados = [
                lugar for lugar in resultados
                if lugar.get("country_code", "").upper() == pais.upper()
            ]

        if not resultados:
            print("[WARNING] No se encontro la ciudad indicada.")
            return None

        lugar = resultados[0] #SE UTILIZA EL PRIMER RESULTADO QUE COINCIDA

        return {
            "ciudad": lugar.get("name"),
            "pais": lugar.get("country"),
            "latitud": lugar.get("latitude"),
            "longitud": lugar.get("longitude")
        }

    except requests.exceptions.Timeout:
        print("[ERROR] La consulta de ubicacion excedio el tiempo de espera.")

    except requests.exceptions.ConnectionError:
        print("[ERROR] No fue posible conectar con el servicio de ubicacion.")

    except requests.exceptions.HTTPError:
        print("[ERROR] El servicio de ubicacion respondio con un error.")

    except (ValueError, KeyError):
        print("[ERROR] No fue posible procesar la respuesta de ubicacion.")

    except requests.exceptions.RequestException:
        print("[ERROR] Ocurrio un problema al consultar la ubicacion.")

    return None

#CONSULTAR INFORMACION CLIMATICA

def obtener_clima(ciudad, pais=None):

    ubicacion = obtener_coordenadas(ciudad, pais)

    if ubicacion is None:
        return None

    parametros = {
        "latitude": ubicacion["latitud"],
        "longitude": ubicacion["longitud"],
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "weather_code"
        ],
        "timezone": "auto"
    }

    try:
        respuesta = requests.get(
            API_CLIMA,
            params=parametros,
            timeout=10
        )

        respuesta.raise_for_status()
        datos = respuesta.json()

        clima = datos.get("current")

        if not clima:
            print("[ERROR] La API no entrego informacion climatica.")
            return None

        codigo = clima.get("weather_code")

        if codigo is None:
            print("[ERROR] La respuesta no contiene el estado del tiempo.")
            return None

        return {
            "ciudad": ubicacion["ciudad"],
            "pais": ubicacion["pais"],
            "temperatura": clima.get("temperature_2m"),
            "humedad": clima.get("relative_humidity_2m"),
            "estado": interpretar_clima(codigo),
            "fecha_consulta": clima.get("time")
        }

    except requests.exceptions.Timeout:
        print("[ERROR] La consulta climatica excedio el tiempo de espera.")

    except requests.exceptions.ConnectionError:
        print("[ERROR] No fue posible conectar con el servicio climatico.")

    except requests.exceptions.HTTPError:
        print("[ERROR] El servicio climatico respondio con un error HTTP.")

    except (ValueError, KeyError):
        print("[ERROR] No fue posible procesar la respuesta climatica.")

    except requests.exceptions.RequestException:
        print("[ERROR] Ocurrio un problema al consultar el clima.")

    return None