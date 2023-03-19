#!/usr/bin/env python3

import random

from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative
from communication.message.MessageService import MessageService


##################################
###### ALICE OU BOB ##############
##################################

class SpeakingAgent(CommunicatingAgent):
    """ """

    def __init__(self, unique_id, model, name):
        super().__init__(unique_id, model, name)
        self.__v = random.randint(0, 1000)
        self.name = name

    def get_v(self):
        return self.__v

    def step(self):
        # il faut recevoir les messages
        new_messages = set(self.get_new_messages())
        message = None

        if new_messages:
            if new_messages.intersection(set(self.get_messages_from_performative(MessagePerformative.ACCEPT))):
                for mess in new_messages.intersection(set(self.get_messages_from_performative(MessagePerformative.ACCEPT))):
                    sender = mess.get_exp()
                    message = Message(self.name, sender,
                                      MessagePerformative.QUERY_REF, "v?")
                    self.send_message(message)
                    print(message.__str__())

            # if on a reçu un commit
            if new_messages.intersection(set(self.get_messages_from_performative(MessagePerformative.COMMIT))):
                for mess in new_messages.intersection(set(self.get_messages_from_performative(MessagePerformative.COMMIT))):
                    sender = mess.get_exp()
                    message = Message(self.name, sender,
                                      MessagePerformative.ACCEPT, "ok tiptop")
                    self.send_message(message)
                    print(message.__str__())

            # if on a reçu des inform_ref
            if (new_messages.intersection(set(self.get_messages_from_performative(
                    MessagePerformative.INFORM_REF)))
                    ):
                for mess in new_messages.intersection(set(self.get_messages_from_performative(
                        MessagePerformative.INFORM_REF))):
                    sender = mess.get_exp()
                    value = mess.get_content()
                    if self.__v == value:
                        message = Message(
                            self.name, sender, MessagePerformative.ACCEPT, "ok tiptop"
                        )
                        self.send_message(message)
                        print(message.__str__())
                    else:
                        message = Message(
                            self.name, sender, MessagePerformative.PROPOSE, self.__v
                        )
                        self.send_message(message)
                        print(message.__str__())

        # sinon, pas de message en attente


##################################
###### CHARLES ###################
##################################

class ControlAgent(CommunicatingAgent):
    def __init__(self, unique_id, model, name):
        super().__init__(unique_id, model, name)
        self.__v = random.randint(0, 1000)
        self.name = name

    def get_v(self):
        return self.__v

    def step(self):
        # il faut recevoir les messages
        new_messages = set(self.get_new_messages())
        # print([mess.__str__() for mess in new_messages])
        message = None

        if new_messages:
            if new_messages.intersection(set(self.get_messages_from_performative(MessagePerformative.ACCEPT))):
                for mess in new_messages.intersection(set(self.get_messages_from_performative(MessagePerformative.ACCEPT))):
                    sender = mess.get_exp()
                    message = Message(self.name, sender,
                                      MessagePerformative.ACCEPT, "on termine alors !")
                    self.send_message(message)
                    print(message.__str__())

            # if on a recu des propose
            if new_messages.intersection(set(self.get_messages_from_performative(MessagePerformative.PROPOSE))):
                for mess in new_messages.intersection(set(self.get_messages_from_performative(MessagePerformative.PROPOSE))):
                    sender = mess.get_exp()
                    value = mess.get_content()
                    self.__v = value
                    message = Message(self.name, sender,
                                      MessagePerformative.COMMIT, self.__v)
                    self.send_message(message)
                    print(message.__str__())

            # if on a reçu des query
            if new_messages.intersection(set(self.get_messages_from_performative(MessagePerformative.QUERY_REF))):
                # je le lis, j'identifie la valeur et l'envoyeur
                # print([mess.__str__() for mess in new_messages.intersection(
                #     set(self.get_messages_from_performative(MessagePerformative.QUERY_REF)))])
                for mess in new_messages.intersection(set(self.get_messages_from_performative(MessagePerformative.QUERY_REF))):
                    # print(mess)
                    sender = mess.get_exp()
                    message = Message(
                        self.name, sender, MessagePerformative.INFORM_REF, self.__v
                    )
                    self.send_message(message)
                    print(message.__str__())


##################################
###### MODEL #####################
##################################

class SpeakingModel(Model):
    """ """

    def __init__(self):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)
        self.running = True

    def step(self):
        # self.__message_service.get_instance(.set_instant_delivery(False)
        # self.__messages_service.dispatch_messages()
        self.schedule.step()


##################################
###### RUN THE MODEL #############
##################################
if __name__ == "__main__":
    # Init model and agents
    speaking_model = SpeakingModel()

    # Create Alice, Bob, Charles
    Alice = SpeakingAgent(speaking_model.next_id(), speaking_model, "Alice")
    Bob = SpeakingAgent(speaking_model.next_id(), speaking_model, "Bob")
    Charles = ControlAgent(speaking_model.next_id(), speaking_model, "Charles")

    # add au scheduler
    for a in [Alice, Bob, Charles]:
        print(f"L'agent {a.get_name()} a pour valeur {a.get_v()}")
        speaking_model.schedule.add(a)

    # Launch the Communication part
    message = Message("Alice", "Charles", MessagePerformative.QUERY_REF, "v?")
    print(message.__str__())
    Alice.send_message(message)
    message = Message("Bob", "Charles", MessagePerformative.QUERY_REF, "v?")
    print(message.__str__())
    Bob.send_message(message)

    step = 0
    while step < 50:
        speaking_model.step()
        step += 1
