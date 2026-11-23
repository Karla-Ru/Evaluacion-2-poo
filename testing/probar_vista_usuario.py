from proyecto.view.vista_usuario import menu_usuarios

def iniciar_prueba():

    try:
        menu_usuarios()

    except KeyboardInterrupt:
        print("\n\n[INFO] Prueba interrumpida por el usuario.")

    except Exception as e:
        print(f"\n[ERROR] No se pudo ejecutar la vista: {e}")

if __name__ == "__main__":
    iniciar_prueba()

#PROBADO, FUNCIONA CORRECTAMENTE