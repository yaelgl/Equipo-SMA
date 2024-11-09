
#----------------------------------------------------------
# Model: AgenteRobot.py
# Date: 08-Nov-2024
# Authors:
#           A01749581 Mariana Balderrábano Aguilar
#           A01750911 Yael Michel García López 
#----------------------------------------------------------


from mesa.time import RandomActivation
from mesa import Agent, Model
from mesa.datacollection import DataCollector
import time

from mesa.space import MultiGrid

start_time = time.time()  # Guarda el tiempo de inicio de la simulación
basuraRecogida = 0  # Variable para contar la cantidad de basura recogida

# Tiempo máximo de simulación en segundos
maxTime = 20

# Función para obtener el tiempo transcurrido desde el inicio de la simulación
def getTime(model):
    return time.time() - start_time

# Clase que representa al agente Robot
class AgenteRobot(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'Robot'  # Define el tipo de agente como 'Robot'
        self.basuraRecogida = 0
        self.final = False  # Indica si la simulación ha terminado

    # Método que ejecuta el paso del agente
    def step(self):
        self.move()  # Mueve el agente a una nueva posición
        self.limpioSucio()  # Verifica si la celda está limpia

    # Método para mover el agente a una posición vecina
    def move(self):
       if not self.final:
            # Obtiene las posiciones vecinas posibles
            possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                moore=True,
                include_center=True
            )
            # Selecciona una nueva posición aleatoria
            new_position = self.random.choice(possible_steps)
            self.model.grid.move_agent(self, new_position)
       else:
           print("Fin de simulación")
           print("El robot limpió:", basuraRecogida)
           pass

    # Método que verifica si la celda está limpia (sin implementación en este código)
    def limpioSucio(self):
        pass

# Clase que representa a los agentes de tipo Basura
class Agente_Basura(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = 'Basura'  # Define el tipo de agente como 'Basura'

    # Método para cambiar el tipo de agente a 'limpio' si es limpiado
    def Limpiando(self):
        global basuraRecogida
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for cellmate in cellmates:
            if cellmate.type == 'Robot':
                self.type = 'limpio'  # Cambia el estado de 'Basura' a 'limpio'

    # Método que ejecuta el paso del agente de basura
    def step(self):
        self.Limpiando()

# Clase principal del modelo de la aspiradora
class Aspiradora(Model):
    def __init__(self, R, B, width, height):
        self.cantidadBasura = B  # Cantidad de agentes de basura
        self.cantidadRobot = R  # Cantidad de agentes robot
        self.grid = MultiGrid(width, height, True)  # Crea una cuadrícula con dimensiones especificadas
        self.basuraRecogida = ((width * height) * B) / 100  # Calcula la cantidad de basura inicial
        self.schedule = RandomActivation(self)  # Agendador de pasos aleatorios
        self.running = True  # Controla el estado de la simulación

        # Añade los robots a la cuadrícula y al agendador
        for i in range(self.cantidadRobot):
            a = AgenteRobot(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (1, 1))  # Posiciona el robot en (1,1)

        # Añade la basura a posiciones aleatorias en la cuadrícula
        for i in range(int(self.basuraRecogida)):
            a = Agente_Basura(i + R, self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        # DataCollector para recolectar datos de tiempo de simulación
        self.datacollector = DataCollector(model_reporters={"Time": getTime})

    # Método que detiene la simulación cuando toda la basura ha sido limpiada
    def stop(self):
        count = 0
        for agent in self.schedule.agents:
            if agent.type == 'limpio':
              count += 1
            if count == self.basuraRecogida:
                print("Terminó en:", time.time() - start_time)
                self.running = False
   
    # Método que detiene la simulación si se supera el tiempo máximo
    def stop2(self):
        if (time.time() - start_time) >= maxTime:
            self.porcentajeLimpio()
            self.running = False
            print("Fin de la simulación, se acabó el tiempo")
    # Calcula el porcentaje de basura recogida y lo imprime
    def porcentajeLimpio(self):
        global basuraRecogida
        for agent in self.schedule.agents:
            if agent.type == 'limpio':
                basuraRecogida += 1
        print("Basura Recogida:", ((basuraRecogida / self.cantidadBasura) * 100), '%')

    

    # Método que ejecuta un paso del modelo
    def step(self):
        self.stop2()  # Verifica si se alcanzó el tiempo máximo
        self.stop()  # Verifica si se limpió toda la basura
        self.schedule.step()  # Avanza un paso para todos los agentes
        print(time.time() - start_time)  # Imprime el tiempo transcurrido

