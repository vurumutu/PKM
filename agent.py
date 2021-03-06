from pade.misc.utility import display_message
from pade.misc.common import set_ams, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.acl.messages import ACLMessage

import threading
import time

class AgenteHelloWorld(Agent):
    def __init__(self, aid):
        super(AgenteHelloWorld, self).__init__(aid=aid, debug=False)
        display_message(self.aid.localname, 'Salam dunya!')
        position = 100

    def newOrder(self):
        display_message(self.aid.localname, 'Nowy cel')
        message = ACLMessage(ACLMessage.INFORM)
        message.add_receiver(AID('Destinatario'))
        message.set_content('Ola')
        self.send(message)
        print("cos")

    def react(self, message):
        display_message(self.aid.localname, 'Mensagem recebida')
        print("cos_w_odpowiedzi")

