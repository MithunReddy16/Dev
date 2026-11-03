#-----------------------------------------------------------------------------------------
# Name:        SYNC.GRPPORECEIPTInterface.USEREXIT.IN.BEFORE
# Description: Set default values for inbound GR data (XML-based)
#
# Enterprise Service: GRPPORECEIPTInterface
# Event: Integration --> Enterprise Service --> Request --> User Exit --> Before External Exit
#
# Author: Amir Anwar.
#-----------------------------------------------------------------------------------------

'''
* Manage trans type
* Manage Status ( COMP, winsp , WASSET)
* Manage External ref iD ( done)
* Manage Inspection on PO ( done)
* Change Relase num ( done)
* Changes to UI for adding External Ref - shipment etc..
'''

'''
skipped transaction might need to be created in Maximo for tracking purpise of parent - child
Trans TYpes
1.	RETURN TO VENDOR
2.	DELIVER
3.	TRANSFER ( NA within PO receipting)
4.	REJECT ( to maximo this is similar to return to vendor so it will be skipped)
5.	RETURN TO RECEIVING (  This could be void in case delievered)
6.	UNORDERED (Transaction of un existing PO is not permitted in Maximo hence skipped)
7.	ACCEPT ( to maximo this is similar to deliver so it will be skipped)
8.	CORRECT
9.	RECEIVE ( in maximo if item is not require inspection then Receive  delivery )

'''

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

logger = MXLoggerFactory.getLogger("maximo.custom")
logger.debug("============= SYNC.GRPPORECEIPTInterface.USEREXIT.IN.BEFORE: START =============")

userInfo = MXServer.getMXServer().getSystemUserInfo()

def getMaximoUoM(UOM):
    MaximoUoM = UOM
    UoMSet = MXServer.getMXServer().getMboSet("MEASUREUNIT", MXServer.getMXServer().getSystemUserInfo())
    where = SqlFormat(UoMSet.getUserInfo(), "DM_GRPUNITID = :1")
    where.setObject(1, "MEASUREUNIT", "DM_GRPUNITID", UOM)
    
    UoMSet.setWhere(where.format())
    UoMSet.reset()
    
    UoMMbo = UoMSet.moveFirst()
    if UoMMbo and not UoMMbo.isNull('MEASUREUNITID'):
        MaximoUoM = UoMMbo.getString('MEASUREUNITID')
    UoMSet.cleanup()
    UoMSet.close()
    
    return  MaximoUoM


#-----------------------------------------------------------------------------------------
# get the PO 
#
# @param Mbo (poNum) The PO Number
# @param Mbo (siteId) The Organization
#-----------------------------------------------------------------------------------------
def getPO(poNum,POHeaderID, siteId):
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-getPO\n" + " - PO1111: " + str(poNum))

    #whereclause = "ponum = :1 and siteid = :2" 
    #whereclause = whereclause + " and revisionnum = (select max(revisionnum) from po where ponum = :1 and siteid = :2 "
    
    whereclause = "(PONUM=:1 OR DM_GRPHEADERID = :2) and siteid = :3" 
    whereclause = whereclause + " and revisionnum = (select max(revisionnum) from po where (PONUM=:1 OR DM_GRPHEADERID = :2) and siteid = :3 "
    
    whereclause = whereclause + " and status not in (select value from synonymdomain where domainid = 'POSTATUS' and maxvalue in ('CAN', 'REVISE', 'CLOSE')))"
    
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-getPO\n" + " - whereclause: " + whereclause)
    
    
    sqlFormat = SqlFormat(userInfo, whereclause)    
    sqlFormat.setObject(1, "PO", "ponum", poNum)
    sqlFormat.setObject(2, "PO", "DM_GRPHEADERID", POHeaderID)
    sqlFormat.setObject(3, "PO", "siteid", siteId)
    
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-getPO\n" + " - whereclause: " + sqlFormat.format())

    pos = MXServer.getMXServer().getMboSet("PO", userInfo)
    pos.setWhere(sqlFormat.format())
    pos.reset()
    
    

    PO = pos.getMbo(0)

    if PO :
        logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-getPO\n" + " PO FOund")
        return PO
    
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-getPO\n" + " PO NOT FOund!!")    
    return None


