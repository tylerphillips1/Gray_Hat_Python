from pydbg import *
from pydbg.defines import *
from ctypes import windll


import struct
import random

# This is our user defined callback function
def printf_randomizer(dbg):
    
    # Read in the value of the counter at ESP + 0x8 as a DWORD
    parameter_addr = dbg.context.Esp + 0x8
    counter = dbg.read_process_memory(parameter_addr, 4)
    
    # When using read_process_memory, it returns a packed binary
    # string, we must first unpack it before we can use it further
    counter = struct.unpack("L", counter)[0]
    print "Counter: %d" % int(counter)
    
    # Generate a random number and pack it into binary format
    # so that it is written correctly back into the process
    random_counter = random.randint(1, 100)
    random_counter = struct.pack("L", random_counter)[0]
    
    dbg.write_process_memory(parameter_addr, random_counter)

    return DBG_CONTINUE

dbg = pydbg()
pid = raw_input("Enter the printf_loop.py PID: ")

dbg.attach(int(pid))

printf_address = dbg.func_resolve("msvcrt", "printf")
dbg.bp_set(printf_address, description = "printf_address", handler = printf_randomizer)

dbg.run()
