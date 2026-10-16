import matplotlib

matplotlib.use("TkAgg")

import matplotlib.pyplot as plt


class VistaSimulacion:

    def mostrar_resultados(self, resultados):
        print("\nRESULTADOS DE LA SIMULACIÓN\n")

        encabezado = (
            f"{'Hora':<8}"
            f"{'Hum':<8}"
            f"{'Nub':<8}"
            f"{'Temp':<8}"
            f"{'H':<8}"
            f"{'N':<8}"
            f"{'Tf':<8}"
            f"{'Índice':<10}"
            f"{'Estado'}"
        )

        print(encabezado)
        print("-" * 85)

        for resultado in resultados:
            print(
                f"{resultado['hora']:<8}"
                f"{resultado['humedad']:<8}"
                f"{resultado['nubosidad']:<8}"
                f"{resultado['temperatura']:<8}"
                f"{resultado['h']:<8.2f}"
                f"{resultado['n']:<8.2f}"
                f"{resultado['tf']:<8.2f}"
                f"{resultado['indice']:<10.3f}"
                f"{resultado['estado']}"
            )

    def graficar_comparacion(
        self,
        resultados_original,
        resultados_ajustado
    ):
        horas = [
            r["hora"]
            for r in resultados_original
        ]

        indices_original = [
            r["indice"]
            for r in resultados_original
        ]

        indices_ajustado = [
            r["indice"]
            for r in resultados_ajustado
        ]

        plt.figure(figsize=(10, 5))

        plt.plot(
            horas,
            indices_original,
            marker="o",
            label="Modelo original (0.5, 0.3, 0.2)"
        )

        plt.plot(
            horas,
            indices_ajustado,
            marker="o",
            label="Modelo ajustado (0.6, 0.25, 0.15)"
        )

        plt.axhline(
            y=0.40,
            linestyle="--",
            label="Baja posibilidad"
        )

        plt.axhline(
            y=0.60,
            linestyle="--",
            label="Lluvia probable"
        )

        plt.axhline(
            y=0.75,
            linestyle="--",
            label="Lluvia"
        )

        plt.xlabel("Hora")
        plt.ylabel("Índice de lluvia")
        plt.title("Comparación del modelo original y ajustado")

        plt.grid(True)
        plt.legend()

        plt.show()