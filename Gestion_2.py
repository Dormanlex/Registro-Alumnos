import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List

# MODELO DE DATOS
@dataclass
class Producto:
    id: int
    nombre: str
    categoria: str
    precio: float
    stock: int
    fecha_creacion: str

    def a_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Producto":
        return cls(**data)


# CLASE GESTORA DEL INVENTARIO
class GestorInventario:
    def __init__(self, ruta_archivo: str = "inventario.json"):
        self.ruta_archivo = ruta_archivo
        self.productos: List[Producto] = []
        self.cargar_datos()

    def cargar_datos(self) -> None:
        """Carga los datos desde el archivo JSON si existe."""
        if not os.path.exists(self.ruta_archivo):
            self.guardar_datos()
            return

        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                self.productos = [Producto.from_dict(p) for p in datos]
        except (json.JSONDecodeError, IOError) as e:
            print(f"¡ADVERTENCIA! Error al cargar la base de datos: {e}")
            self.productos = []

    def guardar_datos(self) -> None:
        """Guarda la lista actual de productos en el archivo JSON."""
        try:
            with open(self.ruta_archivo, "w", encoding="utf-8") as archivo:
                datos = [p.a_dict() for p in self.productos]
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"¡ERROR! No se pudieron guardar los datos: {e}")

    def generar_id(self) -> int:
        """Genera un ID autoincremental único."""
        if not self.productos:
            return 1
        return max(p.id for p in self.productos) + 1

    def agregar_producto(self, nombre: str, categoria: str, precio: float, stock: int) -> Producto:
        nuevo_id = self.generar_id()
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        producto = Producto(
            id=nuevo_id,
            nombre=nombre,
            categoria=categoria,
            precio=precio,
            stock=stock,
            fecha_creacion=fecha_actual
        )
        self.productos.append(producto)
        self.guardar_datos()
        return producto

    def eliminar_producto(self, id_producto: int) -> bool:
        for i, p in enumerate(self.productos):
            if p.id == id_producto:
                del self.productos[i]
                self.guardar_datos()
                return True
        return False

    def obtener_estadisticas(self) -> dict:
        if not self.productos:
            return {}

        total_unidades = sum(p.stock for p in self.productos)
        valor_inventario = sum(p.precio * p.stock for p in self.productos)
        precio_promedio = sum(p.precio for p in self.productos) / len(self.productos)
        mas_caro = max(self.productos, key=lambda p: p.precio)
        mas_barato = min(self.productos, key=lambda p: p.precio)

        return {
            "total_items": len(self.productos),
            "total_unidades": total_unidades,
            "valor_total": valor_inventario,
            "precio_promedio": precio_promedio,
            "mas_caro": mas_caro,
            "mas_barato": mas_barato,
        }


# --- FUNCIONES DE INTERFAZ Y VALIDACIÓN ---
def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pedir_float(mensaje: str) -> float:
    while True:
        try:
            valor = float(input(mensaje).strip())
            if valor < 0:
                print("¡ERROR! El valor no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print("¡ERROR! Entrada inválida. Ingrese un número decimal/entero válido.")


def pedir_int(mensaje: str) -> int:
    while True:
        try:
            valor = int(input(mensaje).strip())
            if valor < 0:
                print("¡ERROR! El valor no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print("¡ERROR! Entrada inválida. Ingrese un número entero válido.")


# --- FLUJO PRINCIPAL DE LA APLICACIÓN ---
def main():
    gestor = GestorInventario()

    while True:
        print("\n========================================")
        print("   GESTOR DE INVENTARIO PROFESIONAL")
        print("========================================")
        print("1. Ver inventario completo")
        print("2. Agregar nuevo producto")
        print("3. Eliminar producto")
        print("4. Ver estadísticas del inventario")
        print("5. Salir")
        print("----------------------------------------")

        opcion = input("Seleccione una opción (1-5): ").strip()

        if opcion == "1":
            limpiar_pantalla()
            print("\n==========================================================================================")
            print("                                 INVENTARIO DE PRODUCTOS")
            print("==========================================================================================")
            if not gestor.productos:
                print("El inventario está completamente vacío.")
            else:
                for p in gestor.productos:
                    print(
                        f"ID: {p.id:<3} | Nombre: {p.nombre:<18} | Categoría: {p.categoria:<12} "
                        f"| Precio: ${p.precio:<8.2f} | Stock: {p.stock:<4} u. | Fecha: {p.fecha_creacion}"
                    )
            print("==========================================================================================")
            input("\nPresione Enter para continuar...")

        elif opcion == "2":
            limpiar_pantalla()
            print("\n--- AGREGAR PRODUCTO ---")
            nombre = input("Nombre del producto: ").strip()
            if not nombre:
                print("¡ERROR! El nombre no puede estar vacío.")
                continue
            categoria = input("Categoría: ").strip() or "General"
            precio = pedir_float("Precio ($): ")
            stock = pedir_int("Cantidad en stock: ")

            prod = gestor.agregar_producto(nombre, categoria, precio, stock)
            print(f"\n¡Listo! Producto '{prod.nombre}' agregado correctamente (ID: {prod.id}).")
            input("\nPresione Enter para continuar...")

        elif opcion == "3":
            limpiar_pantalla()
            id_eliminar = pedir_int("\nIngrese el ID del producto a eliminar: ")
            if gestor.eliminar_producto(id_eliminar):
                print(f"¡Listo! Producto con ID {id_eliminar} eliminado correctamente.")
            else:
                print("¡ERROR! No existe ningún producto con ese ID.")
            input("\nPresione Enter para continuar...")

        elif opcion == "4":
            limpiar_pantalla()
            stats = gestor.obtener_estadisticas()
            print("\n--- ESTADÍSTICAS DEL INVENTARIO ---")
            if not stats:
                print("No hay datos suficientes en el inventario.")
            else:
                print(f"- Variedad de productos registrados: {stats['total_items']}")
                print(f"- Unidades totales acumuladas:      {stats['total_unidades']}")
                print(f"- Valoración total del inventario:  ${stats['valor_total']:.2f}")
                print(f"- Precio promedio por producto:     ${stats['precio_promedio']:.2f}")
                print(f"- Producto más caro:               {stats['mas_caro'].nombre} (${stats['mas_caro'].precio:.2f})")
                print(f"- Producto más barato:             {stats['mas_barato'].nombre} (${stats['mas_barato'].precio:.2f})")
            input("\nPresione Enter para continuar...")

        elif opcion == "5":
            print("\n¡Guardando cambios y saliendo...")
            break
        else:
            print("¡ERROR! Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()