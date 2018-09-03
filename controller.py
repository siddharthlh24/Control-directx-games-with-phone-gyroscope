import ctypes
import time
import socket


UDP_IP = "192.168.43.153"
UDP_PORT = 5007
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


SendInput = ctypes.windll.user32.SendInput


up = 0xC8
left = 0xCB
right = 0xCD
down = 0xD0
a=1

up1 = 0
down1 = 0
left1 = 0
right1 = 0



# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    
def Pressup():
            print("fwd")
            PressKey(0xC8)
            #time.sleep(0.1)
            ReleaseKey(0xD0)
            up1 = 1
            down1 = 0

def Pressdown():
                print("bwd")
                PressKey(0xD0)
                #time.sleep(0.1)
                ReleaseKey(0xC8)
                up1 = 0
                down1 = 1
                
def Pressright():
                print("rgt")
                PressKey(0xCD)
                #time.sleep(0.1)
                ReleaseKey(0xCB)
                left1 = 0
                right1 = 1
                

def Pressleft():
                print("lft")
                PressKey(0xCB)
                #time.sleep(0.1)
                ReleaseKey(0xCD)
                left1 = 1
                right1 = 0
                
def linearrelease():
    ReleaseKey(0xD0)
    ReleaseKey(0xC8)
    up1 = 0
    down1 = 0
    
def lateralrelease():
    ReleaseKey(0xCD)
    ReleaseKey(0xCB)
    left1 = 0
    right1 = 0
    
        
while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        #print(data)

        a=data.decode()
        ar1=a.split(',')
        y=ar1[4]
        z=ar1[5]
        #print(z)
        
        if float(z)< -8  :
            Pressup()
            
        elif float(z)> -4.5 :
            Pressdown()
            
        else :
            linearrelease()

            
        if float(y)>1  :
            Pressleft()
            
        elif float(y)<-1 :
            Pressright()
            
        else :
            lateralrelease()
            
                

