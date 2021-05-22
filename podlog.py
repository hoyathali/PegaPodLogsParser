
import json
import sys
from os.path import join
import os
import datetime
#a
def progressBar(rulelogfile,alertlogfile,current, total, barLength = 20):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))
    print('Progress: [%s%s] %d ' % (arrow, spaces, percent), end='\r')

def startProgress(title):
    global progress_x
    sys.stdout.write(title + ": [" + "-"*40 + "]" + chr(8)*41)
    sys.stdout.flush()
    progress_x = 0

def progress(x):
    global progress_x
    x = int(x * 40 // 100)
    sys.stdout.write("#" * (x - progress_x))
    sys.stdout.flush()
    progress_x = x

def endProgress(pegaruleslog,pegaalertlog):
    sys.stdout.write("#" * (40 - progress_x) + "]\n")
    print("Logs have been parsed and stored at " + join(os.path.join(os.path.expanduser("~"), "desktop")))
    print("1. " +pegaruleslog)
    print("2. " + pegaalertlog)
    sys.stdout.flush()

def format(brace,size,text):
    output=brace
    if(len(text)<size):
        for i in range(0,size-len(text)):
            output=output+" "
        output=output+text
    else:
        output=output+text[-size:]
    if(brace=='['):
        output=output+ ']'
    else:
        output=output+')'
    return output
def writeAlerts(file,message):
    file.write(message)

def writeRules(file,time,threadname,pegathread,tenantid,app,loggername,level,userid,message,exceptionclass,exceptionmessage,stacktrace):
    output=""
    output= output+(time.replace("T", " ").replace("Z", "").replace(".",",")+" ")
    output= output+(format('[',20,threadname)+" ")
    output= output+(format('[',10,pegathread)+" ")
    output= output+(format('[',20, tenantid)+" ")
    output= output+(format('[', 20, app)+" ")
    output= output+(format('(',30, loggername)+" ")
    output= output+(level+"  ")
    if(userid):
        output= output+(userid+" - ")
    else:
        output=output+("  - ")
    output= output+(message+" ")
    output=output+(exceptionclass+": ")
    output = output + (exceptionmessage)
    output = output + ("\n"+stacktrace)
    #print(output)
    file.write(output)

if(len(sys.argv)<2):
    print("Please provide File  name as parameter.... ")
    print("Example: Podlog C:/users/singh4/desktop/podlogs.txt or .log file")
else:
    print(sys.argv[1])
    pegarules = []
    pegaalert = []
    stack=[]
    try:
        f = open(sys.argv[1], "r")
    except:
      print("There was an issue while trying to read the file, probably the file doesn't exist")
      print("Please provide File  name as parameter.... ")
      print("Example: Podlog C:/users/singh4/desktop/podlogs.txt or .log file")
      sys.exit()

    data = f.read()
    stack.append(-1)
    rulelogfile="Pod_PegaRules"+datetime.datetime.now().strftime("%d%M%Y%H%M%S")+".txt"
    alertlogfile="Pod_PegaAlert"+datetime.datetime.now().strftime("%d%M%Y%H%M%S")+".txt"
    ruleslog = open(join(os.path.join(os.path.expanduser("~"), "desktop"),rulelogfile), 'w+')
    alertlog = open(join(os.path.join(os.path.expanduser("~"), "desktop"),alertlogfile), 'w+')
    total = len(data)

    if(total<10):
        print("Incomplete file (not enough logs to display), please provide a complete log file ")
    else:
        startProgress("Parsing the Log file")
        for i in range(0,len(data)):
            if(data[i]=='{'):
                stack.append(i)
            elif(data[i]=='}'):
                popped=stack.pop()
                if(len(stack)==1):
                    templog=json.loads(data[popped:i+1])
                    if templog.get('alertType'):
                        writeAlerts(alertlog,templog.get('message'))
                        progress((i / total) * 100)
                    else:
                        if templog.get('exception'):
                           writeRules(ruleslog, templog.get('@timestamp'),
                                       templog.get('thread_name'),
                                       templog.get('pegathread'),
                                       templog.get('tenantid'),
                                       templog.get('app'),
                                       templog.get('logger_name'),
                                       templog.get('level'),
                                       templog.get('userid'),
                                       templog.get('message'),
                                       templog['exception']['exception_class'],
                                       templog['exception']['exception_message'],
                                       templog['exception']['stacktrace'])
                           progress((i / total) * 100)

                        else:
                            writeRules(ruleslog,templog.get('@timestamp'),
                                       templog.get('thread_name'),
                                       templog.get('pegathread'),
                                       templog.get('tenantid'),
                                       templog.get('app'),
                                       templog.get('logger_name'),
                                       templog.get('level'),
                                       templog.get('userid'),
                                       templog.get('message'),
                                       '','','')
                            progress((i / total) * 100)
        endProgress(rulelogfile,alertlogfile)





