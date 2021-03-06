from ctypes import *
from my_debugger_defines import *

# 32-bit dynamic link library for Windows OS kernel
kernel32 = windll.kernel32


class debugger():
    
    # Constructor for getting process ID
    def _init_(self): 
        self.h_process       = None
        self.debugger_active = False
        process_information  = PROCESS_INFORMATION()             # https://msdn.microsoft.com/en-us/library/ms684873(v=vs.85).aspx
        self.pid             = process_information.dwProcessId   # https://msdn.microsoft.com/en-us/library/windows/desktop/ms684873(v=vs.85).aspx

    # Creates a new process and its primary thread
    def load(self, path_to_exe):
        
        # Constant from my_debugger_defines used in CreateProcessA()
        creation_flags = DEBUG_PROCESS               # https://msdn.microsoft.com/en-us/library/windows/desktop/ms684863(v=vs.85).aspx
        
        startupinfo         = STARTUPINFO()          # https://msdn.microsoft.com/en-us/library/ms686331.aspx
        process_information = PROCESS_INFORMATION()  # https://msdn.microsoft.com/en-us/library/ms684873(v=vs.85).aspx
        
        # The following two options allow the started process to be shown as a separate window. 
        # Illustrates different settings in the STARTUPINFO struct can affect the debuggee.
        startupinfo.dwFlags     = 0x1                # https://msdn.microsoft.com/en-us/library/windows/desktop/ms686331(v=vs.85).aspx
        startupinfo.wShowWindow = 0x0                # https://msdn.microsoft.com/en-us/library/windows/desktop/ms633548(v=vs.85).aspx
        
        # Initialize the cb variable in the STARTUPINFO struct which is just the size of the struct itself
        startupinfo.cb = sizeof(startupinfo)

        # Launce path_to_exe using Widowns API function
        if kernel32.CreateProcessA(path_to_exe,  # https://msdn.microsoft.com/en-us/library/ms682425.aspx
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
            self.h_process = self.open_process(process_information.dwProcessId)
        else:
            print "[*] Error: 0x%08x." % kernel32.GetLastError() 
      
    
    def open_process(self, pid):
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)  # https://msdn.microsoft.com/en-us/library/ms684320.aspx?query=
        return h_process
    
    
    def attach(self, pid):
        self.h_process = self.open_process(pid)
         
        if kernel32.DebugActiveProcess(pid):
            self.debugger_active = True
            self.pid             = int(pid)
            self.run()
            
        else:
            print "[*] Unable to attach to the process [%d] - %s" % (int(pid), FormatError(kernel32.GetLastError()))
       
    
    def run(self):  
        while self.debugger_active == True:
            self.get_debug_event()
            
            
    def get_debug_event(self):
        debug_event     = DEBUG_EVENT()                               # https://msdn.microsoft.com/en-us/library/windows/desktop/ms679308(v=vs.85).aspx
        continue_status = DBG_CONTINUE                                # https://msdn.microsoft.com/en-us/library/windows/desktop/ms679285(v=vs.85).aspx
        
        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):  # https://msdn.microsoft.com/en-us/library/windows/desktop/ms681423(v=vs.85).aspx
            
            raw_input("Press a key to continue...")
            
            self.debugger_active= False
            kernel32.ContinueDebugEvent(\
                debug_event.dwProcessId, \
                debug_event.dwThreadId, \
                continue_status)
            
            
    def detach(self):
        if kernel32.DebugActiveProcessStop(self.pid):                 # https://msdn.microsoft.com/en-us/library/windows/desktop/ms679296(v=vs.85).aspx
            print "[*] Finished debugging. Exiting..."
            return True
        else:
            print "There was an error"
            return False
