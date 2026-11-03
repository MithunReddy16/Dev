#-----------------------------------------------------------------------------------------
# Name:        SYNC.GRPPOINTERFACE.USEREXIT.IN.BEFORE
# Description: Set default values and normalize status for inbound PO data (XML-based)
#
# Enterprise Service: GRP_POSTD
# Event: Integration --> Enterprise Service --> Request --> User Exit --> Before External Exit
#
# Author: Mithun Reddy
# Version: 1.0 - 21-Mar-2025
# Version: 2.0 - Amir Anwar - 21-Mar-2025
# Version: 3.0 - Amir Anwar - 31-Dec-2025 - Changes for Blanket  PO and Release number
#-----------------------------------------------------------------------------------------
from psdi.iface.mic import StructureData
from psdi.server import MXServer
from psdi.util.logging import MXLoggerFactory
from java.io import StringWriter
from javax.xml.transform import TransformerFactory
from javax.xml.transform.dom import DOMSource
from javax.xml.transform.stream import StreamResult
from org.jdom2.output import XMLOutputter
from psdi.server import MXServer
from psdi.mbo import SqlFormat
from psdi.util import MXApplicationException
from java.text import SimpleDateFormat

logger = MXLoggerFactory.getLogger("maximo.custom")
logger.debug("============= SYNC.GRPPOINTERFACE.USEREXIT.IN.BEFORE: START =============")

'''
Standard Receipt - 2 steps
1-Receive
2-Deliver
Inspection -  3 steps
1-Receive
2-Inspection
3-Deliver
 
Direct Delivery  one step
'''

def getMaximoUoM(UOM):
    MaximoUoM = UOM
    UoMSet = MXServer.getMXServer().getMboSet("MEASUREUNIT", MXServer.getMXServer().getSystemUserInfo())
    where = SqlFormat(UoMSet.getUserInfo(), "MEASUREUNITID = :1")
    where.setObject(1, "MEASUREUNIT", "MEASUREUNITID", UOM)
    
    UoMSet.setWhere(where.format())
    UoMSet.reset()
    
    UoMMbo = UoMSet.moveFirst()
    if UoMMbo and not UoMMbo.isNull('DM_GRPUNITID'):
        MaximoUoM = UoMMbo.getString('DM_GRPUNITID')
    UoMSet.cleanup()
    UoMSet.close()
    
    return  MaximoUoM


def mandatoryChecks(erData):
    logger.debug("***mandatorychecks def***")
    if False:
        ctx.error("", "ERROR", ["No Site or Revision found."])
    #if erData.isCurrentDataNull("ITEMNUM"):
        #raise MXApplicationException("integration", "missingitemnum")


#----------------------------------------------------------------------------------------------    
#------------------------------------------------------------------------------
#
#
#Delete Lines that marked as delete within the action
#------------------------------------------------------------------------------
def DeleteLines(erData,LinesToBeDeleted):
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-Delete Lines - Started - :" + str(LinesToBeDeleted) + " len=" + str(len(LinesToBeDeleted)))
    if len(LinesToBeDeleted) <=0:
        return
    k=0

    LinesToBeDeleted.sort(reverse=True)
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-Delete Lines - Starting Delete Loop + " + str(LinesToBeDeleted))
    for k in range(len(LinesToBeDeleted)):
        
        try:
            erData.removeChildData("POLINE",LinesToBeDeleted[k])
        except:
        # Catch all exceptions
            scError = sys.exc_info()[1]
            logger.debug("\n\r!!!  SYNC.POINTERFACE.USEREXIT.IN.BEFORE- Couldn't delete line -  error : " + str(scError))



#-----------------------------------------------------------------------------------------
# Set default values for required fields if missing in the incoming XML data
#-----------------------------------------------------------------------------------------
def setDefaultValues(erData):
    logger.debug("Setting default values if missing...")

    if erData.isCurrentDataNull("SITEID"):
        erData.setCurrentData("SITEID", "DM")
        logger.debug("SITEID defaulted to DM")



    # setting potype as STD in all cases 
    erData.setCurrentData("ORGID", "DMORG")
    #erData.setCurrentData("POTYPE", "STD")
    
