#----------------------------------------------------------
# Model: cleanModel.py
# Date: 08-Nov-2024
# Authors:
#           A01749581 Mariana Balderrábano Aguilar
#           A01750911 Yael Michel García López 
#----------------------------------------------------------
import mesa

def calculate_clean_percentage(model):
    """Calculates the percentage of clean cells after the simulation."""
    return (model.areaGrid - model.dirtyCells) * 100 / model.areaGrid

def calculate_total_moves(model):
    """Calculates the total number of moves made by the agents."""
    return sum([agent.moves for agent in model.schedule.agents])

def calculate_total_time(model):
    """Gets the total time elapsed in the simulation."""
    return model.schedule.time

class CleaningModel(mesa.Model):
    """Cleaning simulation model."""

    def __init__(self, numAgents, gridWidth, gridHeight, maxTime, dirtyPercentage):
        super().__init__()
        self.numAgents = numAgents
        self.grid = mesa.space.MultiGrid(gridWidth, gridHeight, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        self.areaGrid = gridWidth * gridHeight
        self.dirtyCells = int(self.areaGrid * (dirtyPercentage/100))
        self.maxTime = maxTime
        self.time = 0

        # Create cleaning agents
        for i in range(self.numAgents):
            cleaningAgent = CleaningAgent(i, self)
            self.schedule.add(cleaningAgent)
            self.grid.place_agent(cleaningAgent, (1, 1))

        # Create dirty cells
        for i in range(self.dirtyCells):
            dirtyCell = DirtyCell(i, self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(dirtyCell, (x, y))

        # Collect data from the simulation
        self.dataCollector = mesa.datacollection.DataCollector(
            model_reporters={"Total time": calculate_total_time, "Total moves": calculate_total_moves, "Clean cell percentage": calculate_clean_percentage},
            agent_reporters={"Moves": "moves", "Cleaned cells": "cleanedCells"}
        )

    def step(self):
        """Executes a step in the simulation."""
        self.time += 1
        self.schedule.step()
        self.dataCollector.collect(self)

        # Stop the simulation if there are no dirty cells or the maximum time is reached
        if self.dirtyCells == 0 or self.time >= self.maxTime:
            self.running = False


class CleaningAgent(mesa.Agent):
    """Cleaning agent."""

    def __init__(self, uniqueId, model):
        super().__init__(uniqueId, model)
        self.moves = 0
        self.cleanedCells = 0

    def move(self):
        """Moves the agent to a new position."""
        possibleSteps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        
        filteredSteps = []
        for step in possibleSteps:
            cellContent = self.model.grid.get_cell_list_contents([step])
            if not any(isinstance(agent, CleaningAgent) for agent in cellContent):
                filteredSteps.append(step)
        possibleSteps = filteredSteps
        
        if possibleSteps:
            newPos = self.random.choice(possibleSteps)
            self.model.grid.move_agent(self, newPos)
            self.moves += 1
    
    def clean(self):
        """Cleans the cell the agent is in."""
        cellContent = self.model.grid.get_cell_list_contents([self.pos])
        for item in cellContent:
            if isinstance(item, DirtyCell):
                self.model.grid.remove_agent(item)
                self.cleanedCells += 1
                self.model.dirtyCells -= 1

    def step(self):
        """Executes a step for the agent."""
        self.move()
        self.clean()
        
class DirtyCell(mesa.Agent):
    """Dirty cell."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

