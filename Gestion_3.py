import sqlite3
import os

# Nombre del archivo de base de datos
DB_NAME = "inventario_v2.db"

def inicializar_base():
    """Crea la tabla de productos si todavía no existe."""
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def ver_inventario():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, categoria, precio, stock FROM productos")
    productos = cursor.fetchall()
    conexion.close()

    limpiar_pantalla()
    print("\n==========================================================================")
    print("                         INVENTARIO DE PRODUCTOS")
    print("==========================================================================")
    
    if not productos:
        print("El inventario está completamente vacío.")
    else:
        for p in productos:
            # p[0]=id, p[1]=nombre, p[2]=categoria, p[3]=precio, p[4]=stock
            print(f"ID: {p[0]:<3} | Nombre: {p[1]:<18} | Categoría: {p[2]:<12} | Precio: ${p[3]:<8.2f} | Stock: {p[4]:<4} u.")
    
    print("==========================================================================")
    input("\nPresione Enter para continuar...")

def agregar_producto():
    limpiar_pantalla()
    print("\n--- AGREGAR PRODUCTO ---")
    nombre = input("Nombre del producto: ").strip()
    if not nombre:
        print("¡ERROR! El nombre no puede estar vacío.")
        input("\nPresione Enter para continuar...")
        return

    categoria = input("Categoría: ").strip() or "General"
    
    try:
        precio = float(input("Precio ($): ").strip())
        if precio < 0:
            print("¡ERROR! El precio no puede ser negativo.")
            input("\nPresione Enter para continuar...")
            return
    except ValueError:
        print("¡ERROR! Ingrese un número válido para el precio.")
        input("\nPresione Enter para continuar...")
        return

    try:
        stock = int(input("Cantidad en stock: ").strip())
        if stock < 0:
            print("¡ERROR! El stock no puede ser negativo.")
            input("\nPresione Enter para continuar...")
            return
    except ValueError:
        print("¡ERROR! Ingrese un número entero válido para el stock.")
        input("\nPresione Enter para continuar...")
        return

    # Guardar en la base de datos SQLite
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO productos (nombre, categoria, precio, stock)
        VALUES (?, ?, ?, ?)
    """, (nombre, categoria, precio, stock))
    conexion.commit()
    conexion.close()

    print(f"\n¡ÉXITO! Producto '{nombre}' agregado correctamente.")
    input("\nPresione Enter para continuar...")

def eliminar_producto():
    limpiar_pantalla()
    print("\n--- ELIMINAR PRODUCTO ---")
    try:
        id_eliminar = int(input("Ingrese el ID del producto a eliminar: ").strip())
    except ValueError:
        print("¡ERROR! Ingrese un ID válido.")
        input("\nPresione Enter para continuar...")
        return

    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    
    # Verificar si el producto existe antes de borrarlo
    cursor.execute("SELECT nombre FROM productos WHERE id = ?", (id_eliminar,))
    resultado = cursor.fetchone()

    if resultado:
        cursor.execute("DELETE FROM productos WHERE id = ?", (id_eliminar,))
        conexion.commit()
        print(f"\n¡ÉXITO! Producto '{resultado[0]}' eliminado correctamente.")
    else:
        print("¡ERROR! No existe ningún producto con ese ID.")
        
    conexion.close()
    input("\nPresione Enter para continuar...")

def main():
    inicializar_base()
    
    while True:
        limpiar_pantalla()
        print("\n========================================")
        print("      GESTOR DE INVENTARIO SQLITE")
        print("========================================")
        print("1. Ver inventario completo")
        print("2. Agregar nuevo producto")
        print("3. Eliminar producto")
        print("4. Salir")
        print("----------------------------------------")

        opcion = input("Seleccione una opción (1-4): ").strip()

        if opcion == "1":
            ver_inventario()
        elif opcion == "2":
            agregar_producto()
        elif opcion == "3":
            eliminar_producto()
        elif opcion == "4":
            print("\nSaliendo del programa...")
            break
        else:
            print("¡ERROR! Opción inválida. Intente de nuevo.")
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()