#-----------------------------------------------------------------------------------------
# get the contract MBO
#
# @param Mbo (poNum) The Contract Number
# @param Mbo (siteId) The Organization
#-----------------------------------------------------------------------------------------
def getPO(poNum, siteId):
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-getPO\n" + " - PO: " + str(poNum))

    whereclause = "ponum = :1 and siteid = :2" 
    whereclause = whereclause + " and revisionnum = (select max(revisionnum) from po where ponum = :1 and siteid = :2 "
    whereclause = whereclause + " and status not in (select value from synonymdomain where domainid = 'POSTATUS' and maxvalue in ('CAN', 'REVISE', 'CLOSE')))"
    
    sqlFormat = SqlFormat(userInfo, whereclause)    
    sqlFormat.setObject(1, "PO", "ponum", poNum)
    sqlFormat.setObject(2, "PO", "siteid", siteId)
    #sqlFormat.setObject(3, "PO", "revisionnum", revisionNum)
    
    pos = MXServer.getMXServer().getMboSet("PO", userInfo)
    pos.setWhere(sqlFormat.format())
    pos.reset()
    
    #logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-getPO\n" + " - whereclause: " + pos.getCompleteWhere())
    
    return pos.getMbo(0)


def getSamePO(poNum, siteId,revisionNum):
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-getPO\n" + " - PO: " + str(poNum))

    whereclause = "ponum = :1 and siteid = :2" 
    whereclause = whereclause + " and revisionnum = (select max(revisionnum) from po where ponum = :1 and siteid = :2 "
    whereclause = whereclause + " and status not in (select value from synonymdomain where domainid = 'POSTATUS' and maxvalue in ('CAN', 'REVISE', 'CLOSE')))"
    
    sqlFormat = SqlFormat(userInfo, whereclause)    
    sqlFormat.setObject(1, "PO", "ponum", poNum)
    sqlFormat.setObject(2, "PO", "siteid", siteId)
    #sqlFormat.setObject(3, "PO", "revisionnum", revisionNum)
    
    pos = MXServer.getMXServer().getMboSet("PO", userInfo)
    pos.setWhere(sqlFormat.format())
    pos.reset()
    
    #logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-getPO\n" + " - whereclause: " + pos.getCompleteWhere())
    
    return pos.getMbo(0)
#---------------------------------------------------------------------------------------------
# Add PO Line
#
#------------------------------------------------------------------------------------------
def addPOLine(data,POLine):
    data.createChildrenData("POLINE",True)
    data.setCurrentData("POLINENUM",POLine.getString('POLINENUM'))
    data.setCurrentData("TOSITEID",POLine.getString('TOSITEID'))
    

    data.setCurrentData("ITEMNUM",POLine.getString('ITEMNUM'))
    data.setCurrentData("DESCRIPTION",POLine.getString('DESCRIPTION'))
    data.setCurrentData("UNITCOST",POLine.getDouble('UNITCOST'))
    data.setCurrentData("LINECOST",POLine.getDouble('LINECOST'))
    data.setCurrentData("ORDERQTY",POLine.getDouble('ORDERQTY'))
    data.setCurrentData("LINETYPE",POLine.getString('LINETYPE'))
    data.setCurrentData("ORDERUNIT",POLine.getString('ORDERUNIT'))

    data.setCurrentData("PRNUM",POLine.getString('PRNUM'))
    data.setCurrentData("PRLINENUM",POLine.getString('PRLINENUM'))
    
    data.setCurrentData("VENDELIVERYDATE",POLine.getDate('VENDELIVERYDATE'))
    data.setCurrentData("REQDELIVERYDATE",POLine.getDate('REQDELIVERYDATE'))

    data.setCurrentData("STORELOC",POLine.getString('STORELOC'))
    
    

    data.setCurrentData("GLDEBITACCT",POLine.getString('GLDEBITACCT'))
    if POLine.getBoolean('RECEIPTSCOMPLETE'):
        data.setCurrentData("RECEIPTSCOMPLETE",POLine.getString('RECEIPTSCOMPLETE'))

    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE\n" + " - New POLINE details: "
                         
                         + "\n POLINENUM = " + str(data.getCurrentDataAsString("POLINENUM"))
                         + "\n LINETYPE = " + str(data.getCurrentDataAsString("LINETYPE"))
                         + "\n ITEMNUM = " + str(data.getCurrentDataAsString("ITEMNUM"))
                         + "\n PRNUM = " + str(data.getCurrentDataAsString("PRNUM"))
                         + "\n PRLINENUM = " + str(data.getCurrentDataAsString("PRLINENUM"))
                         + "\n STORELOC = " + str(data.getCurrentDataAsString("STORELOC")))

    
    data.setParentAsCurrent()




