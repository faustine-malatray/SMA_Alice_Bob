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
        self.name = name

    def step(self):
        super().step()
        # il faut recevoir les messages
        self.get_messages()
        message = None

        # if on a reçu des inform_ref
        if (
            len(self.get_messages_from_performative(MessagePerformative.INFORM_REF))
            >= 1
        ):
            for mess in self.get_messages_from_performative(
                MessagePerformative.INFORM_REF
            ):
                sender = mess.get_exp()
                value = mess.get_content()
                if self.__v == value:
                    message = Message(
                        self.name, sender, MessagePerformative.ACCEPT, "ok tiptop"
                    )
                else:
                    message = Message(
                        self.name, sender, MessagePerformative.PROPOSE, self.__v
                    )

        # if on a reçu un commit
        if len(self.get_messages_from_performative(MessagePerformative.COMMIT)) >= 1:
            for mess in self.get_messages_from_performative(MessagePerformative.COMMIT):
                sender = mess.get_exp()
                message = Message(self.name, sender, MessagePerformative.ACCEPT, "ok tiptop")

        if message:
            self.send_message(message)
            print(message.__str__())


class ControlAgent(CommunicatingAgent):
    def __init__(self, unique_id, model, name):
        super().__init__(unique_id, model, name)
        self.__v = random.randint(0, 1000)
        self.name = name

    def step(self):
        super().step()
        # il faut recevoir les messages
        self.get_messages()
        message = None

        # if on a reçu des query
        if len(self.get_messages_from_performative(MessagePerformative.QUERY_REF)) >= 1:
            # je le lis, j'identifie la valeur et l'envoyeur
            for mess in self.get_messages_from_performative(
                MessagePerformative.QUERY_REF
            ):
                sender = mess.get_exp()
                message = Message(
                    self.name, sender, MessagePerformative.INFORM_REF, self.__v
                )

        # if on a recu des propose
        if len(self.get_messages_from_performative(MessagePerformative.PROPOSE)) >= 1:
            for mess in self.get_messages_from_performative(
                MessagePerformative.PROPOSE
            ):
                sender = mess.get_exp()
                value = mess.get_content()
                self.__v = value
                message = Message(self.name, sender, MessagePerformative.COMMIT, self.__v)

        if len(self.get_messages_from_performative(MessagePerformative.ACCEPT)) >= 1:
            pass

        if message:
            self.send_message(message)
            print(message.__str__())


class SpeakingModel(Model):
    """ """

    def __init__(self):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)
        self.running = True

    def step(self):
        # self.__message_service.get_instance(.set_instant_delivery(False)
        self.__messages_service.dispatch_messages()
        self.schedule.step()


if __name__ == "__main__":
    # Init model and agents
    speaking_model = SpeakingModel()

    # Create Alice, Bob, Charles
    # add au scheduler
    Alice = SpeakingAgent(speaking_model.next_id(), speaking_model, "Alice")
    Bob = SpeakingAgent(speaking_model.next_id(), speaking_model, "Bob")
    Charles = ControlAgent(speaking_model.next_id(), speaking_model, "Charles")

    speaking_model.schedule.add(Alice)
    speaking_model.schedule.add(Bob)
    speaking_model.schedule.add(Charles)

    # Launch the Communication part
    message = Message("Alice", "Charles", MessagePerformative.QUERY_REF, "v?")
    print(message.__str__())
    Alice.send_message(message)

    step = 0
    while step < 10:
        speaking_model.step()
        step += 1
