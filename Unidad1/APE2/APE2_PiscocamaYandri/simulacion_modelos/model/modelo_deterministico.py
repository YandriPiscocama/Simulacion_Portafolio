import numpy as np


class ModeloDeterministico:

    def simular(self, poblacion_inicial, tasa_crecimiento, tiempo):
        tiempos = np.arange(0, tiempo + 1)
        poblacion = []  

        for t in tiempos:
            valor = poblacion_inicial * np.exp(tasa_crecimiento * t)
            poblacion.append(valor)

        return tiempos, poblacion

    