#---------------------------------------------------------------------------------------------
# Add Missing Lines 
#
#------------------------------------------------------------------------------------------
def addMissingLines(data,PONUM,MessageLineNum):
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-addMissingLines - Started - PO:" + str(PONUM))
    #get Revision number
    #revisionNum=""
    #if (data.isInCurrentData("STATUS") and not data.isCurrentDataNull("STATUS")):
    #    status = data.getCurrentData("STATUS")
    ##    if status=='CAN':
    #        revisionNum = data.getCurrentDataAsInt("REVISIONNUM")
    #    else:
    #        revisionNum = data.getCurrentDataAsInt("REVISIONNUM") - 1
    #elif (data.isInCurrentData("REVISIONNUM") and not data.isCurrentDataNull("REVISIONNUM")):
    #    revisionNum = data.getCurrentDataAsInt("REVISIONNUM")



    ## get Site ID
    siteId=""
    if (data.isInCurrentData("SITEID") and not data.isCurrentDataNull("SITEID")):
        siteId = data.getCurrentData("SITEID")
    else:
        siteId = "DM"

    
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-addMissingLines - \n"                 
                 + "Siteid=" + str(siteId) + "\n")
    
    if not siteId:
        ctx.error("", "ERROR", ["No Site or Revision found."])
    
    

    PO = getPO(PONUM,siteId)
    if (PO):
        POLines = PO.getMboSet('POLINE')
        
        logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-addMissingLines - Message Lines\n" +  str(MessageLineNum))
        
        #if POLines.count() > len(MessageLineNum):
        POLine = POLines.moveFirst()
        while POLine:
            if not POLine.getInt('POLINENUM') in MessageLineNum:
                addPOLine(data,POLine)

            POLine = POLines.moveNext()
        


#-----------------------------------------------------------------------------------------
# Converting the incoming status values to Maximo internal statuses
#-----------------------------------------------------------------------------------------
def convertStatus(erData):
    if erData.isInCurrentData("DM_GRPSTATUS") and not erData.isCurrentDataNull("DM_GRPSTATUS"):
        status = erData.getCurrentDataAsString("DM_GRPSTATUS").strip()
        
        if status == "REQUIRES REAPPROVAL":
            erData.setCurrentData("STATUS", "RETURNED")
            logger.debug("STATUS changed to WAPPR")
        elif status == "APPROVED":
            erData.setCurrentData("STATUS", "APPR")
            logger.debug("STATUS changed to APPR")
        elif status == "IN PROCESS":
            erData.setCurrentData("STATUS", "INPRG")
            logger.debug("STATUS changed to INPRG")
        elif status == "REJECTED":
            erData.setCurrentData("STATUS", "CAN")
            logger.debug("STATUS changed to CAN")
        elif status == "INCOMPLETE":
            erData.setCurrentData("STATUS", "WAPPR")
            logger.debug("STATUS changed to CAN")
        
    if erData.isInCurrentData("CLOSEDCODE") and not erData.isCurrentDataNull("CLOSEDCODE"):
        closecode = erData.getCurrentDataAsString("CLOSEDCODE").strip()
        if closecode =="FINALLY CLOSED" :
            erData.setCurrentData("STATUS", "CLOSE")

def checkingRevision(erData):
    try:
        incomingRev = erData.getCurrentDataAsInt("REVISIONNUM")
        ponum = erData.getCurrentDataAsString("PONUM")
        siteid = erData.getCurrentDataAsString("SITEID")

        logger.debug("****Incoming REVISIONNUM: " + str(incomingRev))
        logger.debug("****ponum : " + str(ponum))
        logger.debug("****siteid : " + str(siteid))
        poSet = MXServer.getMXServer().getMboSet("PO", MXServer.getMXServer().getSystemUserInfo())
        where = SqlFormat(poSet.getUserInfo(), "PONUM = :1 AND SITEID = :2")
        where.setObject(1, "PO", "PONUM", ponum)
        where.setObject(2, "PO", "SITEID", siteid)
        poSet.setWhere(where.format())
        poSet.reset()
        logger.debug("** po getwhere is  " +poSet.getWhere()  )
        poSet.setOrderBy("REVISIONNUM desc")
        logger.debug("Incoming REVISIONNUM: " + str(incomingRev))
        if not poSet.isEmpty():
            po = poSet.moveFirst()
            maxRev = po.getInt("REVISIONNUM")
            logger.debug("Existing Max REVISIONNUM: " + str(maxRev))

            if incomingRev > maxRev:
                erData.setCurrentData("REVCOMMENTS", "PO revision "+str(incomingRev)+" revised from GRP.")
                #erData.setCurrentData("STATUS","PNDREV")
                logger.debug("REVCOMMENTS set for new revision")

        poSet.close()
    except Exception as e:
        logger.error("Error in checkAndSetRevisionComments: " + str(e))

