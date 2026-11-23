from proyecto.model.generador_informes import GeneradorInformes

def menu_informes():
    try:
        generador = GeneradorInformes()
        generador.mostrar_menu_informes()

    except KeyboardInterrupt:
        print("\n\n[INFO] Generación de informes interrumpida.")

    except Exception as e:
        print(f"\n[ERROR] No fue posible acceder al generador de informes: {e}")