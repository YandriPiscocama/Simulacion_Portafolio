class DatoClimatico:
    def __init__(self, hora, humedad, nubosidad, temperatura):
        self.hora = hora
        self.humedad = humedad
        self.nubosidad = nubosidad
        self.temperatura = temperatura

    def obtener_humedad_normalizada(self):
        return self.humedad / 100

    def obtener_nubosidad_normalizada(self):
        return self.nubosidad / 100

    