def isDMPO(poNum, siteId):
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-isDMPO\n" + " - PO: " + str(poNum))

    whereclause = "ponum = :1 and siteid = :2" 
    #whereclause = whereclause + " and revisionnum = (select max(revisionnum) from po where ponum = :1 and siteid = :2 "
    whereclause = whereclause + " and status not in (select value from synonymdomain where domainid = 'POSTATUS' and maxvalue in ('CAN', 'REVISE', 'CLOSE'))"
    
    sqlFormat = SqlFormat(userInfo, whereclause)    
    sqlFormat.setObject(1, "PO", "ponum", poNum)
    sqlFormat.setObject(2, "PO", "siteid", siteId)
    #sqlFormat.setObject(3, "PO", "revisionnum", revisionNum)
    
    pos = MXServer.getMXServer().getMboSet("PO", userInfo)
    pos.setWhere(sqlFormat.format())
    pos.reset()

    if pos.moveFirst():
        logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-isDMPO eNDED - PO FOUND\n")
        return True
    
    prLineSet = MXServer.getMXServer().getMboSet("prLine", userInfo)
    prLineSet.setWhere(sqlFormat.format())
    prLineSet.reset()

    sqlFormat = SqlFormat(userInfo, "DM_GRPPONUM = :1  AND SITEID = :2")
    sqlFormat.setObject(1, "prLine", "DM_GRPPONUM",  poNum)
    sqlFormat.setObject(2, "prLine", "siteid",  siteId)
    prLineSet.setWhere(sqlFormat.format())
    prLineSet.reset()
    if prLineSet.moveFirst() :
        logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-isDMPO eNDED - po fOUND\n")
        return True
    
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-isDMPO eNDED - PO NOT FOUND\n")
    
    return  False


def getPOLine(erData):
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-getPOLine start\n")
    ponum = erData.getCurrentDataAsString("PONUM") 

    if erData.isInCurrentData("DM_GRPRELEASENUM") and not erData.isCurrentDataNull("DM_GRPRELEASENUM"):
        ReleaseNum =  erData.getCurrentDataAsInt("DM_GRPRELEASENUM")
        ponum =ponum + "-" + str(ReleaseNum)

    POHeaderID = erData.getCurrentDataAsString("DM_POHEADERID")
    PO = getPO(ponum,POHeaderID,"DM")
    if PO :
        poLineSet =PO.getMboSet("POLINE")
        polinenum = erData.getCurrentDataAsString("POLINENUM")
        whereclause = "polinenum=:1"
        sqlFormat = SqlFormat(userInfo, whereclause)

        sqlFormat.setObject(1, "POLINE", "POLINENUM", polinenum)

        poLineSet.setWhere(sqlFormat.format())
        poLineSet.reset()
        POline = poLineSet.moveFirst()
        if POline:
            logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-getPOLine end PO LINE FOUND\n")
            return POline
        logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-getPOLine end - NO POLINE FOUND\n")
        return None
    else:
        logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-getPOLine end- No PO FOUND\n")
        return None
    



    
def getItemRecord(ItemNum):
    itemMbo = None

    ItemMboSet = MXServer.getMXServer().getMboSet("ITEM", userInfo)
    whereclause = "ITEMNUM = :1 "
    
    sqlFormat = SqlFormat(userInfo, whereclause)
    sqlFormat.setObject(1, "ITEM", "ITEMNUM", ItemNum)
    
    ItemMboSet.setWhere(sqlFormat.format())
    ItemMboSet.reset()
    itemMbo = ItemMboSet.moveFirst()
    if itemMbo:
        return itemMbo
    else:
        return None
    

