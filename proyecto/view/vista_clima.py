from proyecto.services.servicio_clima import obtener_clima

def pausar():
    input("\nPresione ENTER para continuar...")

def consultar_clima():

    print("\n========== CONSULTAR CLIMA ==========")

    ciudad = input("Ingrese el nombre de la ciudad: ").strip()

    if not ciudad:
        print("[WARNING] Debe ingresar una ciudad.")
        return

    pais = input(
        "Código del país (CL, AR, etc.) o ENTER para omitir: "
    ).strip().upper()

    if pais and (len(pais) != 2 or not pais.isalpha()):
        print("[WARNING] Ingrese un código de país de dos letras.")
        return

    # Consultar el servicio climático
    clima = obtener_clima(ciudad, pais if pais else None)

    if clima is None:
        print("\n[ERROR] No fue posible obtener la información climática.")
        return

    print("\n")
    print("============================================")
    print("          INFORMACIÓN CLIMÁTICA")
    print("============================================")
    print(f"Ciudad:       {clima['ciudad']}")
    print(f"País:         {clima['pais']}")
    print("--------------------------------------------")
    print(f"Temperatura:  {clima['temperatura']} °C")
    print(f"Humedad:      {clima['humedad']} %")
    print(f"Estado:       {clima['estado']}")
    print("--------------------------------------------")
    print(f"Fecha:        {clima['fecha_consulta']}")
    print("============================================")

def menu_clima():

    while True:

        print("\n")
        print("============================================")
        print("           SERVICIO CLIMÁTICO")
        print("============================================")
        print("1. Consultar clima de una ciudad")
        print("0. Volver al menú principal")
        print("============================================")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            consultar_clima()
            pausar()

        elif opcion == "0":
            break

        else:
            print("\n[WARNING] Opción no válida.")
            pausar()