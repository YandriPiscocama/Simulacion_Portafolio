import java.math.BigInteger;
import java.util.Arrays;

public final class LCGTest {
    private static BigInteger b(long n) { return BigInteger.valueOf(n); }
    public static void main(String[] args) {
        BigInteger x = b(1);
        long[] expected = {8, 11, 10, 5, 12};
        for (long value : expected) {
            x = LCG.next(x, b(5), b(3), b(16));
            if (!x.equals(b(value))) throw new AssertionError("Estado inesperado: " + x);
        }
        if (!LCG.normalized(b(8), b(16)).equals("0.50000000000000000")) throw new AssertionError("Normalización");
        try {
            LCG.validate(b(16), b(5), b(3), b(16), 1);
            throw new AssertionError("Semilla inválida aceptada");
        } catch (IllegalArgumentException expectedException) { }
        // Producto que desbordaría long, contrastado con un cálculo conocido.
        BigInteger huge = new BigInteger("100000000000000000000");
        if (!LCG.next(huge.subtract(b(1)), huge.subtract(b(1)), b(1), huge).equals(b(2)))
            throw new AssertionError("Aritmética grande");
        System.out.println("LCGTest: correcto");
    }
}
