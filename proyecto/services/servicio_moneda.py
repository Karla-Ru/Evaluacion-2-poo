import requests

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re

#DIRECCIÓN DE LA API IMPLEMENTADA ()
API_MONEDA = "https://api.frankfurter.dev/v2"

#VALIDAR CODIGO DE MONEDA
def validar_moneda(moneda):

    if not isinstance(moneda, str):
        return False

    return bool(re.fullmatch(r"[A-Za-z]{3}", moneda.strip()))


#CONSULTAR TIPO DE CAMBIO
def obtener_tipo_cambio(moneda_origen, moneda_destino):

    if not validar_moneda(moneda_origen):
        print("[WARNING] Codigo de moneda de origen no valido.")
        return None

    if not validar_moneda(moneda_destino):
        print("[WARNING] Codigo de moneda de destino no valido.")
        return None

    origen = moneda_origen.strip().upper()
    destino = moneda_destino.strip().upper()

    if origen == destino: #SI AMBAS MONEDAS SON IGUALES, EL CAMBIO ES 1 
        return {
            "origen": origen,
            "destino": destino,
            "tipo_cambio": Decimal("1"),
            "fecha": None
        }

    url = f"{API_MONEDA}/rate/{origen.lower()}/{destino.lower()}"

    try:
        respuesta = requests.get(
            url,
            timeout=10
        )

        respuesta.raise_for_status()

        datos = respuesta.json(parse_float=Decimal)

        tipo_cambio = Decimal(str(datos["rate"]))

        return {
            "origen": datos["base"].upper(),
            "destino": datos["quote"].upper(),
            "tipo_cambio": tipo_cambio,
            "fecha": datos.get("date")
        }

    except requests.exceptions.Timeout:
        print("[ERROR] La consulta del tipo de cambio excedio el tiempo de espera.")

    except requests.exceptions.ConnectionError:
        print("[ERROR] No fue posible conectar con el servicio economico.")

    except requests.exceptions.HTTPError as e:

        codigo = e.response.status_code if e.response is not None else None

        if codigo == 404:
            print("[ERROR] No se encontro el tipo de cambio solicitado.")

        elif codigo == 422:
            print("[ERROR] La API no pudo procesar las monedas solicitadas.")

        else:
            print("[ERROR] El servicio economico respondio con un error.")

    except (ValueError, KeyError, InvalidOperation, TypeError):
        print("[ERROR] No fue posible procesar el tipo de cambio.")

    except requests.exceptions.RequestException:
        print("[ERROR] Ocurrio un problema al consultar el servicio economico.")

    return None

#CONVERTIR MONEDA

def convertir_moneda(monto, moneda_origen, moneda_destino):

    try:
        monto = Decimal(str(monto))

        if not monto.is_finite() or monto <= 0:
            print("[WARNING] El monto debe ser un numero positivo.")
            return None

    except (InvalidOperation, ValueError, TypeError):
        print("[WARNING] El monto ingresado no es valido.")
        return None

    cambio = obtener_tipo_cambio(
        moneda_origen,
        moneda_destino
    )

    if cambio is None:
        return None

    resultado = (
        monto * cambio["tipo_cambio"]
    ).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

    return {
        "monto_original": monto,
        "moneda_origen": cambio["origen"],
        "moneda_destino": cambio["destino"],
        "tipo_cambio": cambio["tipo_cambio"],
        "monto_convertido": resultado,
        "fecha": cambio["fecha"]
    }