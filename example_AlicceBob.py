#!/usr/bin/env python3

import random

from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative
from communication.message.MessageService import MessageService


class SpeakingAgent(CommunicatingAgent):
    """ """
    def __init__(self, unique_id, model, name):
        super().__init__(unique_id, model, name)
        self.__v = random.randint(0, 1000)

    def step(self):
        super().step()
        #To complete

class SpeakingModel(Model):
    """ """
    def __init__(self):
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)
        self.running = True

    def step(self):
        #To complete



if __name__ == "__main__":
    # Init the model and the agents
     #To complete

   
  

    # Launch the Communication part 

       # To complete

    step = 0
    while step < 10:
        speaking_model.step()
        step += 1
