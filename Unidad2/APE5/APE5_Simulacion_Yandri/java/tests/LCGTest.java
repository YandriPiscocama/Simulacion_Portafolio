import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

public class LCGTest {
    public static void main(String[] args) throws Exception {
        Path file = Paths.get(args[0]);
        LCG.export(12345, file);
        List<String> rows = Files.readAllLines(file, StandardCharsets.UTF_8);
        if (rows.size() != 10001 || !rows.get(1).startsWith("1,87628868,")) {
            throw new AssertionError("Cantidad o primer estado incorrecto");
        }
        try {
            LCG.export(-1, file);
            throw new AssertionError("Semilla inválida aceptada");
        } catch (IllegalArgumentException expected) {
            System.out.println("LCGTest: correcto");
        }
    }
}
