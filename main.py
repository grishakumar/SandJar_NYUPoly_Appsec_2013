import os
import sys
import inspect
import resource
from __builtin__ import *

from sandBox import sandBoxStaticModule, sandBoxDynamicModule
 
global functionsWhiteDict
global typeWhiteDict

"""
Creating a white list & black list of functions that can be passed
"""
functionsList = []
for (func, funcObj) in inspect.getmembers(__builtins__):
    if inspect.isbuiltin(funcObj):
        functionsList.append(func)
functionsBlackList = ['__import__', 'apply', 'bytearray', 'compile', 'delattr', 'dir', 'exec', 'eval', 'execfile', 'file', 'getattr', 'globals', 'hasattr','id', 'input',  'locals', 'memoryview', 'open', 'reload', 'setattr', 'vars', 'type']
functionsWhiteList = [validItem for validItem in functionsList if validItem not in functionsBlackList]
functionsWhiteDict = dict([ (itemWhiteList, locals().get(itemWhiteList)) for itemWhiteList in functionsWhiteList])

typeWhiteList = ['True', 'False', 'int', 'float', 'long', 'complex','str', 'unicode', 'list', 'tuple', 'buffer', 'xrange']
typeWhiteDict = dict([ (itemWhiteList, locals().get(itemWhiteList)) for itemWhiteList in typeWhiteList])

"""
Setting a limit for resources for the sandbox:
RLIMIT_CORE: The maximum size (in bytes) of a core file that the current process can create. This may result in the creation of a partial core file if a larger core would be required to contain the entire process image.
RLIMIT_CPU: The maximum amount of processor time (in seconds) that a process can use. If this limit is exceeded, a SIGXCPU signal is sent to the process. (See the signal module documentation for information about how to catch this signal and do something useful, e.g. flush open files to disk.)
RLIMIT_FSIZE: The maximum size of a file which the process may create. This only affects the stack of the main thread in a multi-threaded process.
RLIMIT_DATA: The maximum size (in bytes) of the processs heap.
RLIMIT_STACK: The maximum size (in bytes) of the call stack for the current process.
RLIMIT_RSS: The maximum resident set size that should be made available to the process.
RLIMIT_NPROC: The maximum number of processes the current process may create.
RLIMIT_NOFILE: The maximum number of open file descriptors for the current process.
RLIMIT_OFILE: The BSD name for RLIMIT_NOFILE.
RLIMIT_MEMLOCK: The maximum address space which may be locked in memory.
RLIMIT_VMEM: The largest area of mapped memory which the process may occupy.
RLIMIT_AS: The maximum area (in bytes) of address space which may be taken by the process.
"""

def setResourceLimits():
    resource.setrlimit(resource.RLIMIT_AS,(0,524288))
    resource.setrlimit(resource.RLIMIT_CORE,(0,524288))
    resource.setrlimit(resource.RLIMIT_CPU,(0,20))
    resource.setrlimit(resource.RLIMIT_DATA,(0,524288))
    resource.setrlimit(resource.RLIMIT_FSIZE,(0,1024))
    resource.setrlimit(resource.RLIMIT_MEMLOCK,(65536,65536))
    resource.setrlimit(resource.RLIMIT_NOFILE,(1024,4096))
    resource.setrlimit(resource.RLIMIT_NPROC,(27109,27109))
    #resource.setrlimit(resource.RLIMIT_OFILE,(9,7))
    resource.setrlimit(resource.RLIMIT_RSS,(-1,-1))
    resource.setrlimit(resource.RLIMIT_STACK,(0,524288))

  
def main():
    
    """
    Users can enter only one extra argument to run with the python file else print ERROR and exit code
    """
    if(len(sys.argv) == 2): 
        scriptName = sys.argv[1] 
    else :
        print """Please enter only 1 argument and try again..."""
        exit(0)
    
        
    setResourceLimits()
    try:
        print "Reading script..."
        scriptText = open(scriptName, "rb").read()
        
        """
        Testing in sandbox static and dynamic module class, the script text
        """
        sandBoxObjStatic = sandBoxStaticModule(scriptName, scriptText)
        sandBoxObjStatic.testStaticMain()
        sandBoxObjDynamic = sandBoxDynamicModule(scriptName, scriptText, functionsWhiteDict, typeWhiteDict)
        sandBoxObjDynamic.testDynamicMain()
        
    except Exception,e:
        print "Error:" + str(e)
    print "Sandbox exiting..."
        
    

if __name__ == "__main__":
    main()