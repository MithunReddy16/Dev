#-----------------------------------------------------------------------------------------
# Name:        PUBLISH.GRP_PR_OUT.USEREXIT.OUT.AFTER
# Description: Sets formatted values during outbound publish from INVTRANS
#
# Publish Channel: GRP_PR_OUT
# Event: Integration --> Publish Channel --> User Exit --> After External Exit
#
# Author: Mithun Reddy
# Version: 1.0 - 26-Mar-2025
# Version: 2.0 - AA - 26-Mar-2025 - Replace By Feidls with EmployeeID , and Replace None by no value
#-----------------------------------------------------------------------------------------
from psdi.mbo import SqlFormat
from psdi.iface.mic import StructureData
from psdi.server import MXServer
from psdi.util import MXException
from psdi.mbo import MboRemote, MboSetRemote
from psdi.util.logging import MXLoggerFactory
from org.jdom2 import Element
from org.jdom2 import Namespace
from org.jdom2.output import XMLOutputter, Format
from psdi.mbo import MboConstants
from java.sql import SQLException

logger = MXLoggerFactory.getLogger("maximo.integration.userexit")
logger.debug("*** PUBLISH.GRP_PR_OUT.USEREXIT.OUT.AFTER: START ***")

logger.debug(XMLOutputter().outputString(irData.getData()))
logger.debug("*** after erData ***")

erData.breakData()

#mxServer = MXServer.getMXServer()
#userInfo=mxServer.getSystemUserInfo()
logger.debug(XMLOutputter().outputString(erData.getData()))
curMbo = irData.getCurrentMbo()
ns = Namespace.getNamespace("max", "http://www.ibm.com/maximo")
no_ns = Namespace.NO_NAMESPACE

#-----------------------------------------------------------------------------------------
# Get GRP UOM
#-----------------------------------------------------------------------------------------
def getGRPUoM(UOM):
    GRPUoM = UOM
    UoMSet = MXServer.getMXServer().getMboSet("MEASUREUNIT", MXServer.getMXServer().getSystemUserInfo())
    where = SqlFormat(UoMSet.getUserInfo(), "MEASUREUNITID = :1")
    where.setObject(1, "MEASUREUNIT", "MEASUREUNITID", UOM)
    
    UoMSet.setWhere(where.format())
    UoMSet.reset()
    
    UoMMbo = UoMSet.moveFirst()
    if UoMMbo and not UoMMbo.isNull('DM_GRPUNITID'):
        GRPUoM = UoMMbo.getString('DM_GRPUNITID')
    UoMSet.cleanup()
    UoMSet.close()
    
    return  GRPUoM

#-----------------------------------------------------------------------------------------
# Get Employee Number
#-----------------------------------------------------------------------------------------
def getEmployeeID(PersonID):
    EmployeeID = PersonID
    logger.debug("*** getEmployeeID1 ***"+str(PersonID))
    PersonSet = MXServer.getMXServer().getMboSet("PERSON",MXServer.getMXServer().getSystemUserInfo())
    where = SqlFormat(MXServer.getMXServer().getSystemUserInfo(), "PERSONID=:1")
    
    where.setObject(1, "PERSON", "PERSONID", PersonID)
    PersonSet.setWhere(where.format())
    PersonMbo = PersonSet.moveFirst()
    logger.debug("*** getEmployeeID2 ***")
    if PersonMbo:
        if not PersonMbo.isNull("DM_GRPEMPNUM"):
            #EmployeeID =  PersonMbo.getString("DM_GRPEMPNUM")
            EmployeeID =  PersonMbo.getString("DM_GRPEMPNUM")
            
    PersonSet.cleanup()
    PersonSet.close()
    

    return "DM"+EmployeeID
