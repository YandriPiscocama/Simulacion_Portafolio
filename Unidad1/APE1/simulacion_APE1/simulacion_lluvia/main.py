from controller.simulacion_controller import SimulacionController
from model.modelo_lluvia import ModeloLluvia
from view.vista_simulacion import VistaSimulacion


def main():

    vista = VistaSimulacion()
    modelo_original = ModeloLluvia(
        peso_humedad=0.5,
        peso_nubosidad=0.3,
        peso_temperatura=0.2
    )

    controlador_original = SimulacionController(
        modelo_original
    )

    resultados_original = (
        controlador_original.ejecutar_simulacion()
    )

    modelo_ajustado = ModeloLluvia(
        peso_humedad=0.6,
        peso_nubosidad=0.25,
        peso_temperatura=0.15
    )
    controlador_ajustado = SimulacionController(
        modelo_ajustado
    )

    resultados_ajustado = (
        controlador_ajustado.ejecutar_simulacion()
    )

   
    print("\nMODELO ORIGINAL")
    vista.mostrar_resultados(resultados_original)

    print("\nMODELO AJUSTADO")
    vista.mostrar_resultados(resultados_ajustado)

  
    vista.graficar_comparacion(
        resultados_original,
        resultados_ajustado
    )

if __name__ == "__main__":
    main()