
from datetime import date

from proyecto.model.empleado import (
    Empleado,
    validar_tabla_empleado,
    insertar_datos_empleado
)

from proyecto.model.proyecto import (Proyecto, validar_tabla_proyecto)


def main():
    validar_tabla_empleado()
    validar_tabla_proyecto()

#EJECUCIÓN DE EMPLEADO
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

#EJECUCIÓN DE DEPARTAMENTO
from proyecto.model.departamento import (
    Departamento,
    validar_tabla_departamento,
    insertar_datos_departamento
)

validar_tabla_departamento()

#CREAR UN DEPARTAMENTO
departamento = Departamento(
    nombre="Desarrollo Tecnológico",
    descripcion="Departamento encargado del desarrollo de soluciones tecnológicas.",
    id_gerente=1
)

#INSERTAR EN ORACLE
insertar_datos_departamento(departamento)

#MOSTRAR INFO
print(departamento.mostrar_datos())

#LO DE USUARIOS
from proyecto.model.usuario_sistema import (
    validar_tabla_usuario_sistema,
    autenticar_usuario
)

from proyecto.model.usuario_empleado import (
    UsuarioEmpleado,
    insertar_usuario_empleado
)
