import java.util.ArrayList;
import java.util.List;

/**
 * Clase que representa un producto dentro del inventario.
 */
class Producto {
    private String nombre;
    private double precio;
    private int cantidad;

    /**
     * Constructor del producto.
     * Valida que el nombre no esté vacío y que precio/cantidad no sean negativos.
     */
    public Producto(String nombre, double precio, int cantidad) {
        setNombre(nombre);
        setPrecio(precio);
        setCantidad(cantidad);
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

    public void setNombre(String nombre) {
        if (nombre == null || nombre.trim().isEmpty()) {
            throw new IllegalArgumentException("El nombre del producto no puede estar vacío.");
        }
        this.nombre = nombre.trim();
    }

    public void setPrecio(double precio) {
        if (precio < 0) {
            throw new IllegalArgumentException("El precio no puede ser negativo.");
        }
        this.precio = precio;
    }

    public void setCantidad(int cantidad) {
        if (cantidad < 0) {
            throw new IllegalArgumentException("La cantidad no puede ser negativa.");
        }
        this.cantidad = cantidad;
    }

    /**
     * Devuelve la información del producto en formato legible.
     */
    @Override
    public String toString() {
        return "Producto{" +
                "nombre='" + nombre + '\'' +
                ", precio=$" + String.format("%.2f", precio) +
                ", cantidad=" + cantidad +
                '}';
    }
}

/**
 * Clase que gestiona el inventario de productos.
 */
class Inventario {
    private final List<Producto> productos;

    public Inventario() {
        this.productos = new ArrayList<>();
    }

    /**
     * Registra un nuevo producto en el inventario.
     * Si ya existe un producto con el mismo nombre, no lo agrega.
     */
    public void registrarProducto(Producto producto) {
        if (buscarProducto(producto.getNombre()) != null) {
            System.out.println("No se pudo registrar: ya existe un producto con el nombre \"" 
                    + producto.getNombre() + "\".");
            return;
        }

        productos.add(producto);
        System.out.println("Producto registrado correctamente: " + producto.getNombre());
    }

    /**
     * Muestra todos los productos del inventario.
     */
    public void mostrarInventario() {
        System.out.println("\n=== INVENTARIO COMPLETO ===");

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
     */
    public Producto buscarProducto(String nombre) {
        for (Producto producto : productos) {
            if (producto.getNombre().equalsIgnoreCase(nombre.trim())) {
                return producto;
            }
        }
        return null;
    }

    /**
     * Busca y muestra un producto por nombre.
     */
    public void mostrarProductoBuscado(String nombre) {
        Producto producto = buscarProducto(nombre);

        if (producto == null) {
            System.out.println("No existe un producto con el nombre \"" + nombre + "\".");
        } else {
            System.out.println("Producto encontrado: " + producto);
        }
    }

    /**
     * Actualiza la cantidad de un producto existente.
     * Valida que la nueva cantidad no sea negativa.
     */
    public void actualizarCantidad(String nombre, int nuevaCantidad) {
        if (nuevaCantidad < 0) {
            System.out.println("Error: la cantidad no puede ser negativa.");
            return;
        }

        Producto producto = buscarProducto(nombre);

        if (producto == null) {
            System.out.println("No se puede actualizar: el producto \"" + nombre + "\" no existe.");
        } else {
            producto.setCantidad(nuevaCantidad);
            System.out.println("Cantidad actualizada correctamente para \"" 
                    + producto.getNombre() + "\". Nueva cantidad: " + nuevaCantidad);
        }
    }
}

/**
 * Clase principal para probar el sistema de inventario.
 */
public class Main {
    public static void main(String[] args) {
        Inventario inventario = new Inventario();

        try {
            // Se registran al menos cinco productos de prueba.
            inventario.registrarProducto(new Producto("Laptop", 15500.99, 8));
            inventario.registrarProducto(new Producto("Mouse", 250.50, 20));
            inventario.registrarProducto(new Producto("Teclado", 699.99, 12));
            inventario.registrarProducto(new Producto("Monitor", 3200.00, 6));
            inventario.registrarProducto(new Producto("Impresora", 2899.90, 4));

            // Mostrar inventario inicial.
            inventario.mostrarInventario();

            // Buscar productos.
            System.out.println("\n=== BÚSQUEDA DE PRODUCTOS ===");
            inventario.mostrarProductoBuscado("Mouse");
            inventario.mostrarProductoBuscado("Tablet");

            // Actualizar cantidad de un producto existente.
            System.out.println("\n=== ACTUALIZACIÓN DE CANTIDAD ===");
            inventario.actualizarCantidad("Monitor", 10);

            // Intentar actualizar un producto inexistente.
            inventario.actualizarCantidad("Tablet", 5);

            // Intentar actualizar con cantidad negativa.
            inventario.actualizarCantidad("Laptop", -3);

            // Mostrar inventario final.
            inventario.mostrarInventario();

            // Ejemplo de validación al crear un producto inválido.
            // Descomenta estas líneas para probar la validación:
            // inventario.registrarProducto(new Producto("Cámara", -1500.0, 3));
            // inventario.registrarProducto(new Producto("Bocina", 800.0, -2));

        } catch (IllegalArgumentException e) {
            System.out.println("Error al crear producto: " + e.getMessage());
        }
    }
}