def setBusinessValues(erData):
    if erData.isInCurrentData("POTYPE") and not erData.isCurrentDataNull("POTYPE"):
        poType = erData.getCurrentDataAsString("POTYPE")
        if poType == "BLANKET":
            if erData.isInCurrentData("DM_GRPRELEASENUM") and not erData.isCurrentDataNull("DM_GRPRELEASENUM"):
                ReleaseNum =  erData.getCurrentDataAsInt("DM_GRPRELEASENUM")
                PO =  erData.getCurrentDataAsString("PONUM")
                erData.setCurrentData("PONUM",PO + "-" + str(ReleaseNum))




    if erData.isInCurrentData("ORDERUNIT") and not erData.isCurrentDataNull("ORDERUNIT"):
        erData.setCurrentData("ORDERUNIT",getMaximoUoM(erData.getCurrentDataAsString("ORDERUNIT")))



    '''
    Remove for Reduced Reciving Processing 
    if erData.isInCurrentData("DM_ROUTINGNAME") and not erData.isCurrentDataNull("DM_ROUTINGNAME"):
        RoutingName = erData.getCurrentDataAsString("DM_ROUTINGNAME")
        if RoutingName == "Inspection Required":
            erData.setCurrentData("INSPECTIONREQUIRED","1")
    '''
    logger.debug("**** in business def****")
    

def getPrLineDetails(siteId, poNumber, poLineNumber):
        
    prLine = None
    exactMatch= False

    userInfo = MXServer.getMXServer().getSystemUserInfo()
    if (siteId is None or poNumber is None ):
        return prLine,exactMatch
                        
    # Fetch PR line details
    sqlFormat = SqlFormat(userInfo, "DM_GRPPONUM = :1 AND DM_GRPPOLINENUM = :2 AND SITEID = :3")
    sqlFormat.setObject(1, "prLine", "DM_GRPPONUM",  poNumber)
    sqlFormat.setObject(2, "prLine", "DM_GRPPOLINENUM",  poLineNumber)
    sqlFormat.setObject(3, "prLine", "siteid",  siteId)
        
    prLineSet = MXServer.getMXServer().getMboSet("prLine", userInfo)
    prLineSet.setWhere(sqlFormat.format())
    prLineSet.reset()
        
    if (not prLineSet.isEmpty()):
        prLine = prLineSet.getMbo(0)
        exactMatch= True
    else:
        exactMatch= False
        sqlFormat = SqlFormat(userInfo, "DM_GRPPONUM = :1  AND SITEID = :2")
        sqlFormat.setObject(1, "prLine", "DM_GRPPONUM",  poNumber)
        sqlFormat.setObject(2, "prLine", "siteid",  siteId)
        prLineSet.setWhere(sqlFormat.format())
        prLineSet.reset()
        prLine = prLineSet.moveFirst()
        

        
    prLineSet.close()
                    
    return prLine ,exactMatch
        


    
def skipRule(erData):
    if erData.isInCurrentData("DM_GRPSTATUS") and not erData.isCurrentDataNull("DM_GRPSTATUS"):
        status = erData.getCurrentDataAsString("DM_GRPSTATUS").strip()
        
        if status == "REQUIRES REAPPROVAL" or status == "IN PROCESS" or status == "INCOMPLETE":
            logger.debug("PO is not in Approve Status , Skipping Transaction")
            service.raiseSkipTransaction()


    
           
        

# setting default error at the end            
def logErData(erData):
    try: 
        logger.debug("===== Pretty Printed erData before =====")
        logger.debug(XMLOutputter().outputString(erData.getData()))
        logger.debug("===== Pretty Printed erData After =====")
    except Exception, e:
        logger.error("Error while printing erData XML: " + str(e))

