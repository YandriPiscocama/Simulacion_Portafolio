import matplotlib.pyplot as plt


class VistaSimulacion:

    def graficar_modelo(self, tiempo, poblacion, nombre_modelo):
        plt.figure(figsize=(8, 5))

        plt.plot(
            tiempo,
            poblacion,
            marker="o",
            label=nombre_modelo
        )

        plt.title(nombre_modelo)
        plt.xlabel("Tiempo")
        plt.ylabel("Población")

        plt.grid(True, alpha=0.3)
        plt.legend()

        plt.tight_layout()
        plt.show()

    def graficar_comparacion(self, resultados):
        plt.figure(figsize=(9, 6))

        for nombre, resultado in resultados.items():
            plt.plot(
                resultado["tiempo"],
                resultado["poblacion"],
                marker="o",
                label=nombre.capitalize()
            )

        plt.title("Comparación de modelos de crecimiento poblacional")
        plt.xlabel("Tiempo")
        plt.ylabel("Población")

        plt.grid(True, alpha=0.3)
        plt.legend()

        plt.tight_layout()
        plt.show()

    def mostrar_graficas(self, resultados):

        self.graficar_modelo(
            resultados["deterministico"]["tiempo"],
            resultados["deterministico"]["poblacion"],
            "Modelo determinístico"
        )

        self.graficar_modelo(
            resultados["discreto"]["tiempo"],
            resultados["discreto"]["poblacion"],
            "Modelo discreto"
        )

        self.graficar_modelo(
            resultados["estocastico"]["tiempo"],
            resultados["estocastico"]["poblacion"],
            "Modelo estocástico"
        )

        self.graficar_modelo(
            resultados["continuo"]["tiempo"],
            resultados["continuo"]["poblacion"],
            "Modelo continuo mediante Euler"
        )

        self.graficar_comparacion(resultados)