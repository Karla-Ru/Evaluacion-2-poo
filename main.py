
from datetime import date

from proyecto.model.empleado import (
    Empleado,
    validar_tabla_empleado,
    insertar_datos_empleado
)

validar_tabla_empleado()

# Coso para crear empleado
empleado1 = Empleado(
    nombre="Camila González",
    direccion="Puerto Montt",
    telefono="987654321",
    correo_electronico="camila@ecotech.cl",
    fecha_contratacion=date.today(),
    salario=850000
)

print(empleado1.mostrar_datos()) 

insertar_datos_empleado(empleado1) 

empleado1.actualizar_salario(950000) 

empleado1.cambiar_estado(False)
