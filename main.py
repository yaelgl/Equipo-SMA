#----------------------------------------------------------
# Model: main.py
# Date: 08-Nov-2024
# Authors:
#           A01749581 Mariana Balderrábano Aguilar
#           A01750911 Yael Michel García López 
#----------------------------------------------------------

# Importación de módulos para la visualización y el servidor de la simulación
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

from AgenteRobot import Aspiradora  # Importa la clase del modelo principal

# Función que define cómo se visualizarán los agentes según su tipo
def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}  # Forma y tamaño base de los agentes

    if agent.type == 'Robot':
        portrayal["Color"] = "purple"  # Color para los agentes de tipo 'Robot'
        portrayal["Layer"] = 3  # Capa de visualización superior
    elif agent.type == 'Basura':
        portrayal["Color"] = "green"  # Color para los agentes de tipo 'Basura'
        portrayal["Layer"] = 2  # Capa de visualización media
    elif agent.type == 'limpio':
        portrayal["Color"] = "white"  # Color para las celdas limpias
        portrayal["Layer"] = 1  # Capa de visualización inferior
    return portrayal

# Configuración de la cuadrícula para la visualización, con 5x5 celdas de 500x500 píxeles
grid = CanvasGrid(
    agent_portrayal, 10, 10, 500, 500,  #10 y 10 son width y height, si se quieren cambiar hay que cambiarlos tambien abajo 
)

# Configuración del gráfico que muestra los pasos del modelo en el tiempo
chart = ChartModule([{'Label': 'Steps', 'Color': 'Black'}], data_collector_name='datacollector')

# Configuración del servidor para ejecutar y visualizar el modelo
server = ModularServer(
    Aspiradora,                  # Modelo principal
    [grid, chart],               # Elementos de visualización (cuadrícula y gráfico)
    "Vacuum Model",              # Título del modelo
    {"R": 1, "B": 20, "width": 10, "height": 10}  # Parámetros iniciales del modelo (robots, basura, tamaño)
)
server.port = 8521  # Puerto en el que se ejecutará el servidor

# Inicia el servidor para ejecutar el modelo en el navegador
server.launch()