#-----------------------------------------------------------------------------------------
# Set basic transaction data
#-----------------------------------------------------------------------------------------
def setBaseData():
    #PR
    logger.debug("*** basedata1 ***")
    erData.setCurrentData("pReferenceNum", str(irData.getCurrentDataAsString("PRNUM")))
    #erData.setCurrentData("pAuthorizationStatus", str(irData.getCurrentDataAsString("STATUS")))
    erData.setCurrentData("pAuthorizationStatus", "INCOMPLETE")
    #erData.setCurrentData("pAuthorizationStatus", "IN PROCESS")
    if not irData.isCurrentDataNull("VENDOR"):
        erData.setCurrentData("pVendor", str(irData.getCurrentDataAsString("VENDOR")))
    else:
        erData.setCurrentData("pVendor", "")
    erData.setCurrentData("pCurrencyCode", str(irData.getCurrentDataAsString("CURRENCYCODE")))
    erData.setCurrentData("pOrgId", "305")
    
    ## PR Description
    if not irData.isCurrentDataNull("DESCRIPTION"):
        erData.setCurrentData("pDescription", irData.getCurrentDataAsString("DESCRIPTION"))
    else:
        erData.setCurrentData("pDescription","")
        
    #erData.setCurrentData("pPreparerId", str(irData.getCurrentDataAsString("REQUESTEDBY")))
    #erData.setCurrentData("pPreparerId", getEmployeeID(irData.getCurrentDataAsString("REQUESTEDBY")))
    #erData.setCurrentData("pSuggesBuyerId", getEmployeeID(irData.getCurrentDataAsString("REQUESTEDBY")))
    #erData.setCurrentData("P_SUGGESTED_BUYER_USER_NAME", getEmployeeID(irData.getCurrentDataAsString("REQUESTEDBY")))
    logger.debug("*** basedata2 ***")
    #erData.setCurrentData("P_DELIVER_TO_REQUESTOR_USER_NAME", getEmployeeID(irData.getCurrentDataAsString("REQUESTEDBY")))
    #logger.debug("*** basedata2.1 ***"+str(irData.getCurrentDataAsString("PR_REQUESTEDBY")))
    erData.setCurrentData("P_PREPARER_USER_NAME", getEmployeeID(irData.getCurrentDataAsString("REQUESTEDBY")))
    logger.debug("*** basedata3 ***")
    #if not erData.isCurrentDataNull("DM_PURCHASEAGENT"):
    #    erData.setCurrentData("pSuggesBuyerId", getEmployeeID(irData.getCurrentDataAsString("DM_PURCHASEAGENT")))
    #erData.setCurrentData("pDeliverToLocId", str(irData.getCurrentDataAsString("DM_SHIPTO")))
    #erData.setCurrentData("DM_SHIPTO", str(irData.getCurrentDataAsString("DM_SHIPTO")))
    #erData.setCurrentData("REMARK", str(irData.getCurrentDataAsString("REMARK")))
    
    
    
    # GRP FIELDS 
    erData.setCurrentData("pGroupCode", str(irData.getCurrentDataAsString("PRNUM")))
    erData.setCurrentData("pRate", "1")
    erData.setCurrentData("pRateDate", MXServer.getMXServer().getDate())
    erData.setCurrentData("pRateType", "1043")
    erData.setCurrentData("pInterfaceSourceCode", "MAXIMO")
    erData.setCurrentData("pSourceTypeCode", "VENDOR")
    erData.setCurrentData("pGlDate", MXServer.getMXServer().getDate())
    erData.setCurrentData("pRequisitionType", "PURCHASE")
    logger.debug("*** basedata4 ***")
    
    
#-----------------------------------------------------------------------------------------
# Set item number segments
#-----------------------------------------------------------------------------------------
def setItemSegments():
    itemNum = irData.getCurrentDataAsString("ITEMNUM")
    if itemNum is not None:
        DM_ITEMSEG1, DM_ITEMSEG2 = itemNum.split('-', 1)
        erData.setCurrentData("pItemSegment1", DM_ITEMSEG1)
        erData.setCurrentData("pItemSegment2", DM_ITEMSEG2)
    else:
        erData.setCurrentDataNull("pItemSegment1")
        erData.setCurrentDataNull("pItemSegment2")