#-----------------------------------------------------------------------------------------
# Return original receipt Mbo
#
# @param String (tableName) The table MATRECTRANS or SERVRECTRANS.
# @param StructureData (data) The data consists the EXTERNALREFID of original receipt.
#-----------------------------------------------------------------------------------------
def getOrigReceipt(tableName, data):
    logger.debug("\n\r!!! INV-LIB-SCRIPT-getOrigReceipt\n" + " - for: " + tableName)

    if (not data.isInCurrentData("DM_PARENTID") or data.isCurrentDataNull("DM_PARENTID")):
        return None
        
    OrgReceiptID = data.getCurrentDataAsString("DM_PARENTID")
    ponum = data.getCurrentDataAsString("PONUM")
    '''
    if erData.isInCurrentData("DM_GRPRELEASENUM") and not erData.isCurrentDataNull("DM_GRPRELEASENUM"):
        if not '-' in ponum:
            ReleaseNum =  erData.getCurrentDataAsInt("DM_GRPRELEASENUM")
            ponum =erData.getCurrentDataAsString("PONUM") + "-" + str(ReleaseNum)
    
    '''
    POLineNum = data.getCurrentDataAsString("POLINENUM")
    #voidWhere = "issuetype = 'RECEIPT' "    
    voidWhere = " externalrefid = :1 "
    voidWhere = voidWhere + " AND PONUM=:2 AND POLINENUM=:3 AND POSITEID='DM' AND SITEID='DM' "
    
    sqlFormat = SqlFormat(userInfo, voidWhere)
    sqlFormat.setObject(1, tableName, "externalrefid",OrgReceiptID )
    sqlFormat.setObject(2, tableName, "ponum",ponum )
    sqlFormat.setObject(3, tableName, "polinenum",POLineNum )
    
    recSet = MXServer.getMXServer().getMboSet(tableName, userInfo)
    recSet.setWhere(sqlFormat.format())
    recSet.reset()
    
    logger.debug("\n\r!!! INV-LIB-SCRIPT-getOrigReceipt\n" + " -  Where: " + recSet.getCompleteWhere())

    PrimaryKey = tableName + 'id'

    origRec = recSet.getMbo(0)
    '''
    if (not origRec ):
            logger.debug("\n\r!!! INV-LIB-SCRIPT-getOrigReceipt\n" + " -  NO Source Transaction Found - seeking different route")
            voidWhere = "" 
            voidWhere = voidWhere + "positeid = :1 "
            voidWhere = voidWhere + "and ponum = :2 "
            voidWhere = voidWhere + "and porevisionnum = (select revisionnum from po where siteid = :1 and ponum = :2 and status = 'APPR') "
            voidWhere = voidWhere + "and polinenum = :3 "
            voidWhere = voidWhere + "and issuetype = 'RECEIPT' "
            voidWhere = voidWhere + "and quantity = :4 " 
            voidWhere = voidWhere + "and "+PrimaryKey+" not in "
            voidWhere = voidWhere + "("
            voidWhere = voidWhere + "select receiptref from "+tableName+" matrectrans2 "
            voidWhere = voidWhere + "where matrectrans2.positeid = :1 "
            voidWhere = voidWhere + "and matrectrans2.ponum = :2 "
            voidWhere = voidWhere + "and matrectrans2.porevisionnum = (select revisionnum from po where siteid = :1 and ponum = :2 and status = 'APPR') "
            voidWhere = voidWhere + "and matrectrans2.polinenum = :3 "
            voidWhere = voidWhere + "and matrectrans2.issuetype = 'RETURN'"
            voidWhere = voidWhere + ")"
                    
            sqlFormat = SqlFormat(userInfo, voidWhere)
            sqlFormat.setObject(1, tableName, "siteid", "DM")
            sqlFormat.setObject(2,tableName, "ponum", data.getCurrentDataAsString("PONUM"))
            sqlFormat.setObject(3, tableName, "polinenum", str(data.getCurrentDataAsInt("POLINENUM")))
            sqlFormat.setObject(4, tableName, "quantity", data.getCurrentDataAsString("RECEIPTQUANTITY"))
            
            matRecSet = MXServer.getMXServer().getMboSet(tableName, userInfo)
            matRecSet.setWhere(sqlFormat.format())

            origRec = matRecSet.getMbo(0)
            matRecSet.close()
        
            
            
            logger.debug("\n\r!!! SYNC.GRPPORECEIPTInterface.USEREXIT.IN.BEFORE\n" + " - Void Where 2: " + str(matRecSet.getWhere())) 
    '''
    if not origRec:
        logger.debug("\n\r!!! INV-LIB-SCRIPT-getOrigReceipt\n" + " -  NO Source Transaction Found -")

    return origRec

def mandatoryChecks(erData):
    logger.debug("***SYNC.GRPPORECEIPTInterface.USEREXIT.IN.BEFORE ==>> mandatoryChecks Starts***")
    #isInCurrentData
    #if erData.isCurrentDataNull("ITEMNUM"):
     #   raise MXApplicationException("userexit", "missingitemnum")
    #if erData.isCurrentDataNull("TOSTORELOC"):
     #   raise MXApplicationException("userexit", "missingtostoreloc")
    #receiptQty = erData.getCurrentDataAsDouble("RECEIPTQUANTITY")
    #if receiptQty < 0:
        #raise MXApplicationException("userexit", "negativereceiptqty")
    
    logger.debug("***SYNC.GRPPORECEIPTInterface.USEREXIT.IN.BEFORE ==>> mandatoryChecks Starts***")
    



