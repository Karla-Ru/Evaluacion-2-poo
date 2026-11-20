from datetime import date

class Proyecto:
    """ Representa los proyectos desarrollados por la empresa """

    estados_validos = ("Pendiente", "En curso", "Finalizado", "Cancelado")

    def __init__(self, idProyecto: int, nombre: str, descripcion: str, fechaInicio: date, fechaTermino: date, estado: str = "Pendiente"):
        self.__idProyecto   = idProyecto
        self.__nombre       = nombre
        self.__descripcion  = descripcion
        self.__fechaInicio  = fechaInicio
        self.__fechaTermino = fechaTermino
        self.__estado       = estado
        self.__empleados    = [] #Empleados asignados al proyecto

    def idProyecto(self) -> int:
        return self.__idProyecto

    def nombre(self) -> str:
        return self.__nombre

    def descripcion(self) -> str:
        return self.__descripcion

    def fechaInicio(self) -> date:
        return self.__fechaInicio

    def fechaTermino(self) -> date:
        return self.__fechaTermino

    def estado(self) -> str:
        return self.__estado

    def empleados(self) -> list:
        return self.__empleados

# Validar datos del proyecto antes de crearlo
def crearProyecto(self) -> bool:
    if not self.__nombre or not self.__nombre.strip():
        print("Error: El nombre del proyecto no puede estar vacío.")
        return False
    if self.__fechaTermino < self.__fechaInicio:
        print("Error: La fecha de término no puede ser anterior a la de inicio.")
        return False
    if self.__estado not in self.estados_validos:
        print(f"Error: Estado inválido.")
        return False
    print(f"Proyecto '{self.__nombre}' creado correctamente")
    return True

def modificarProyecto(self, nombre: str = None, descripcion: str = None, fechaInicio: date = None, fechaTermino: date = None) -> None:
    if nombre is not None:
        self.__nombre = nombre
    if descripcion is not None:
        self.__ = descripcion
    if fechaInicio is not None:
        self.__fechaiInicio = fechaInicio
    if fechaTermino is not None:
        self.__fechaTermino = fechaTermino
    print(f"Proyecto {self.__idProyecto} modificado correctamente.")

# Elimina el proyecto lo marca como cancelado y libera a los empleados
def ekiminarProyecto(self) -> None:
    self.__empleados.clear()
    self.__estado = "Cancelado"
    print(f"Proyecto '{self.__nombre}' eliminado.")

def asignarEmpleado(self, empleado) -> bool:
    if empleado in self.__empleados:
        print("El empleado ya está asignado a este proyecto.")
        return False
    self.__empleados.append(empleado)
    print("Empleado asignado al proyecto.")
    return True

def liberarEmpleado(self, empleado) -> bool:
    if empleado not in self.__empleados:
        print("El empleado no está asignado a este proyecto.")
        return False
    self.__empleados.remove(empleado)
    print("Empleado liberado del proyecto")
    return True

def cambiarEstado(self, nuevoEstado: str) -> bool:
        if nuevoEstado not in self.estados_validos:
            print(f"Estado inváldo. Use uno de: {', '.join(self.estados_validos)}")
            return False
        self.__estado = nuevoEstado
        print(f"Estado del proyecto cambiado a '{nuevoEstado}'.")
        return True

def __str__(self) -> str:
    return (f"Proyecto [{self.idProyecto}] {self.nombre} | {self.estado} | "
            f"{self.__fechaInicio} -> {self.__fechaTermino} | "
            f"Empleados asignados: {len(self.__empleados)}")

