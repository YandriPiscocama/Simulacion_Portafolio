import java.io.BufferedWriter;
import java.io.IOException;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.math.RoundingMode;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

public final class LCG {
    private LCG() {}

    public static void validate(BigInteger seed, BigInteger a, BigInteger c, BigInteger m, int n) {
        if (m.compareTo(BigInteger.ONE) <= 0 || n < 1 || seed.signum() < 0 ||
            a.signum() < 0 || c.signum() < 0 || seed.compareTo(m) >= 0 ||
            a.compareTo(m) >= 0 || c.compareTo(m) >= 0) {
            throw new IllegalArgumentException("Se requiere m > 1, 0 <= semilla,a,c < m y n >= 1");
        }
    }

    public static BigInteger next(BigInteger x, BigInteger a, BigInteger c, BigInteger m) {
        return a.multiply(x).add(c).mod(m);
    }

    public static String normalized(BigInteger x, BigInteger m) {
        return new BigDecimal(x).divide(new BigDecimal(m), Math.max(17, m.toString().length() + 1), RoundingMode.HALF_EVEN).toPlainString();
    }

    public static void main(String[] args) {
        try {
            String seed = "42", a = "1664525", c = "1013904223", m = "4294967296", n = "10000";
            String output = "data/lcg_java.csv";
            for (int i = 0; i < args.length; i += 2) {
                if (i + 1 >= args.length) throw new IllegalArgumentException("Falta el valor de " + args[i]);
                switch (args[i]) {
                    case "--seed": seed = args[i + 1]; break;
                    case "--a": a = args[i + 1]; break;
                    case "--c": c = args[i + 1]; break;
                    case "--m": m = args[i + 1]; break;
                    case "--n": n = args[i + 1]; break;
                    case "--output": output = args[i + 1]; break;
                    default: throw new IllegalArgumentException("Opción desconocida: " + args[i]);
                }
            }
            BigInteger x = new BigInteger(seed), multiplier = new BigInteger(a);
            BigInteger increment = new BigInteger(c), modulus = new BigInteger(m);
            int count = Integer.parseInt(n);
            validate(x, multiplier, increment, modulus, count);
            try (BufferedWriter writer = Files.newBufferedWriter(Paths.get(output), StandardCharsets.UTF_8)) {
                String header = "indice,estado,uniforme";
                writer.write(header + "\n");
                System.out.println(header);
                for (int i = 0; i < count; i++) {
                    x = next(x, multiplier, increment, modulus);
                    String row = ((long) i + 1) + "," + x + "," + normalized(x, modulus);
                    writer.write(row + "\n");
                    System.out.println(row);
                }
            }
        } catch (IllegalArgumentException | IOException ex) {
            System.err.println("Error: " + ex.getMessage());
            System.exit(1);
        }
    }
}