#-----------------------------------------------------------------------------------------
# Set default values for missing fields in inbound XML
#-----------------------------------------------------------------------------------------
def setDefaultValues(erData):
    logger.debug("Setting default values if missing...")

    if not erData.isInCurrentData("SITEID")  or erData.isCurrentDataNull("SITEID"):
        erData.setCurrentData("SITEID", "DM")
        logger.debug("**SITEID defaulted to DM")
    
    if not erData.isInCurrentData("POSITEID")  or erData.isCurrentDataNull("POSITEID"):
        erData.setCurrentData("POSITEID", "DM")
        logger.debug("**POSITEID defaulted to DM")
    
    if not erData.isInCurrentData("SOURCESYSID")  or erData.isCurrentDataNull("SOURCESYSID"):
        erData.setCurrentData("SOURCESYSID", "GRP")
        logger.debug("**SOURCESYSID defaulted to GRP")
    
    
    #erData.setCurrentData("EXTERNALREFID", erData.getCurrentDataAsString("DM_RECEIPTNUM") + "/" + erData.getCurrentDataAsString("POLINENUM"))
    
    erData.setCurrentData("ENTERBY", "MAXADMIN")
    logger.debug("**ENTERBY defaulted to MAXADMIN")

def setBusinessValues(erData,POLine):
    
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-setBusinessValues START\n")
    # Set Quantity negative for Return
    receiptQty = erData.getCurrentDataAsDouble("RECEIPTQUANTITY")
    TransType = erData.getCurrentDataAsString("ISSUETYPE")
    if TransType == "RETURN":
        receiptQty = (-1 * receiptQty)

    '''
    ##Moved to GRPRECInterface
    if erData.isInCurrentData("DM_GRPRELEASENUM") and not erData.isCurrentDataNull("DM_GRPRELEASENUM"):
        ReleaseNum =  erData.getCurrentDataAsInt("DM_GRPRELEASENUM")
        ponum =erData.getCurrentDataAsString("PONUM") + "-" + str(ReleaseNum)
        erData.setCurrentData("PONUM",  ponum)

    '''
    # Set Qanitity field
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-setBusinessValues -Set Qanitity field\n")
    linetype=None
    if POLine:
        erData.setCurrentData("PONUM",  POLine.getString("PONUM"))

        linetype = POLine.getString("LINETYPE")
        erData.setCurrentData("LINETYPE", linetype)
        #if linetype in ("ITEM", "MATERIAL") :
        #    erData.setCurrentData("LINETYPE", linetype)
           
        if linetype in ( "SERVICE" ,"STDSERVICE"):            
            erData.setCurrentDataNull("RECEIPTQUANTITY")
            erData.setCurrentData("QTYTORECEIVE", receiptQty)
        
        if linetype == "MATERIAL":
            erData.setCurrentDataNull("GLCREDITACCT")
            erData.setCurrentData("GLDEBITACCT", POLine.getString('GLDEBITACCT'))

            
    # process for M00:
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-setBusinessValues -M00\n")
    if erData.isInCurrentData("TOSTORELOC") and not erData.isCurrentDataNull("TOSTORELOC"):
        if erData.getCurrentDataAsString("TOSTORELOC") == "M00":
            erData.setCurrentDataNull("TOSTORELOC")

    # process binnum 
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-setBusinessValues -BIN \n")
    if erData.isInCurrentData("TOBIN") and not erData.isCurrentDataNull("TOBIN"):
        binnum = erData.getCurrentDataAsString("TOBIN")
        if binnum is not None :
            binnum=formatBin(binnum)
            erData.setCurrentData("TOBIN", str(binnum))

    # process UOM 
    if erData.isInCurrentData("RECEIVEDUNIT") and not erData.isCurrentDataNull("RECEIVEDUNIT"):
        erData.setCurrentData("RECEIVEDUNIT",getMaximoUoM(erData.getCurrentDataAsString("RECEIVEDUNIT")))

    # roatating items
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-setBusinessValues -Rotating\n")
    if erData.isInCurrentData("ITEMNUM") and not erData.isCurrentDataNull("ITEMNUM"):
        
        ItemMbo = getItemRecord(erData.getCurrentDataAsString("ITEMNUM"))
        if ItemMbo:
            if ItemMbo.getBoolean("ROTATING") and TransType != "RETURN":
                erData.setCurrentData("STATUS", "WASSET")

            # process usedby and lotnum 
            if not  ItemMbo.isNull("LOTTYPE")  and  ItemMbo.getString("LOTTYPE") == "LOT" :
                logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-setBusinessValues -usedby \n")
                if erData.isInCurrentData("DM_EXPIRYDATE") and not erData.isCurrentDataNull("DM_EXPIRYDATE"):
                    erData.setCurrentData("USEBY", erData.getCurrentDataAsDate("DM_EXPIRYDATE"))

                logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-setBusinessValues -lot \n")
                if erData.isInCurrentData("DM_GRPLOTNUM") and not erData.isCurrentDataNull("DM_GRPLOTNUM"):
                    erData.setCurrentData("TOLOT", erData.getCurrentDataAsString("DM_GRPLOTNUM")[:])

    #Return ReceiptRef
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-setBusinessValues -ReceiptRef\n")
    if linetype and  TransType in ("RETURN","VOID"):
        origRec = None
        if linetype in  ( "SERVICE" ,"STDSERVICE"):  
            origRec = getOrigReceipt("SERVRECTRANS",erData)
        else:
            origRec = getOrigReceipt("MATRECTRANS",erData)
        
        if origRec:
            erData.setCurrentData("RECEIPTREF", str(origRec.getUniqueIDValue()))

    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-setBusinessValues end\n")


    
    
        
