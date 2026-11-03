# Description: Set status values to integer and workLogs
#
# Publish Channel: DM.CRM.OUT
#
# Author: Pramod
# Date: 13-May-2025
#*****************************************************************************************
from org.jdom2 import Namespace

worklog=""
if irData.getCurrentMbo().getString("VENDOR"):
    compSet=irData.getCurrentMbo().getMboSet("DM_VENDOR")
    if compSet.count()>0:
        compNam=compSet.getMbo(0).getString("NAME")
        worklog="Assigned to Contractor "+compNam


if (irData.getCurrentDataAsString("STATUS") == 'NEW') :
    irData.setCurrentData("STATUS","930650010")
elif (irData.getCurrentDataAsString("STATUS") == 'INPROG') :
    irData.setCurrentData("STATUS","")
    irData.setCurrentData("REMARKDESC","Work is in progress")
elif (irData.getCurrentDataAsString("STATUS") == 'ASSIGNED') :
    irData.setCurrentData("STATUS","")
    irData.setCurrentData("REMARKDESC","Ticket Assigned")
elif (irData.getCurrentDataAsString("STATUS") == 'REJECTED') :
    irData.setCurrentData("STATUS","2000")
    irData.setCurrentData("REMARKDESC","Ticket Rejected")
elif (irData.getCurrentDataAsString("STATUS") == 'RESOLVED') :
    irData.setCurrentData("STATUS","5")
    irData.setCurrentData("REMARKDESC","Ticket Resolved")
elif (irData.getCurrentDataAsString("STATUS") == 'CLOSED') :
    irData.setCurrentData("STATUS","")
    irData.setCurrentData("REMARKDESC","Ticket Closed")