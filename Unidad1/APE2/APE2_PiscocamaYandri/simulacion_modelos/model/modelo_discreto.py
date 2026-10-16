class ModeloDiscreto:

    def simular(self, poblacion_inicial, tasa_crecimiento, tiempo):
        tiempos = list(range(tiempo + 1))
        poblacion = [poblacion_inicial]

        for periodo in range(1, tiempo + 1):
            poblacion_actual = poblacion[-1]

            incremento = tasa_crecimiento * poblacion_actual

            nueva_poblacion = poblacion_actual + incremento

            poblacion.append(nueva_poblacion)

        return tiempos, poblacion