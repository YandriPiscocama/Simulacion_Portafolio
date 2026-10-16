import numpy as np


class ModeloContinuo:

    def simular(
        self,
        poblacion_inicial,
        tasa_crecimiento,
        tiempo,
        dt
    ):
        tiempos = np.arange(
            0,
            tiempo + dt,
            dt
        )

        poblacion = [poblacion_inicial]

        for i in range(1, len(tiempos)):
            poblacion_actual = poblacion[-1]

            cambio = tasa_crecimiento * poblacion_actual

            nueva_poblacion = (
                poblacion_actual
                + dt * cambio
            )

            poblacion.append(nueva_poblacion)

        return tiempos, poblacion