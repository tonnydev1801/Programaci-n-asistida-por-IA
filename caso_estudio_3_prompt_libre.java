import java.util.Arrays;

/**
 * Clase que representa a un estudiante.
 */
class Estudiante {
    private String nombre;
    private double calificacion;

    /**
     * Constructor de la clase Estudiante.
     *
     * @param nombre nombre del estudiante
     * @param calificacion calificación del estudiante
     */
    public Estudiante(String nombre, double calificacion) {
        this.nombre = nombre;
        this.calificacion = calificacion;
    }

    public String getNombre() {
        return nombre;
    }

    public double getCalificacion() {
        return calificacion;
    }

    @Override
    public String toString() {
        return "Estudiante{nombre='" + nombre + "', calificacion=" + calificacion + "}";
    }
}

/**
 * Clase utilitaria que contiene la lógica de QuickSort para ordenar estudiantes
 * por calificación de menor a mayor.
 */
class OrdenadorEstudiantes {

    /**
     * Método público para ordenar el arreglo de estudiantes.
     *
     * @param estudiantes arreglo de estudiantes
     */
    public static void quickSort(Estudiante[] estudiantes) {
        if (estudiantes == null || estudiantes.length == 0) {
            System.out.println("La lista de estudiantes está vacía. No hay nada que ordenar.");
            return;
        }

        quickSort(estudiantes, 0, estudiantes.length - 1);
    }

    /**
     * Implementación recursiva de QuickSort.
     *
     * @param estudiantes arreglo de estudiantes
     * @param inicio índice inicial
     * @param fin índice final
     */
    private static void quickSort(Estudiante[] estudiantes, int inicio, int fin) {
        if (inicio < fin) {
            int indicePivote = particionar(estudiantes, inicio, fin);

            quickSort(estudiantes, inicio, indicePivote - 1);
            quickSort(estudiantes, indicePivote + 1, fin);
        }
    }

    /**
     * Reordena el arreglo usando la calificación del último elemento como pivote.
     *
     * @param estudiantes arreglo de estudiantes
     * @param inicio índice inicial
     * @param fin índice final
     * @return posición final del pivote
     */
    private static int particionar(Estudiante[] estudiantes, int inicio, int fin) {
        double pivote = estudiantes[fin].getCalificacion();
        int i = inicio - 1;

        for (int j = inicio; j < fin; j++) {
            if (estudiantes[j].getCalificacion() <= pivote) {
                i++;
                intercambiar(estudiantes, i, j);
            }
        }

        intercambiar(estudiantes, i + 1, fin);
        return i + 1;
    }

    /**
     * Intercambia dos posiciones dentro del arreglo.
     *
     * @param estudiantes arreglo de estudiantes
     * @param i índice del primer elemento
     * @param j índice del segundo elemento
     */
    private static void intercambiar(Estudiante[] estudiantes, int i, int j) {
        Estudiante temporal = estudiantes[i];
        estudiantes[i] = estudiantes[j];
        estudiantes[j] = temporal;
    }
}

/**
 * Clase principal para probar el ordenamiento.
 */
public class Main {

    /**
     * Muestra los estudiantes en consola.
     *
     * @param titulo título de la sección
     * @param estudiantes arreglo de estudiantes
     */
    public static void mostrarEstudiantes(String titulo, Estudiante[] estudiantes) {
        System.out.println("\n" + titulo);

        if (estudiantes == null || estudiantes.length == 0) {
            System.out.println("No hay estudiantes en la lista.");
            return;
        }

        for (Estudiante estudiante : estudiantes) {
            System.out.println(estudiante);
        }
    }

    public static void main(String[] args) {
        // Se crea un arreglo con al menos ocho estudiantes y calificaciones variadas
        Estudiante[] estudiantes = {
            new Estudiante("Ana", 8.7),
            new Estudiante("Luis", 6.5),
            new Estudiante("Carlos", 9.1),
            new Estudiante("María", 7.8),
            new Estudiante("Sofía", 10.0),
            new Estudiante("Jorge", 5.9),
            new Estudiante("Elena", 8.2),
            new Estudiante("Pedro", 7.0)
        };

        // Mostrar la lista original
        mostrarEstudiantes("Lista original de estudiantes:", estudiantes);

        // Ordenar con QuickSort recursivo
        OrdenadorEstudiantes.quickSort(estudiantes);

        // Mostrar la lista ordenada
        mostrarEstudiantes("Lista ordenada por calificación:", estudiantes);

        // Ejemplo opcional para validar lista vacía
        Estudiante[] listaVacia = {};
        mostrarEstudiantes("Prueba con lista vacía:", listaVacia);
        OrdenadorEstudiantes.quickSort(listaVacia);
    }
}
