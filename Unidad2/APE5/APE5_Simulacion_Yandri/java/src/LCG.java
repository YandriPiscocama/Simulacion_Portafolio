import java.io.BufferedWriter;
import java.io.IOException;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public final class LCG {
    private static final long A = 1664525L, C = 1013904223L, M = 1L << 32;
    private static final int N = 10000;

    public static void export(long seed, Path output) throws IOException {
        if (seed < 0 || seed >= M) {
            throw new IllegalArgumentException("La semilla debe pertenecer a [0, m)");
        }
        Files.createDirectories(output.toAbsolutePath().getParent());
        long state = seed;
        BigDecimal modulus = BigDecimal.valueOf(M);
        try (BufferedWriter writer = Files.newBufferedWriter(output, StandardCharsets.UTF_8)) {
            writer.write("indice,estado,uniforme\n");
            for (int index = 1; index <= N; index++) {
                // A*(M-1)+C es menor que 2^53 y cabe en long.
                state = (A * state + C) % M;
                String normalized = BigDecimal.valueOf(state).divide(modulus).setScale(32).toPlainString();
                writer.write(index + "," + state + "," + normalized + "\n");
            }
        }
    }

    public static void main(String[] args) throws IOException {
        if (args.length != 2) {
            throw new IllegalArgumentException("Uso: LCG SEMILLA ARCHIVO_CSV");
        }
        export(Long.parseLong(args[0]), Paths.get(args[1]));
    }
}
