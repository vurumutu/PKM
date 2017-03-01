import serial
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

    class Semafora:
        def wlacz(self, led):
            self.send(format(led, "x") + " 00")
        def mrugaj(self, led):
            self.send("00 " + format(led, "x"))
        def wylacz(self):
            self.send(format(LED_OFF, "x") + ' ' + format(LED_OFF, "x"))

    class Zwrotnica:
        def lewo(self):
            self.send(format("31", "x"))
        def prawo(self):
            self.send(format("32", "x"))
        def wylacz(self):
            self.send(format("30", "x"))

    class Balisa:




# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=500,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser.isOpen()
ser.write('master\r')
print 'Enter your commands below.\r\nInsert "exit" to leave the application.'

input=1
while 1 :
    # get keyboard input
    input = raw_input(">> ")
        # Python 3 users
        # input = input(">> ")
    if input == 'exit':
        ser.close()
        exit()
    else:
        # send the character to the device
        # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
        ser.write(input + '\r\n')
        out = ''
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        while ser.inWaiting() > 0:
            out += ser.read(1)

        if out != '':
            print ">>" + out