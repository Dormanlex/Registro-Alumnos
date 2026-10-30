import sqlite3
import os

DB_NAME = "alumnos.db"

def inicializar_base():
    """Crea la tabla de alumnos si no existe."""
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alumnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            materia TEXT NOT NULL,
            nota1 REAL NOT NULL,
            nota2 REAL NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def ver_boletin():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, materia, nota1, nota2 FROM alumnos")
    registros = cursor.fetchall()
    conexion.close()

    limpiar_pantalla()
    print("\n==========================================================================")
    print("                         BOLETÍN DE CALIFICACIONES")
    print("==========================================================================")
    
    if not registros:
        print("No hay alumnos registrados en la base de datos.")
    else:
        for r in registros:
            # r[0]=id, r[1]=nombre, r[2]=materia, r[3]=nota1, r[4]=nota2
            promedio = (r[3] + r[4]) / 2
            estado = "Aprobado" if promedio >= 6.0 else "Desaprobado"
            print(f"ID: {r[0]:<3} | Alumno: {r[1]:<18} | Materia: {r[2]:<12} | Promed: {promedio:<4.1f} | Estado: {estado}")
    
    print("==========================================================================")
    input("\nPresione Enter para continuar...")

def registrar_alumno():
    limpiar_pantalla()
    print("\n--- REGISTRAR ALUMNO Y NOTAS ---")
    nombre = input("Nombre del alumno: ").strip()
    if not nombre:
        print("¡ERROR! El nombre no puede estar vacío.")
        input("\nPresione Enter para continuar...")
        return

    materia = input("Materia: ").strip() or "Programación"

    try:
        n1 = float(input("Nota 1 (1-10): ").strip())
        n2 = float(input("Nota 2 (1-10): ").strip())
        if not (1 <= n1 <= 10 and 1 <= n2 <= 10):
            print("¡ERROR! Las notas deben estar dentro del rango de 1 a 10.")
            input("\nPresione Enter para continuar...")
            return
    except ValueError:
        print("¡ERROR! Ingrese valores numéricos válidos para las notas.")
        input("\nPresione Enter para continuar...")
        return

    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO alumnos (nombre, materia, nota1, nota2)
        VALUES (?, ?, ?, ?)
    """, (nombre, materia, n1, n2))
    conexion.commit()
    conexion.close()

    print(f"\n¡ÉXITO! Registro de '{nombre}' guardado correctamente.")
    input("\nPresione Enter para continuar...")

def buscar_alumno():
    limpiar_pantalla()
    print("\n--- BUSCAR REGISTROS DE ALUMNO ---")
    busqueda = input("Ingrese el nombre a buscar: ").strip()
    if not busqueda:
        print("¡ERROR! Debe ingresar un texto para buscar.")
        input("\nPresione Enter para continuar...")
        return

    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    # Uso de LIKE para buscar coincidencias parciales del nombre
    cursor.execute("SELECT id, nombre, materia, nota1, nota2 FROM alumnos WHERE nombre LIKE ?", (f"%{busqueda}%",))
    resultados = cursor.fetchall()
    conexion.close()

    print("\n--------------------------------------------------------------------------")
    if not resultados:
        print(f"No se encontraron registros para '{busqueda}'.")
    else:
        print(f"Se encontraron {len(resultados)} registro(s):")
        for r in resultados:
            promedio = (r[3] + r[4]) / 2
            estado = "Aprobado" if promedio >= 6.0 else "Desaprobado"
            print(f"ID: {r[0]:<3} | Alumno: {r[1]:<18} | Materia: {r[2]:<12} | Promed: {promedio:<4.1f} | Estado: {estado}")
    print("--------------------------------------------------------------------------")
    input("\nPresione Enter para continuar...")

def eliminar_registro():
    limpiar_pantalla()
    print("\n--- ELIMINAR REGISTRO ACADÉMICO ---")
    try:
        id_eliminar = int(input("Ingrese el ID del registro a eliminar: ").strip())
    except ValueError:
        print("¡ERROR! Ingrese un número de ID válido.")
        input("\nPresione Enter para continuar...")
        return

    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, materia FROM alumnos WHERE id = ?", (id_eliminar,))
    resultado = cursor.fetchone()

    if resultado:
        cursor.execute("DELETE FROM alumnos WHERE id = ?", (id_eliminar,))
        conexion.commit()
        print(f"\n¡ÉXITO! Registro de '{resultado[0]}' en '{resultado[1]}' eliminado correctamente.")
    else:
        print("¡ERROR! No existe ningún registro con ese ID.")
        
    conexion.close()
    input("\nPresione Enter para continuar...")

def main():
    inicializar_base()
    
    while True:
        limpiar_pantalla()
        print("\n========================================")
        print("      SISTEMA DE NOTAS Y ALUMNOS")
        print("========================================")
        print("1. Ver boletín general")
        print("2. Registrar alumno y notas")
        print("3. Buscar por nombre del alumno")
        print("4. Eliminar registro")
        print("5. Salir")
        print("----------------------------------------")

        opcion = input("Seleccione una opción (1-5): ").strip()

        if opcion == "1":
            ver_boletin()
        elif opcion == "2":
            registrar_alumno()
        elif opcion == "3":
            buscar_alumno()
        elif opcion == "4":
            eliminar_registro()
        elif opcion == "5":
            print("\n¡Saliendo del programa... Hasta luego!")
            break
        else:
            print("¡ERROR! Opción inválida. Intente de nuevo.")
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()