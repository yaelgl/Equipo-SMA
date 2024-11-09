#----------------------------------------------------------
# Model: run.py
# Date: 08-Nov-2024
# Authors:
#           A01749581 Mariana Balderrábano Aguilar
#           A01750911 Yael Michel García López 
#----------------------------------------------------------

from cleanModel import mesa, CleaningModel, CleaningAgent, DirtyCell

def agent_portrayal(agent):
    """Defines the visual representation of the agents in the simulation."""
    if isinstance(agent, DirtyCell):
        return {"Shape": "plant.png", "Layer": 0, "r": 0.5}
    elif isinstance(agent, CleaningAgent):
        return {"Shape": "wall_e.png", "Layer": 1, "r": 0.5}

# Simulation charts
total_time_graph = mesa.visualization.ChartModule([{"Label": "Total time", "Color": "Green"}], data_collector_name='dataCollector')
cleaned_percentage_graph = mesa.visualization.ChartModule([{"Label": "Clean cell percentage", "Color": "Blue"}], data_collector_name='dataCollector')
total_moves_graph = mesa.visualization.ChartModule([{"Label": "Total moves", "Color": "Purple"}], data_collector_name='dataCollector')

grid_width = 7
grid_height = 20
base_canvas_size = 500

if grid_width >= grid_height:
    canvas_width = base_canvas_size
    canvas_height = int(base_canvas_size * (grid_height / grid_width))
else:
    canvas_height = base_canvas_size
    canvas_width = int(base_canvas_size * (grid_width / grid_height))

grid = mesa.visualization.CanvasGrid(agent_portrayal, grid_width, grid_height, canvas_width, canvas_height)

server = mesa.visualization.ModularServer(
    CleaningModel, [grid, total_time_graph, cleaned_percentage_graph, total_moves_graph], "Cleaning Simulation", {"numAgents": 12, "gridWidth": grid_width, "gridHeight": grid_height, "maxTime": 120, "dirtyPercentage": 30}
)
server.description = "Automated Cleaning Simulation"
server.port = 8000
server.launch()


