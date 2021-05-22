# PegaPodLogsParser

In the recent times, log of pega applications are deployed on kubernetes env.

And most of the times, we do look at logs of POD as getting the Pega rules and alert form server would take some time.

But, these pod logs are in json format and its hard to debug. 

This tool helps to parse the JSON formatted POD logs and create two files PegaRules and PegaAlert in good format.

Usage:

Download the exe from dist folder.

open terminal in the same diretory and provide the pod log path and file name as parameter.

Example: podlog C:\user\hoyath\Desktop\webnodelogs.txt
