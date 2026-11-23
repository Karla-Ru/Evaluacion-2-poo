#SE CREA ESTO TEMPORALMENTE PARA PROBAR QUE FUNCIONEN CORRECTAMENTE LAS APIS Y PARA HACER UNA VISTA DE CÓMO SE VE EN LA TERMINAL (INTEGRAR CON LO DEMÁS EN VIEW DESPUÉS)
#NO OLVIDAR TRASPASAR NOTAS DE LA LIBRETA A VSCODE
#SERVICIOS FUNCIONAN CORRECTAMENTE

from proyecto.services.servicio_clima import obtener_clima
from proyecto.services.servicio_moneda import convertir_moneda #SE AGREGA EL IMPORT DEL CONVERSOR DE MONEDA

#PRACTICAR EL USO DE PRINT PARA LUEGO SEGUIR DESARROLLANDO LA INTERFÁZ
#PRUEBA DEL SERVICIO CLIMATICO

print("\n===== PRUEBA DE SERVICIO CLIMATICO =====")

clima = obtener_clima("Puerto Montt", "CL")

if clima:

    print("\nINFORMACION CLIMATICA")
    print("Ciudad:", clima["ciudad"])
    print("Pais:", clima["pais"])
    print("Temperatura:", clima["temperatura"], "°C")
    print("Humedad:", clima["humedad"], "%")
    print("Estado:", clima["estado"])
    print("Fecha:", clima["fecha_consulta"])

#PRUEBA DEL SERVICIO DE CONVERSIÓN DE MONEDA

print("\n===== PRUEBA DE SERVICIO ECONOMICO =====")

conversion = convertir_moneda(
    500,
    "USD",
    "CLP"
)

if conversion:

    print("\nRESULTADO DE CONVERSION")
    print("Monto original:",
          conversion["monto_original"],
          conversion["moneda_origen"])

    print("Tipo de cambio:",
          conversion["tipo_cambio"])

    print("Monto convertido:",
          conversion["monto_convertido"],
          conversion["moneda_destino"])

    print("Fecha del tipo de cambio:",
          conversion["fecha"])
