from controller.simulacion_controller import SimulacionController
from view.vista_simulacion import VistaSimulacion


def main():

    controlador = SimulacionController(
        poblacion_inicial=1000,
        tasa_crecimiento=0.1,
        tiempo=6,
        sigma=50,
        dt=0.5
    )

    resultados = controlador.ejecutar_simulacion()

    vista = VistaSimulacion()

    vista.mostrar_graficas(resultados)


if __name__ == "__main__":
    main()