class ModeloLluvia:

    def __init__(
        self,
        peso_humedad=0.5,
        peso_nubosidad=0.3,
        peso_temperatura=0.2
    ):
        self.peso_humedad = peso_humedad
        self.peso_nubosidad = peso_nubosidad
        self.peso_temperatura = peso_temperatura

        self.validar_pesos()

    def validar_pesos(self):
        suma = (
            self.peso_humedad
            + self.peso_nubosidad
            + self.peso_temperatura
        )

        if abs(suma - 1.0) > 1e-9:
            raise ValueError(
                "La suma de los pesos debe ser igual a 1."
            )

    def calcular_factor_temperatura(self, temperatura):
        # Casos extremos
        if temperatura <= 10:
            return 1.00

        if temperatura >= 28:
            return 0.10

        # Valores establecidos en la guía
        factores = {
            10: 1.00,
            12: 0.90,
            14: 0.80,
            16: 0.70,
            18: 0.60,
            20: 0.50,
            22: 0.40,
            24: 0.30,
            26: 0.20,
            28: 0.10
        }

        # Si existe exactamente en la tabla
        if temperatura in factores:
            return factores[temperatura]

        # Interpolación para temperaturas como 15 o 17
        temperaturas = sorted(factores.keys())

        for i in range(len(temperaturas) - 1):
            temp_inferior = temperaturas[i]
            temp_superior = temperaturas[i + 1]

            if temp_inferior < temperatura < temp_superior:
                tf_inferior = factores[temp_inferior]
                tf_superior = factores[temp_superior]

                proporcion = (
                    (temperatura - temp_inferior)
                    / (temp_superior - temp_inferior)
                )

                tf = tf_inferior + proporcion * (
                    tf_superior - tf_inferior
                )

                return tf

    def calcular_indice(self, h, n, tf):
        indice = (
            self.peso_humedad * h
            + self.peso_nubosidad * n
            + self.peso_temperatura * tf
        )

        return indice

    def clasificar(self, indice):
        if indice < 0.40:
            return "Sin lluvia"

        elif indice < 0.60:
            return "Baja posibilidad"

        elif indice < 0.75:
            return "Lluvia probable"

        else:
            return "Lluvia"