def formatBin(binnum) :
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-FORMAT BIN START - bin :" + str(binnum))
    parts = binnum.split('-')
    if len(parts) != 3:
        parts = binnum.split('.')
        logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-FORMAT Bin parts : " + str(parts))
        if len(parts) != 3:
            raise MXApplicationException("userexit", "invalidbinformat")

    first_part = parts[0]  
    second_part = parts[1]  
    third_part = parts[2]   
    
    first_segment = first_part[0]  
    second_segment = first_part[1:]
    third_segment = second_part  
    fourth_segment = third_part  
    
    result = first_segment + '-' + second_segment + '-' + third_segment + '-' + fourth_segment
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-FORMAT BIN END\n")
    return result




def checkSkiprules(erData,POLine):
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-SKIP RULES START\n")
    ponum = erData.getCurrentDataAsString("PONUM")


    if erData.isInCurrentData("ISSUETYPE") and not erData.isCurrentDataNull("ISSUETYPE"):
        if erData.getCurrentDataAsString("ISSUETYPE") == "CORRECT":
            raise MXApplicationException("CORRECT" ,"OrginNotFound")
    
        if erData.getCurrentDataAsString("ISSUETYPE") == "UNORDERED":
            raise MXApplicationException("UNORDERED" ,"NotConfigured")
        
    if erData.isInCurrentData("DM_GRPRELEASENUM") and not erData.isCurrentDataNull("DM_GRPRELEASENUM"):
        ReleaseNum =  erData.getCurrentDataAsInt("DM_GRPRELEASENUM")
        ponum =ponum + "-" + str(ReleaseNum)

    polinenum = erData.getCurrentDataAsString("POLINENUM")
    externalid = erData.getCurrentDataAsString("EXTERNALREFID")  
    

    if not isDMPO(ponum,"DM"):
        logger.debug("\n\r!!! PO is not DM Inventory PO , skipping ....\n")
        service.raiseSkipTransaction()

    

    if POLine:
        logger.debug("** if poset not empty**")
        linetype=POLine.getString("LINETYPE")
        ObjectName = "SERVRECTRANS" if linetype in ["SERVICE","STDSERVICE"] else "MATRECTRANS"
        logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-SKIP RULES,LINETYPE = {} , oBJECTNAME={} \n".format(linetype,ObjectName))
        
        TransactionSet = MXServer.getMXServer().getMboSet(ObjectName, userInfo)
        sqlFormat = SqlFormat(userInfo, "PONUM = :1 and POLINENUM = :2 AND EXTERNALREFID=:3 ")
        sqlFormat.setObject(1, ObjectName, "PONUM", ponum)
        sqlFormat.setObject(2, ObjectName, "POLINENUM",polinenum)
        sqlFormat.setObject(3, ObjectName, "EXTERNALREFID", externalid)
        TransactionSet.setWhere(sqlFormat.format())
        TransactionSet.reset()
        if TransactionSet.moveFirst() :
            logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-SKIP RULES, TRANSATION FOUND SKIPPING\n")
            service.raiseSkipTransaction()
    
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-SKIP RULES END\n")
        
    
        
    

def logErData(erData):
    try:
        logger.debug("===== Pretty Printed erData XML1 =====")
        logger.debug(XMLOutputter().outputString(erData.getData()))
        logger.debug("===== Pretty Printed erData XML2 =====")
    except Exception, e:
        logger.error("Error while printing erData XML: " + str(e))

#-----------------------------------------------------------------------------------------
# Main Execution
#-----------------------------------------------------------------------------------------
erData.breakData()
erData.setAction("Add")
logger.debug("** Parent action **"+str(erData.getAction()))

POLine = getPOLine(erData)
# Moved to GRPRECTransInterface
#checkSkiprules(erData,POLine)

mandatoryChecks(erData)
setDefaultValues(erData)
setBusinessValues(erData,POLine)

logErData(erData)
logger.debug("============= SYNC.GRPPORECEIPTInterface.USEREXIT.IN.BEFORE: END =============")