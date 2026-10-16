import numpy as np


class ModeloEstocastico:

    def simular(
        self,
        poblacion_inicial,
        tasa_crecimiento,
        sigma,
        tiempo
    ):
        tiempos = list(range(tiempo + 1))
        poblacion = [poblacion_inicial]

        for periodo in range(1, tiempo + 1):
            ruido = np.random.normal(0, sigma)

            poblacion_actual = poblacion[-1]

            nueva_poblacion = (
                poblacion_actual
                + tasa_crecimiento * poblacion_actual
                + ruido
            )

            if nueva_poblacion < 0:
                nueva_poblacion = 0

            poblacion.append(nueva_poblacion)

        return tiempos, poblacion