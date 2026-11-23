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

# CREAR UN PROYECTO
proyecto1 = Proyecto (
    nombre="Sitio Web Corporativo",
    descripcion="Desarrollo del nuevo sitio web de la empresa",
    fechaInicio=date(2026, 1, 10),
    fechaTermino=date(2026, 6, 30),
)
proyecto1.crearProyecto()

# CAMBIAR EDSTADO Y MODIFICAR DATOS
proyecto1.cambiarEstado("En curso")
proyecto1.modificarProyecto(nombre="Sitio Web 2.0", fechaTermino=date(2026, 8, 31))

# ASIGNAR EMPLEADO
proyecto1.asignarEmpleado(1)
proyecto1.desasignarEmpleado(1)

# MOSTRAR LOS PROYECTOS GUARDADOS
print("\n--- Proyectos en la base de datos ---")
for p in Proyecto.listarProyectos():
    print(p)

# ELIMINAR PROYECTO
proyecto1.eliminarProyecto()

if __name__ == "__main__":
    main()


#LO DE USUARIOS
from proyecto.model.usuario_sistema import (
    validar_tabla_usuario_sistema,
    autenticar_usuario
)

from proyecto.model.usuario_empleado import (
    UsuarioEmpleado,
    insertar_usuario_empleado
)

#EJECUCIÓN ADMINISTRADOR

from proyecto.model.administrador import Administrador, insertar_administrador

administrador = Administrador(
    nombre_usuario="admin",
    clave="Admin12345"
)

insertar_administrador(administrador)

print(administrador.mostrar_datos())

print(administrador.mostrar_permisos()) #CONSULTAR PERMISOS

administrador.gestionar_empleados() #PROBAR FUNCIONALIDADES
administrador.gestionar_proyectos()
administrador.consultar_informes()

#EJECUCIÓN ROL

from proyecto.model.rol import (
    Rol,
    Permiso,
    validar_tabla_rol,
    validar_tabla_rol_permiso,
    insertar_rol,
    asignar_permiso_rol
)

from proyecto.model.permiso import ( #AQUÍ HAY DOS FROM PORQUE PERTENECEN A MÓDULOS DISNTINTOS, PYTHON NO PERMITE AGRUPAR ELEMENTOS DE DISTINTOS M´DULOS EN ÚNICO FROM 
    Permiso,
    validar_tabla_permiso,
    insertar_permiso
)

#CREAR TABLAS
validar_tabla_rol()
validar_tabla_permiso()
validar_tabla_rol_permiso()

#CREAR ROL ADMINISTRADOR
rol_admin = Rol(
    nombre="ADMINISTRADOR",
    descripcion="Acceso a las funciones administrativas del sistema."
)

insertar_rol(rol_admin)

#CREAR PERMISOS
permiso_empleados = Permiso(
    nombre="GESTIONAR_EMPLEADOS",
    descripcion="Permite registrar, modificar y eliminar empleados."
)

permiso_proyectos = Permiso(
    nombre="GESTIONAR_PROYECTOS",
    descripcion="Permite administrar los proyectos."
)

permiso_informes = Permiso(
    nombre="CONSULTAR_INFORMES",
    descripcion="Permite consultar los informes del sistema."
)

insertar_permiso(permiso_empleados)
insertar_permiso(permiso_proyectos)
insertar_permiso(permiso_informes)

#PERMISOS

from proyecto.model.permiso import (
    Permiso,
    validar_tabla_permiso,
    insertar_permiso
)

#EJECUCIÓN PERMISOS

validar_tabla_permiso()

permiso = Permiso(
    nombre="GESTIONAR_EMPLEADOS",
    descripcion="Permite registrar, modificar y eliminar empleados."
)

insertar_permiso(permiso)

print(permiso.mostrar_datos())

#GENERADOR INFORME

from proyecto.model.generador_informes import GeneradorInformes