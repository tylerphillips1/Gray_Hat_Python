from ctypes import *
from my_debugger_defines import *

# 32-bit dynamic link library for Windows OS kernel
kernel32 = windll.kernel32

class debugger():
    
    # Constructor
    def _init_(self): 
        pass
 
    # Launch application with path given
    def load(self, path_to_exe):
        
        # Constant from my_debugger_defines
        creation_flags = DEBUG_PROCESS

        # Structure from my_debugger_defines used for CreateProcessA()
        startupinfo = STARTUPINFO()                  # https://msdn.microsoft.com/en-us/library/ms686331.aspx
        process_information = PROCESS_INFORMATION()  # https://msdn.microsoft.com/en-us/library/ms684873(v=vs.85).aspx
 
        # The following two options allow the started process to be shown as a separate window. 
        # Illustrates different settings in the STARTUPINFO struct can affect the debuggee.
        startupinfo.dwFlags = 0x1
        startupinfo.wShowWindow = 0x0
 
        # Initialize the cb variable in the STARTUPINFO struct which is just the size of the struct itself
        startupinfo.cb = sizeof(startupinfo)
 
        # Launce path_to_exe using Widowns API
        if kernel32.CreateProcessA(path_to_exe,   # https://msdn.microsoft.com/en-us/library/ms682425.aspx
                               None,
                               None,
                               None,
                               None,
                               creation_flags,
                               None,
                               None,
                               byref(startupinfo),
                               byref(process_information)):
            print "[*] We have successfully launched the process!"
            print "[*] PID: %d" % process_information.dwProcessId
 
        # Unable to lanch .exe file
        else:
            print "[*] Error: 0x%08x." % kernel32.GetLastError() 
