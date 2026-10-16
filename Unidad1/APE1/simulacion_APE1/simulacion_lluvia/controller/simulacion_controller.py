from model.dato_climatico import DatoClimatico
from model.modelo_lluvia import ModeloLluvia


class SimulacionController:

    def __init__(self, modelo=None):
        if modelo is None:
            modelo = ModeloLluvia()

        self.modelo = modelo

    def obtener_datos_iniciales(self):
        return [
            DatoClimatico("06:00", 65, 40, 14),
            DatoClimatico("08:00", 70, 50, 16),
            DatoClimatico("10:00", 68, 45, 18),
            DatoClimatico("12:00", 60, 30, 22),
            DatoClimatico("14:00", 75, 70, 20),
            DatoClimatico("16:00", 85, 85, 18),
            DatoClimatico("18:00", 92, 95, 16),
            DatoClimatico("20:00", 88, 90, 17),
            DatoClimatico("22:00", 80, 75, 15)
        ]

    def ejecutar_simulacion(self):
        datos = self.obtener_datos_iniciales()
        resultados = []

        for dato in datos:
            h = dato.obtener_humedad_normalizada()
            n = dato.obtener_nubosidad_normalizada()

            tf = self.modelo.calcular_factor_temperatura(
                dato.temperatura
            )

            indice = self.modelo.calcular_indice(
                h,
                n,
                tf
            )

            estado = self.modelo.clasificar(
                indice
            )

            resultado = {
                "hora": dato.hora,
                "humedad": dato.humedad,
                "nubosidad": dato.nubosidad,
                "temperatura": dato.temperatura,
                "h": h,
                "n": n,
                "tf": tf,
                "indice": indice,
                "estado": estado
            }

            resultados.append(resultado)

        return resultados