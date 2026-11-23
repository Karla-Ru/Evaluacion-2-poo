from proyecto.services.servicio_moneda import convertir_moneda

def pausar():
    input("\nPresione ENTER para continuar...")

def realizar_conversion():
    print("\n========== CONVERSIÓN DE MONEDAS ==========")

    monto = input("Ingrese el monto que desea convertir: ").strip()
    moneda_origen = input("Moneda de origen (ej. USD): ").strip().upper()
    moneda_destino = input("Moneda de destino (ej. CLP): ").strip().upper()

    #VALIDAR QUE LOS CÓDIGOS TENGAN TRES LETRAS
    if (
        len(moneda_origen) != 3
        or not moneda_origen.isalpha()
        or len(moneda_destino) != 3
        or not moneda_destino.isalpha()
    ):
        print("\n[WARNING] Los códigos de moneda deben tener tres letras.")
        return

    #CONSULTAR EL SERVICIO DE CONVERSIÓN DE MONEDA
    resultado = convertir_moneda(
        monto,
        moneda_origen,
        moneda_destino
    )

    if resultado is None:
        print("\n[ERROR] No fue posible realizar la conversión.")
        print("Verifique el monto, los códigos de moneda y su conexión a Internet.")
        return

    #MOSTRAR RESULTADOS
    print("\n")
    print("============================================")
    print("           RESULTADO DE CONVERSIÓN")
    print("============================================")
    print(
        f"Monto original:  {resultado['monto_original']} "
        f"{resultado['moneda_origen']}"
    )
    print("--------------------------------------------")
    print(f"Tipo de cambio:  {resultado['tipo_cambio']}")
    print(
        f"Monto convertido: {resultado['monto_convertido']} "
        f"{resultado['moneda_destino']}"
    )
    print("--------------------------------------------")
    print(f"Fecha del tipo de cambio: {resultado['fecha']}")
    print("============================================")

def menu_monedas():
    while True:
        print("\n")
        print("============================================")
        print("             SERVICIO DE MONEDAS")
        print("============================================")
        print("1. Convertir monedas")
        print("0. Volver al menú principal")
        print("============================================")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            realizar_conversion()
            pausar()

        elif opcion == "0":
            break

        else:
            print("\n[WARNING] Opción no válida.")
            pausar()