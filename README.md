# PegaPodLogsParser
Note: This is a personal project and not official tool from Pega 

In the recent times, lot of pega applications are deployed on kubernetes environments.
And most of the times, we tend to look at POD logs rather than PegaRules/Alerts as its quicker and it would take time to get these from server.

But, these pod logs are in json format and its hard to debug. 
This tool helps to parse the JSON formatted POD logs and create two files PegaRules and PegaAlert in Proper format which is understandable by the Pega provided log viewer for easy debuggin.

Usage:

Download the exe file from dist folder.

open terminal in the same diretory and provide the pod log path and file name as parameter.

Example: podlog C:\user\hoyath\Desktop\webnodelogs.txt

This will generate PegaRules and Alert logs seperately on your desktop.
