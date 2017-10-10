fromm pydbg import *
from pydbg.defines import *

import struct
import random

# This is our user defined callback function
def printf_randomizer(dbg):
    
    # Read in the value of the counter at ESP + 0x4 as a DWORD
    parameter_addr = dbg.context.Esp + 0x4
    #print dbg.dump_context()
    counter = dbg.read_process_memory(parameter_addr,4)
    
    # When using read_process_memory, it returns a packed binary
    # string, we must first unpack it before we can use it further
    
    # Hack time. Our real parameter address is different, since it's
    # referenced. This is the base. We'll need to go into it to find the
    # offset
    parameter_addr_base = struct.unpack("L",counter)[0]
    
    # If using this string, "Loop iteration ", the length to number = 15
    # Add in the number itself (assume counter doesn't go beyond XXXX
    # And then "!\n", two more bytes
    string_len = 15 + 4 + 2
    counter_string = dbg.read_process_memory(parameter_addr_base, int(string_len))
    counter_string = struct.unpack(str(string_len) + "s",counter_string)[0]

    # cleanup string
    counter_string = counter_string.split("!\n")[0]
    # And grab number
    counter = counter_string[15:]
    print "Counter: %d" % int(counter)
    
    # Generate a random number and pack it into binary format
    # so that it is written correctly back into the process
    random_counter = int(random.randint(1,100))
    
    # Pack in only what will fit, though.
    if (len(counter) > 1): 
        random_counter = str(random_counter)[0:len(counter)-1]
    else:
        random_counter = str(random_counter)[0]
    #random_counter = struct.pack("L",random_counter)[0]
        
    # Change our parameter address to point to the right
    # location, 15 characters in
    parameter_addr = parameter_addr_base + 15
        
    # Now swap in our random number and resume the process
    dbg.write_process_memory(parameter_addr,random_counter)
        
    return DBG_CONTINUE

# Instantiate the pydbg class
dbg = pydbg()

# Now enter the PID of the printf_loop.py process
pid = raw_input("Enter the printf_loop.py PID: ")

# Attach the debugger to that process
dbg.attach(int(pid))

# Set the breakpoint with the printf_randomizer function
# defined as a callback
printf_address = dbg.func_resolve("msvcrt","printf")
dbg.bp_set(printf_address,description="printf_address",handler=printf_randomizer)

# Resume the process
dbg.run()
