from proyecto.view.vista_departamento import menu_departamentos

def iniciar_prueba():

    try:
        menu_departamentos()

    except KeyboardInterrupt:
        print("\n\nPrueba interrumpida por el usuario.")

    except Exception as e:
        print(f"\n[ERROR] No se pudo ejecutar la vista: {e}")

if __name__ == "__main__":
    iniciar_prueba()

#VISTA PROBADA. FUNCIONA CORRECTAMENTE