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