def isStore(erData):
    if erData.isInCurrentData("STORELOC") and not erData.isCurrentDataNull("STORELOC") and not erData.getCurrentDataAsString("STORELOC") == "M00":
        userInfo = MXServer.getMXServer().getSystemUserInfo()
                            
        sqlFormat = SqlFormat(userInfo, "LOCATION = :1 AND type = 'STOREROOM' AND SITEID = :2")
        sqlFormat.setObject(1, "LOCATIONS", "LOCATION",  erData.getCurrentDataAsString("STORELOC"))        
        sqlFormat.setObject(2, "LOCATIONS", "siteid",  "DM")
            
        LocationsSet = MXServer.getMXServer().getMboSet("LOCATIONS", userInfo)
        LocationsSet.setWhere(sqlFormat.format())
        LocationsSet.reset()
        if LocationsSet.moveFirst():
            LocationsSet.cleanup()
            LocationsSet.close()
            return True
        else:
            LocationsSet.cleanup()
            LocationsSet.close()
            return False
    else:
        return False


#-----------------------------------------------------------------------------------------
# Main Execution
#-----------------------------------------------------------------------------------------
erData.breakData()
logger.debug("** Parent Data **"+erData.getCurrentAction())
logErData(erData)
skipRule(erData)
mandatoryChecks(erData)
setDefaultValues(erData)
convertStatus(erData)
checkingRevision(erData)
setBusinessValues(erData)

# manipulating childern Data 
ponum=erData.getCurrentDataAsString("PONUM")
revnum=erData.getCurrentDataAsInt("REVISIONNUM")


logger.debug("*****revnumafter **"+str(revnum))
'''
lastUpdateDate=erData.getCurrentDataAsDate("DM_LASTUPDATEDATE")
if lastUpdateDate:
    formatter = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss")
    formattedDate = formatter.format(lastUpdateDate)
    logger.debug("*****revnumafter1 **"+str(formattedDate))
'''
poLineList=erData.getChildrenData("POLINE")
noOfPOLines=poLineList.size()

MessageLineNum = []
LinesToBeDeleted = []
if (poLineList is not None and noOfPOLines > 0):
    for i in range(noOfPOLines):        
        erData.setAsCurrent(poLineList,i)

        erData.setCurrentData("TOSITEID", "DM")       
        cancelflag=erData.getCurrentDataAsInt("CANCELFLAG")
        if cancelflag ==1:
            erData.setCurrentAction("Delete")
            LinesToBeDeleted.append(i)
         # linetype  logic
        linetype=erData.getCurrentDataAsString("LINETYPE")
        itemnum= None
        if erData.isInCurrentData("ITEMNUM") and not erData.isCurrentDataNull("ITEMNUM"):
            itemnum=erData.getCurrentDataAsString("ITEMNUM") 


        polinenum=erData.getCurrentDataAsInt("POLINENUM")

        MessageLineNum.append(erData.getCurrentDataAsInt("POLINENUM"))

        isITStoreLoc = isStore(erData)
        if not isITStoreLoc:
            erData.setCurrentDataNull("STORELOC")
            erData.setCurrentData("CONVERSION", "1")

        if itemnum is not None and itemnum != ""  :
            erData.setCurrentData("LINETYPE", "ITEM")
        elif linetype == "Quantity" and (itemnum is None or itemnum==""):

            erData.setCurrentData("LINETYPE", "MATERIAL")
            erData.setCurrentDataNull("STORELOC")
            erData.setCurrentData("CONVERSION", "1")
        
        else:
            erData.setCurrentData("LINETYPE", "SERVICE")
            erData.setCurrentDataNull("STORELOC")
            erData.setCurrentData("CONVERSION", "1")
        
        ## linking PO to PR
        prLine,exactMatch = getPrLineDetails("DM",ponum,str(polinenum))
        if prLine and exactMatch:
            logger.debug("**Skiping the transcation there is no GRPPONUM in POLines **")
            erData.setCurrentData("PRNUM",prLine.getString("PRNUM") )
            erData.setCurrentData("PRLINENUM", prLine.getString("PRLINENUM"))
        elif not prLine:
            logger.debug("**Skiping the transcation there is no GRPPONUM in POLines **")
            service.raiseSkipTransaction()
        logger.debug("**line2 child Data **"+erData.getCurrentAction())
    erData.setParentAsCurrent()


addMissingLines(erData,erData.getCurrentDataAsString("PONUM"),MessageLineNum)
DeleteLines(erData,LinesToBeDeleted)
#if revnum > 0:
#    erData.setCurrentAction("Replace")

logErData(erData)
logger.debug("============= SYNC.GRPPOINTERFACE.USEREXIT.IN.BEFORE: END =============")