def destinationTypeCode():
    '''
    storeloc=irData.getCurrentDataAsString("STORELOC")
    if storeloc is not None and storeloc != "" :
        erData.setCurrentData("pDestinationTypeCode", "INVENTORY")
    else :
        erData.setCurrentData("pDestinationTypeCode", "EXPENSE")
    '''
    if irData.isCurrentDataNull("STORELOC"):
        erData.setCurrentData("pDestinationTypeCode", "EXPENSE")
    else:
        erData.setCurrentData("pDestinationTypeCode", "INVENTORY")
    

    
def distinationOrgId() :
    storeloc=irData.getCurrentDataAsString("STORELOC")
    if storeloc is not None and storeloc != "" :
        locSet = MXServer.getMXServer().getMboSet("LOCATIONS", MXServer.getMXServer().getSystemUserInfo())
        where = SqlFormat(locSet.getUserInfo(), "LOCATION = :1 AND TYPE = :2")
        where.setObject(1, "LOCATIONS", "LOCATION", storeloc)
        where.setObject(2, "LOCATIONS", "TYPE", "STOREROOM")
        locSet.setWhere(where.format())
        logger.debug("** storeloc getwhere is  " +locSet.getWhere()  )
        if not locSet.isEmpty():
            locMbo = locSet.moveFirst()
            erData.setCurrentData("pDistinationOrgId", locMbo.getInt("DM_GRPORGID"))
        locSet.close()
    else :
        erData.setCurrentData("pDistinationOrgId", "1481") # M00 grp org id
        
    
def categoryId() :
    commodity = irData.getCurrentDataAsString("COMMODITY")
    logger.debug("** comm ****"+str(commodity))
    if commodity is not None and commodity != "" :
        commSet = MXServer.getMXServer().getMboSet("COMMODITIES", MXServer.getMXServer().getSystemUserInfo())
        where = SqlFormat(commSet.getUserInfo(), "COMMODITY = :1 ")
        where.setObject(1, "COMMODITIES", "COMMODITY", commodity)
        logger.debug("** comm ****1")
        commSet.setWhere(where.format())
        logger.debug("** comm getwhere is  " +commSet.getWhere()  )
        if not commSet.isEmpty():
            commMbo = commSet.moveFirst()
            erData.setCurrentData("PCategoryId",commMbo.getInt("DM_GRPCATEGORYID") )       
        commSet.close()

def setLineType():
    #GRPValues = {"Goods":1,"Tickets":1003,"Rates":1000,"Service":1001,"Qty-Service":1024 , "Off ASG" :1044,"Fixed Price Services" :6,"Outside processing" ,3}
    LineTypeMap = {"ITEM" : "1" , "MATERIAL" : "1" , "SERVICE" : "1001" , "STDSERVICE" : "1001"}
    erData.setCurrentData("pLineType", LineTypeMap[str(irData.getCurrentDataAsString("LINETYPE"))])


def skipRule(irData):
    try:
        # checking for APPR Status

		prnum = irData.getCurrentDataAsString("PRNUM")
		logger.debug("****prnum : " + str(prnum))
		prStatusSet = MXServer.getMXServer().getMboSet("PRSTATUS", MXServer.getMXServer().getSystemUserInfo())
		where = SqlFormat(prStatusSet.getUserInfo(), "PRNUM = :1 AND SITEID = :2 AND STATUS=:3 ")
		where.setObject(1, "PR", "PRNUM", prnum)
		where.setObject(2, "PR", "SITEID", "DM")
		where.setObject(3, "PR", "STATUS", "APPR")
		prStatusSet.setWhere(where.format())
		prStatusSet.reset()
		logger.debug("** pr getwhere is  " +prStatusSet.getWhere()  )
		
		if prStatusSet.count() > 1:
			logger.debug("** SKIPING the TRANSCATION PR is not Present ***")
			service.raiseSkipTransaction()
		prStatusSet.close()
    except Exception as e:
        logger.error("*** Error in checking the PR with APPR status : " + str(e))


