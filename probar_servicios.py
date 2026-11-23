from proyecto.services.servicio_clima import obtener_clima

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
