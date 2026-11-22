
from proyecto.config.app_config import conectar_db


class GeneradorInformes:

    def __init__(self):
        self.nombre_sistema = "EcoTech Solutions"

    #MÉTODO GENERAL PARA EJECUTAR CONSULTAS
    @staticmethod
    def ejecutar_consulta(consulta_sql, parametros=None):

        conn = None
        cursor = None

        try:
            conn = conectar_db()

            if conn:
                cursor = conn.cursor()

                if parametros:
                    cursor.execute(consulta_sql, parametros)
                else:
                    cursor.execute(consulta_sql)

                resultados = cursor.fetchall()
                return resultados

            return []

        except Exception as e:
            print(f"[ERROR] No se pudo generar el informe | {e}")
            return []

        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()

    #INFORME DE EMPLEADOS
    def generar_informe_empleados(self):

        consulta_sql = """
            SELECT
                id_empleado,
                nombre,
                direccion,
                telefono,
                correo_electronico,
                fecha_contratacion,
                salario,
                activo
            FROM empleados
            ORDER BY id_empleado
        """

        resultados = self.ejecutar_consulta(consulta_sql)

        print("\n========== INFORME DE EMPLEADOS ==========")

        if not resultados:
            print("No existen empleados registrados.")
            return

        for empleado in resultados:

            estado = "Activo" if empleado[7] == 1 else "Inactivo"

            print(f"""
            ID: {empleado[0]}
            Nombre: {empleado[1]}
            Dirección: {empleado[2]}
            Teléfono: {empleado[3]}
            Correo: {empleado[4]}
            Fecha de contratación: {empleado[5]}
            Salario: ${empleado[6]}
            Estado: {estado}
            --------------------------------------------
            """)

        print(f"Total de empleados: {len(resultados)}")

    #INFORME DE DEPARTAMENTOS
    def generar_informe_departamentos(self):

        consulta_sql = """
            SELECT
                d.id_departamento,
                d.nombre,
                d.descripcion,
                e.nombre
            FROM departamentos d
            LEFT JOIN empleados e
                ON d.id_gerente = e.id_empleado
            ORDER BY d.id_departamento
        """

        resultados = self.ejecutar_consulta(consulta_sql)

        print("\n========== INFORME DE DEPARTAMENTOS ==========")

        if not resultados:
            print("No existen departamentos registrados.")
            return

        for departamento in resultados:

            gerente = departamento[3] if departamento[3] else "Sin gerente asignado"

            print(f"""
            ID Departamento: {departamento[0]}
            Nombre: {departamento[1]}
            Descripción: {departamento[2]}
            Gerente: {gerente}
            --------------------------------------------
            """)

        print(f"Total de departamentos: {len(resultados)}")

    #INFORME DE PROYECTOS
    def generar_informe_proyectos(self):

        consulta_sql = """
            SELECT
                p.id_proyecto,
                p.nombre,
                p.descripcion,
                p.fecha_inicio,
                p.fecha_termino,
                p.estado,
                COUNT(pe.id_empleado)
            FROM proyectos p
            LEFT JOIN proyecto_empleado pe
                ON p.id_proyecto = pe.id_proyecto
            GROUP BY
                p.id_proyecto,
                p.nombre,
                p.descripcion,
                p.fecha_inicio,
                p.fecha_termino,
                p.estado
            ORDER BY p.id_proyecto
        """

        resultados = self.ejecutar_consulta(consulta_sql)

        print("\n========== INFORME DE PROYECTOS ==========")

        if not resultados:
            print("No existen proyectos registrados.")
            return

        for proyecto in resultados:

            print(f"""
            ID Proyecto: {proyecto[0]}
            Nombre: {proyecto[1]}
            Descripción: {proyecto[2]}
            Fecha de inicio: {proyecto[3]}
            Fecha de término: {proyecto[4]}
            Estado: {proyecto[5]}
            Cantidad de empleados asignados: {proyecto[6]}
            --------------------------------------------
            """)

        print(f"Total de proyectos: {len(resultados)}")

    #INFORME DE EMPLEADOS ASIGNADOS A PROYECTOS
    def generar_informe_asignaciones(self):

        consulta_sql = """
            SELECT
                p.nombre,
                e.id_empleado,
                e.nombre,
                e.correo_electronico
            FROM proyecto_empleado pe
            INNER JOIN proyectos p
                ON pe.id_proyecto = p.id_proyecto
            INNER JOIN empleados e
                ON pe.id_empleado = e.id_empleado
            ORDER BY p.nombre, e.nombre
        """

        resultados = self.ejecutar_consulta(consulta_sql)

        print("\n========== INFORME DE ASIGNACIONES ==========")

        if not resultados:
            print("No existen empleados asignados a proyectos.")
            return

        for asignacion in resultados:

            print(f"""
Proyecto: {asignacion[0]}
ID Empleado: {asignacion[1]}
Empleado: {asignacion[2]}
Correo: {asignacion[3]}
--------------------------------------------
""")

        print(f"Total de asignaciones: {len(resultados)}")

    #MENÚ DEL GENERADOR DE INFORMES
    def mostrar_menu_informes(self):

        while True:

            print("\n======================================")
            print("     GENERADOR DE INFORMES")
            print("          EcoTech Solutions")
            print("======================================")
            print("1. Informe de empleados")
            print("2. Informe de departamentos")
            print("3. Informe de proyectos")
            print("4. Informe de asignaciones")
            print("5. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.generar_informe_empleados()

            elif opcion == "2":
                self.generar_informe_departamentos()

            elif opcion == "3":
                self.generar_informe_proyectos()

            elif opcion == "4":
                self.generar_informe_asignaciones()

            elif opcion == "5":
                print("Saliendo del generador de informes...")
                break

            else:
                print("[WARNING] Opción no válida. Intente nuevamente.")