"""
def checkIntegratedStatus(prnum):
    
    conn = None
    pstmt = None
    try:
        mxServer = MXServer.getMXServer()
        conKey = mxServer.getSystemUserInfo().getConnectionKey()
        conn = mxServer.getDBManager().getConnection(conKey)
        logger.debug("** PR is  ")
        logger.debug("** PR is  "+prnum)
        prSet = MXServer.getMXServer().getMboSet("PR", MXServer.getMXServer().getSystemUserInfo())
        where = SqlFormat(prSet.getUserInfo(), "PRNUM = :1 ")
        where.setObject(1, "PR", "PRNUM", prnum)
        logger.debug("** PR 2****  "+str(prnum))
        prSet.setWhere(where.format())
        logger.debug("** PR getwhere is  " +prSet.getWhere())
        if not prSet.isEmpty():
            prMbo = prSet.moveFirst()
            logger.debug("** PR getwhere is 1 ")
            if prMbo.getInt("DM_ISINTEGRATED")==1 :
                logger.debug("** PR getwhere is 2 " )
                service.raiseSkipTransaction()
            else :
                sql ="UPDATE PR SET DM_ISINTEGRATED=1 where PRNUM='"+str(prnum)+"' "
                logger.debug("** PR getwhere is 2.1"+sql)
                pstmt = conn.prepareStatement(sql)
                logger.debug("** PR getwhere is 2.2")
                rowsUpdated = pstmt.executeUpdate()
                logger.debug("** PR getwhere is 2.3")
                conn.commit()
                logger.debug("** PR getwhere is  3" )          
        prSet.close()
    except Exception, e:
        if conn is not None:
            conn.rollback()
        logger.debug("*****Error in error in updating DM_ISINTEGRATED in po : " +str(e))
    finally:
        if pstmt is not None:
            pstmt.close()
        if conn is not None:
            conn.close()
    

"""    

#-----------------------------------------------------------------------------------------
# Execute Main 
#-----------------------------------------------------------------------------------------
logger.debug(XMLOutputter().outputString(irData.getData()))
skipRule(irData)
setBaseData()
prnum=irData.getCurrentDataAsString("PRNUM")
#setItemSegments()

# manipulating childern Data 

