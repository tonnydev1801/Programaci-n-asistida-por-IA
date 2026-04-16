import java.util.ArrayList;
import java.util.List;

/**
 * Clase que representa un producto del inventario.
 */
class Producto {
    private String nombre;
    private double precio;
    private int cantidad;

    /**
     * Constructor de la clase Producto.
     *
     * @param nombre   nombre del producto
     * @param precio   precio del producto
     * @param cantidad cantidad disponible del producto
     */
    public Producto(String nombre, double precio, int cantidad) {
        this.nombre = nombre;
        this.precio = precio;
        this.cantidad = cantidad;
    }

    public String getNombre() {
        return nombre;
    }

    public double getPrecio() {
        return precio;
    }

    public int getCantidad() {
        return cantidad;
    }

    public void setCantidad(int cantidad) {
        this.cantidad = cantidad;
    }

    /**
     * Devuelve una representación legible del producto.
     */
    @Override
    public String toString() {
        return "Nombre: " + nombre +
                " | Precio: $" + precio +
                " | Cantidad: " + cantidad;
    }
}

/**
 * Clase encargada de gestionar el inventario.
 * Aquí se implementa la lógica principal del sistema.
 */
class Inventario {
    private List<Producto> productos;

    /**
     * Constructor de la clase Inventario.
     * Inicializa la lista de productos.
     */
    public Inventario() {
        productos = new ArrayList<>();
    }

    /**
     * Agrega un producto al inventario si sus datos son válidos.
     *
     * @param producto producto a registrar
     */
    public void agregarProducto(Producto producto) {
        if (producto.getPrecio() < 0 || producto.getCantidad() < 0) {
            System.out.println("No se puede registrar un producto con valores inválidos: "
                    + producto.getNombre());
            return;
        }

        productos.add(producto);
        System.out.println("Producto registrado correctamente: " + producto.getNombre());
    }

    /**
     * Muestra todos los productos del inventario.
     */
    public void mostrarInventario() {
        if (productos.isEmpty()) {
            System.out.println("El inventario está vacío.");
            return;
        }

        for (Producto producto : productos) {
            System.out.println(producto);
        }
    }

    /**
     * Busca un producto por nombre.
     * La búsqueda no distingue entre mayúsculas y minúsculas.
     *
     * @param nombreBuscado nombre del producto a buscar
     * @return el producto encontrado o null si no existe
     */
    public Producto buscarProducto(String nombreBuscado) {
        for (Producto producto : productos) {
            if (producto.getNombre().equalsIgnoreCase(nombreBuscado)) {
                return producto;
            }
        }
        return null;
    }

    /**
     * Actualiza la cantidad de un producto existente.
     *
     * @param nombreBuscado nombre del producto
     * @param nuevaCantidad nueva cantidad a asignar
     */
    public void actualizarCantidad(String nombreBuscado, int nuevaCantidad) {
        Producto producto = buscarProducto(nombreBuscado);

        if (producto == null) {
            System.out.println("Producto no encontrado: " + nombreBuscado);
            return;
        }

        if (nuevaCantidad < 0) {
            System.out.println("Cantidad inválida. No puede ser negativa.");
            return;
        }

        producto.setCantidad(nuevaCantidad);
        System.out.println("Cantidad actualizada correctamente para el producto: "
                + producto.getNombre());
    }
}

/**
 * Clase principal del programa.
 * Aquí se crean productos de prueba y se demuestra el funcionamiento del sistema.
 */
public class Main {
    public static void main(String[] args) {
        Inventario inventario = new Inventario();

        // Se agregan al menos 5 productos de prueba
        inventario.agregarProducto(new Producto("Laptop", 15000.00, 10));
        inventario.agregarProducto(new Producto("Mouse", 250.50, 25));
        inventario.agregarProducto(new Producto("Teclado", 800.00, 15));
        inventario.agregarProducto(new Producto("Monitor", 3200.99, 8));
        inventario.agregarProducto(new Producto("Impresora", 2100.75, 5));

        // Producto inválido para probar validación
        inventario.agregarProducto(new Producto("Producto inválido", -50.0, 3));

        System.out.println("\n=== Inventario inicial ===");
        inventario.mostrarInventario();

        System.out.println("\n=== Búsqueda de producto ===");
        Producto productoBuscado = inventario.buscarProducto("Mouse");
        if (productoBuscado != null) {
            System.out.println("Producto encontrado: " + productoBuscado);
        } else {
            System.out.println("Producto no encontrado.");
        }

        System.out.println("\n=== Búsqueda de producto inexistente ===");
        Producto productoInexistente = inventario.buscarProducto("Tablet");
        if (productoInexistente != null) {
            System.out.println("Producto encontrado: " + productoInexistente);
        } else {
            System.out.println("Producto no encontrado.");
        }

        System.out.println("\n=== Actualización de cantidad ===");
        inventario.actualizarCantidad("Monitor", 12);

        System.out.println("\n=== Intento de actualización inválida ===");
        inventario.actualizarCantidad("Laptop", -4);

        System.out.println("\n=== Intento de actualizar producto inexistente ===");
        inventario.actualizarCantidad("Tablet", 7);

        System.out.println("\n=== Inventario actualizado ===");
        inventario.mostrarInventario();
    }
}
