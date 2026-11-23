from proyecto.view.vista_moneda import menu_monedas

def iniciar_prueba():
    try:
        menu_monedas()

    except KeyboardInterrupt:
        print("\n\n[INFO] Prueba interrumpida por el usuario.")

    except Exception as e:
        print(f"\n[ERROR] No se pudo ejecutar la vista: {e}")

if __name__ == "__main__":
    iniciar_prueba()