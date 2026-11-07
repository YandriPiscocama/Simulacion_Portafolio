import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;

/** Estimación de pi por Monte Carlo; ampliación propuesta para completar la tabla de la guía. */
public final class EstimacionPi {
    private static final long SEED = 42L;
    private static final long A = 1664525L;
    private static final long C = 1013904223L;
    private static final long M = 4294967296L;
    private static final int[] SIZES = {1000, 10000, 100000, 1000000};

    private EstimacionPi() {}

    public static final class Result {
        public final long inside;
        public final double estimate;
        Result(long inside, double estimate) { this.inside = inside; this.estimate = estimate; }
    }

    public static Result estimatePi(int n) {
        if (n < 1) throw new IllegalArgumentException("n debe ser positivo");
        long x = SEED;
        long inside = 0;
        double modulus = (double) M;
        for (int i = 0; i < n; i++) {
            // Para A, A*x+C <= 1,665,255*(2^32-1)+1,013,902,233 < Long.MAX_VALUE.
            x = (A * x + C) % M;
            double px = x / modulus;
            x = (A * x + C) % M;
            double py = x / modulus;
            if (px * px + py * py <= 1.0) inside++;
        }
        return new Result(inside, 4.0 * inside / n);
    }

    private static double median(double[] values) {
        double[] sorted = values.clone();
        Arrays.sort(sorted);
        return sorted[sorted.length / 2];
    }

    private static double[] measured(int n, int repetitions) {
        estimatePi(Math.min(n, 1000)); // calentamiento fuera de las mediciones
        double[] samples = new double[repetitions];
        for (int i = 0; i < repetitions; i++) {
            long start = System.nanoTime();
            estimatePi(n);
            samples[i] = (System.nanoTime() - start) / 1_000_000_000.0;
        }
        return samples;
    }

    public static void main(String[] args) throws IOException {
        String output = "results/tables/comparacion_pi_java.csv";
        String countsOutput = null;
        int repetitions = 5;
        for (int i = 0; i < args.length; i += 2) {
            if (i + 1 >= args.length) throw new IllegalArgumentException("Falta el valor de " + args[i]);
            if ("--output".equals(args[i])) output = args[i + 1];
            else if ("--counts-output".equals(args[i])) countsOutput = args[i + 1];
            else if ("--repetitions".equals(args[i])) repetitions = Integer.parseInt(args[i + 1]);
            else throw new IllegalArgumentException("Opción desconocida: " + args[i]);
        }
        if (repetitions < 1) throw new IllegalArgumentException("repetitions debe ser positivo");
        Path outputPath = Paths.get(output);
        if (outputPath.getParent() != null) Files.createDirectories(outputPath.getParent());
        Path countsPath = countsOutput == null ? null : Paths.get(countsOutput);
        if (countsPath != null && countsPath.getParent() != null) Files.createDirectories(countsPath.getParent());
        try (BufferedWriter writer = Files.newBufferedWriter(outputPath, StandardCharsets.UTF_8)) {
            writer.write("N,pi_estimado,error_absoluto,tiempo_python_s,tiempo_java_s\n");
            try (BufferedWriter countWriter = countsPath == null ? null : Files.newBufferedWriter(countsPath, StandardCharsets.UTF_8)) {
                if (countWriter != null) countWriter.write("N,puntos_dentro\n");
                System.out.println("N,pi_estimado,error_absoluto,tiempo_java_s");
                for (int n : SIZES) {
                    double[] times = measured(n, repetitions);
                    Result result = estimatePi(n);
                    double error = Math.abs(result.estimate - Math.PI);
                    writer.write(n + "," + Double.toString(result.estimate) + "," + Double.toString(error) + ",," + Double.toString(median(times)) + "\n");
                    if (countWriter != null) countWriter.write(n + "," + result.inside + "\n");
                    System.out.println(n + "," + Double.toString(result.estimate) + "," + Double.toString(error) + "," + Double.toString(median(times)));
                }
            }
        }
    }
}
