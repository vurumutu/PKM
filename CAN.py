import serial
import time
import CAN_const

# ramka:
# 1: '>'
# 4: addr hex in ascii
# 1: space
# 1: command
# n: parameters
# 1: '\r'


class Agent:
    def __init__(self, addr=0):
        self.address = addr

    def send(self, data):
        ser.write('>'+format(self.address, "x")+' '+data+"\r")

    def read(self, cmd):
        ser.flushInput()
        self.send(cmd)
        time.sleep(1)
        return ser.read_all()

    def skanuj(self):
        ser.flushInput()
        self.send("1F000000 39")
        time.sleep(1)
        return ser.read_all()

    def zmien_adres(self, strefa, adres):
        ser.write("61 "+format(strefa, 'x')+format(adres, 'x'))
        self.address = strefa << 16 + adres


class Semafora:
    def __init__(self, agent):
        self.agent = agent

    def wlacz(self, led):
        self.agent.send(format(led, "x") + " 00")

    def mrugaj(self, led):
        self.agent.send("00 " + format(led, "x"))

    def wylacz(self):
        self.agent.send(format(0x30, "x") + ' ' + format(0x30, "x"))


class Zwrotnica:
    def __init__(self, agent):
        self.agent = agent

    def lewo(self):
        self.agent.send(format("31", "x"))

    def prawo(self):
        self.agent.send(format("32", "x"))

    def wylacz(self):
        self.agent.send(format("30", "x"))


class Balisa:
    def __init__(self, agent):
        self.agent = agent

    def wlacz(self, histereza):
        self.agent.send("33 "+format(histereza, "x"))


# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    # port='COM3'
    port='COM21',
    baudrate=500,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

if ser.isOpen():
    print("Serial is open: ")
else:
    print("Serial is closed!!")
print(ser.portstr)
ser.write(format("master\r"))


if __name__ == '__main__':
    a1 = Agent()
    z1 = Zwrotnica(a1)
    print(a1.skanuj())
    for i in range(5):
        z1.lewo()
        time.sleep(5)
        z1.prawo()
        time.sleep(5)
    ser.close()
