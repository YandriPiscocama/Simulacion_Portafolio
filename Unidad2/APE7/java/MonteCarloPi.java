public final class MonteCarloPi {
    private static volatile long warmupSink;

    private MonteCarloPi() {
    }

    public static void main(String[] args) {
        if (args.length < 1 || args.length > 2) {
            System.err.println("Error: uso: java MonteCarloPi N [semilla]");
            System.exit(2);
        }

        final long n;
        final long seed;
        try {
            n = Long.parseLong(args[0]);
            seed = args.length == 2 ? Long.parseLong(args[1]) : 42L;
        } catch (NumberFormatException ex) {
            System.err.println("Error: N y semilla deben ser enteros con signo de 64 bits");
            System.exit(2);
            return;
        }
        if (n <= 0) {
            System.err.println("Error: N debe ser un entero positivo");
            System.exit(2);
        }

        MonteCarloCore.LCG probe = new MonteCarloCore.LCG(seed);
        long[] firstStates = {probe.nextState(), probe.nextState(), probe.nextState()};

        // La JVM se calienta fuera del tramo cronometrado. Su resultado se descarta.
        warmupSink = MonteCarloCore.countInside(100_000L, seed);
        long startNs = System.nanoTime();
        long nc = MonteCarloCore.countInside(n, seed);
        long elapsedNs = System.nanoTime() - startNs;

        double piEstimate = MonteCarloCore.estimatePi(nc, n);
        double absoluteError = MonteCarloCore.absoluteError(piEstimate);
        System.out.println("n=" + n);
        System.out.println("semilla=" + seed);
        for (int i = 0; i < firstStates.length; i++) {
            System.out.println("estado_" + (i + 1) + "=" + firstStates[i]);
        }
        System.out.println("nc=" + nc);
        System.out.println("pi_estimado=" + piEstimate);
        System.out.println("error_absoluto=" + absoluteError);
        System.out.printf(java.util.Locale.ROOT, "tiempo_ms=%.6f%n", elapsedNs / 1_000_000.0);
    }
}
