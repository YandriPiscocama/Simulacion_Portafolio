from model.modelo_deterministico import ModeloDeterministico
from model.modelo_discreto import ModeloDiscreto
from model.modelo_estocastico import ModeloEstocastico
from model.modelo_continuo import ModeloContinuo


class SimulacionController:

    def __init__(
        self,
        poblacion_inicial,
        tasa_crecimiento,
        tiempo,
        sigma,
        dt
    ):
        self.poblacion_inicial = poblacion_inicial
        self.tasa_crecimiento = tasa_crecimiento
        self.tiempo = tiempo
        self.sigma = sigma
        self.dt = dt

        self.validar_parametros()

        self.modelo_deterministico = ModeloDeterministico()
        self.modelo_discreto = ModeloDiscreto()
        self.modelo_estocastico = ModeloEstocastico()
        self.modelo_continuo = ModeloContinuo()

    def validar_parametros(self):
        if self.poblacion_inicial < 0:
            raise ValueError(
                "La población inicial no puede ser negativa."
            )

        if self.tiempo < 0:
            raise ValueError(
                "El tiempo no puede ser negativo."
            )

        if self.sigma < 0:
            raise ValueError(
                "Sigma no puede ser negativo."
            )

        if self.dt <= 0:
            raise ValueError(
                "dt debe ser mayor que cero."
            )

    def ejecutar_simulacion(self):

        tiempo_det, poblacion_det = (
            self.modelo_deterministico.simular(
                self.poblacion_inicial,
                self.tasa_crecimiento,
                self.tiempo
            )
        )

        tiempo_dis, poblacion_dis = (
            self.modelo_discreto.simular(
                self.poblacion_inicial,
                self.tasa_crecimiento,
                self.tiempo
            )
        )

        tiempo_est, poblacion_est = (
            self.modelo_estocastico.simular(
                self.poblacion_inicial,
                self.tasa_crecimiento,
                self.sigma,
                self.tiempo
            )
        )

        tiempo_con, poblacion_con = (
            self.modelo_continuo.simular(
                self.poblacion_inicial,
                self.tasa_crecimiento,
                self.tiempo,
                self.dt
            )
        )

        resultados = {
            "deterministico": {
                "tiempo": tiempo_det,
                "poblacion": poblacion_det
            },
            "discreto": {
                "tiempo": tiempo_dis,
                "poblacion": poblacion_dis
            },
            "estocastico": {
                "tiempo": tiempo_est,
                "poblacion": poblacion_est
            },
            "continuo": {
                "tiempo": tiempo_con,
                "poblacion": poblacion_con
            }
        }

        return resultados