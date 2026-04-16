import java.util.ArrayList;
import java.util.List;

/**
 * Clase que representa a un estudiante con nombre y calificación.
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
}

/**
 * Clase principal que contiene la lógica del programa
 * y los métodos de ordenamiento QuickSort.
 */
public class Main {

    /**
     * Crea una lista de estudiantes de prueba.
     *
     * @return lista con al menos 8 estudiantes
     */
    public static List<Estudiante> crearListaEstudiantes() {
        List<Estudiante> lista = new ArrayList<>();

        lista.add(new Estudiante("Ana", 8.7));
        lista.add(new Estudiante("Luis", 6.5));
        lista.add(new Estudiante("Carlos", 9.1));
        lista.add(new Estudiante("María", 7.8));
        lista.add(new Estudiante("Sofía", 10.0));
        lista.add(new Estudiante("Jorge", 5.9));
        lista.add(new Estudiante("Elena", 8.2));
        lista.add(new Estudiante("Pedro", 7.0));

        return lista;
    }

    /**
     * Ordena la lista de estudiantes usando QuickSort de forma recursiva.
     *
     * @param lista lista de estudiantes
     * @param inicio índice inicial
     * @param fin índice final
     */
    public static void quickSort(List<Estudiante> lista, int inicio, int fin) {
        if (inicio < fin) {
            int pivote = particionar(lista, inicio, fin);
            quickSort(lista, inicio, pivote - 1);
            quickSort(lista, pivote + 1, fin);
        }
    }

    /**
     * Particiona la lista tomando como pivote la calificación
     * del último estudiante del segmento.
     *
     * @param lista lista de estudiantes
     * @param inicio índice inicial
     * @param fin índice final
     * @return posición final del pivote
     */
    public static int particionar(List<Estudiante> lista, int inicio, int fin) {
        double pivote = lista.get(fin).getCalificacion();
        int i = inicio - 1;

        for (int j = inicio; j < fin; j++) {
            if (lista.get(j).getCalificacion() <= pivote) {
                i++;
                intercambiar(lista, i, j);
            }
        }

        intercambiar(lista, i + 1, fin);
        return i + 1;
    }

    /**
     * Intercambia dos elementos de la lista.
     *
     * @param lista lista de estudiantes
     * @param i índice del primer elemento
     * @param j índice del segundo elemento
     */
    public static void intercambiar(List<Estudiante> lista, int i, int j) {
        Estudiante temporal = lista.get(i);
        lista.set(i, lista.get(j));
        lista.set(j, temporal);
    }

    /**
     * Muestra en consola la lista de estudiantes.
     *
     * @param lista lista de estudiantes
     */
    public static void mostrarLista(List<Estudiante> lista) {
        for (Estudiante estudiante : lista) {
            System.out.println(
                "Nombre: " + estudiante.getNombre()
                + " | Calificación: " + estudiante.getCalificacion()
            );
        }
    }

    public static void main(String[] args) {
        List<Estudiante> lista = crearListaEstudiantes();

        // Validar si la lista está vacía antes de ordenar
        if (lista.isEmpty()) {
            System.out.println("No hay estudiantes para ordenar.");
            return;
        }

        System.out.println("Lista original:");
        mostrarLista(lista);

        quickSort(lista, 0, lista.size() - 1);

        System.out.println("\nLista ordenada por calificación:");
        mostrarLista(lista);
    }
}
