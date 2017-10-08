from ctypes import *
import time

#msvcrt - Microsoft C Runtime Library
msvcrt = cdll.msvcrt

counter=0

while 1:
    msvcrt.printf("Loop iteration %d!\n",counter) #ctypes to print
    time.sleep(2) #Suspend execution of the current thread for 2 seconds
    counter +=1
