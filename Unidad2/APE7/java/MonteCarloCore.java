/** Núcleo matemático del experimento: LCG, conteo y estimación, sin E/S. */
final class MonteCarloCore {
    private static final long MASK = 0xFFFFFFFFL;
    private static final double MODULUS = 4294967296.0;
    private static final long MULTIPLIER = 1664525L;
    private static final long INCREMENT = 1013904223L;

    private MonteCarloCore() {
    }

    static final class LCG {
        private long state;

        LCG(long seed) {
            state = seed & MASK;
        }

        long nextState() {
            state = (MULTIPLIER * state + INCREMENT) & MASK;
            return state;
        }

        double nextUniform() {
            return nextState() / MODULUS;
        }
    }

    static long countInside(long n, long seed) {
        LCG generator = new LCG(seed);
        long nc = 0;
        for (long i = 0; i < n; i++) {
            double x = generator.nextUniform();
            double y = generator.nextUniform();
            if (x * x + y * y <= 1.0) {
                nc++;
            }
        }
        return nc;
    }

    static double estimatePi(long nc, long n) {
        return 4.0 * nc / n;
    }

    static double absoluteError(double piEstimate) {
        return Math.abs(piEstimate - Math.PI);
    }
}
