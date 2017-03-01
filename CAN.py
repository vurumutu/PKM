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
    address = 0

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
        def wlacz(self, led):
            self.send(format(led, "x") + " 00")

        def mrugaj(self, led):
            self.send("00 " + format(led, "x"))

        def wylacz(self):
            self.send(format(0x30, "x") + ' ' + format(0x30, "x"))


    class Zwrotnica:
        def lewo(self):
            self.send(format("31", "x"))

        def prawo(self):
            self.send(format("32", "x"))

        def wylacz(self):
            self.send(format("30", "x"))

    class Balisa:
        def wlacz(self, histereza):
            self.send("33 "+format(histereza, "x"))


# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    #port='/dev/ttyUSB1',
    #port='COM3',
    0,
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
    a1 = Agent
    print(a1.skanuj(a1))
    while 1:
        a1.Zwrotnica.lewo()
        time.sleep(5)
        a1.Zwrotnica.prawo()
        time.sleep(5)
    ser.close()