prLineList=erData.getChildrenData("PRLINE")
noOfPrLines=prLineList.size()
if (prLineList is not None and noOfPrLines > 0):
    for i in range(noOfPrLines):        
        erData.setAsCurrent(prLineList,i)
        
        # PRLINE 
        setItemSegments()
        destinationTypeCode()
        distinationOrgId()
        categoryId()
        setLineType()
        
        erData.setCurrentData("pItemDescription", str(irData.getCurrentDataAsString("DESCRIPTION")))
        if not irData.isCurrentDataNull("ORDERUNIT"):
            erData.setCurrentData("pUnitOfMeasure", getGRPUoM(str(irData.getCurrentDataAsString("ORDERUNIT"))))
        else:
            erData.setCurrentData("pUnitOfMeasure","Each")
            
            
        erData.setCurrentData("pUnitPrice", str(irData.getCurrentDataAsString("UNITCOST")))
        erData.setCurrentData("pQuantity", str(irData.getCurrentDataAsString("ORDERQTY")))
        erData.setCurrentData("pDeliverToLocId", str(irData.getCurrentDataAsString("DM_SHIPTO")))
        
        # PR LINE REMARKS , PR NOTE TO BUYER
        remark = irData.getCurrentDataAsString("REMARK")
        if remark is not None and remark!='':
            erData.setCurrentData("pNoteToBuyer", remark)
        else:
            erData.setCurrentData("pNoteToBuyer", "")
        

        
        # PR Line number
        erData.setCurrentData("pLineNum", str(irData.getCurrentDataAsString("PRLINENUM")))
        #erData.setCurrentData("pDeliverToRequesId", str(irData.getCurrentDataAsString("REQUESTEDBY")))
        '''
        if not irData.isCurrentDataNull("SHIPTOATTN"):
            erData.setCurrentData("pDeliverToRequesId", getEmployeeID(irData.getCurrentDataAsString("SHIPTOATTN")))
        else:
            erData.setCurrentData("pDeliverToRequesId", getEmployeeID(irData.getCurrentDataAsString("REQUESTEDBY")))
        #erData.setCurrentData("pChargeAccountId", str(irData.getCurrentDataAsString("GLDEBITACCT")))
        #logger.debug("***debit*** " + str(irData.getCurrentDataAsString("GLDEBITACCT")))'''
        erData.setCurrentData("P_DELIVER_TO_REQUESTOR_USER_NAME", getEmployeeID(irData.getCurrentDataAsString("REQUESTEDBY")))
        if not irData.isCurrentDataNull("REQDELIVERYDATE"):
            erData.setCurrentData("pNeedByDate", irData.getCurrentDataAsDate("REQDELIVERYDATE"))
        else:
            erData.setCurrentData("pNeedByDate", MXServer.getMXServer().getDate())

        erData.setCurrentData("pCreationDate", str(irData.getCurrentDataAsString("ENTERDATE")))
        
        prLineElement = erData.getCurrentData()  
        logger.debug("*** GLDEBITACCT VALUE***1 " )
        glDebitAcct = prLineElement.getChild("GLDEBITACCT",ns)
        logger.debug("*** GLDEBITACCT VALUE***2 "+str(glDebitAcct ))
        if glDebitAcct is not None:
            logger.debug("*** GLDEBITACCT VALUE***3 " )
            valueElement = glDebitAcct.getChild("VALUE",ns)
            logger.debug("*** GLDEBITACCT VALUE***4 " )
            if valueElement is not None:
                
                logger.debug("*** GLDEBITACCT VALUE***5 " )
                glValue = valueElement.getText()
                '''
                logger.debug("*** GLDEBITACCT VALUE: " + glValue)
                caSet = MXServer.getMXServer().getMboSet("chartofaccounts", MXServer.getMXServer().getSystemUserInfo())
                where = SqlFormat(caSet.getUserInfo(), "glaccount = :1 ")
                where.setObject(1, "chartofaccounts", "glaccount", glValue)
                caSet.setWhere(where.format())
                logger.debug("** Chartofaccounts getwhere is  " +caSet.getWhere())
                if not caSet.isEmpty():
                    caMbo = caSet.moveFirst()
                    logger.debug("** ca getwhere is 1 ")
                    erData.setCurrentData("pChargeAccountId", caMbo.getInt("DM_GLCOMBINATIONID"))
                    '''
                erData.setCurrentData("pChargeAccountSeg", glValue.replace("-", "."))

                #erData.setCurrentData("pChargeAccountId", glValue)
            else:
                logger.debug("*** VALUE tag missing in GLDEBITACCT")
        else:
            logger.debug("*** GLDEBITACCT tag not found")

        
    erData.setParentAsCurrent()    

originalElement = erData.getCurrentData()  
parentElement = originalElement.getParent()


prLines = erData.getChildrenData("PRLINE")
logger.debug("Total PRLINEs found: " + str(prLines.size()))


parentElement.removeContent(originalElement)
logger.debug("Removed original PR from parent.")


for i in range(prLines.size()):
    erData.setAsCurrent(prLines, i)
    prLineElement = erData.getCurrentData() 

    logger.debug("******* Processing PRLINE index: " + str(i))

    
    newPR = Element("PR")
    newPR.setAttribute("action", originalElement.getAttributeValue("action"))
    
    for child in originalElement.getChildren():
        if child.getName() != "PRLINE":
            cloneChild = Element(child.getName(), no_ns)
            cloneChild.setText(child.getText())  
            newPR.addContent(cloneChild)  
    
    for child in prLineElement.getChildren():
        cloneChild = Element(child.getName(),no_ns)
        cloneChild.setText(child.getText())
        newPR.addContent(cloneChild)
        logger.debug("Added field from PRLINE: <" + child.getName() + "> = " + child.getText())

   
    parentElement.addContent(newPR)
    logger.debug("Added new flattened PR to GRP_PR_OUTSet")


#checkIntegratedStatus(prnum)


logger.debug(XMLOutputter().outputString(erData.getData()))

logger.debug("*** PUBLISH.GRP_PR_OUT.USEREXIT.OUT.AFTER: END ***")