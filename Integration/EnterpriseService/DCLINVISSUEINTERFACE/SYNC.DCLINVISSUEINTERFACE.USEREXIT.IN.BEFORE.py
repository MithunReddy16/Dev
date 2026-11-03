#-----------------------------------------------------------------------------------------
# Script Name:SYNC.DCLINVISSUEINTERFACE.USEREXIT.IN.BEFORE
# Description: Set default values for inbound CRM data
#
# Enterprise Service: DCLINVISSUEInterface
#
# Author: Mithun
# Date: 13-July-2026
#*****************************************************************************************
from psdi.server import MXServer
from psdi.util.logging import MXLoggerFactory
from psdi.mbo import SqlFormat
from java.text import SimpleDateFormat

logger = MXLoggerFactory.getLogger("maximo.custom.inventory")

def setError(Msg):
    params = [Msg]
    service.error('scriptval', 'scriptvalidationerror', params)

def mandatoryChecks(jsonData):
    
    qty = jsonData.get("QUANTITY")
    logger.debug("***mandatorychecks def***"+qty)
    if qty is None or str(qty).strip() == "":
        setError("Quantity Field is Empty .")

def setDefaultValues(jsonData):
    logger.debug("Setting default values if missing...")
    jsonData.put("ORGID", "DMORG")
    jsonData.put("SITEID", "DM")
    jsonData.put("SENDERSYSID", "DCL")
    jsonData.put("ISSUETYPE", "ISSUE")
    jsonData.put("GLDEBITACCT", "07-000-0000-00000-00-00000-00000-00000")
    jsonData.put("GLCREDITACCT", "07-000-0000-00000-00-00000-00000-00000")
    if jsonData.get("ACTUALDATE") is None:
        sdf = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss")
        jsonData.put("ACTUALDATE", sdf.format(MXServer.getMXServer().getDate()))
    if jsonData.get("STORELOC") is None:
        jsonData.put("STORELOC", "M01")

def setBusinessValues(jsonData):
    logger.debug("**** in business def****")
    binnum = jsonData.get("BINNUM")
    if binnum is None or str(binnum).strip() == "":
        itemnum = jsonData.get("ITEMNUM")
        location = "M01"
        userInfo = MXServer.getMXServer().getSystemUserInfo()
        invbalSet = MXServer.getMXServer().getMboSet("INVBALANCES", userInfo)
        sqlFormat = SqlFormat(userInfo, "ITEMNUM = :1 and LOCATION = :2")
        sqlFormat.setObject(1, "INVBALANCES", "ITEMNUM", itemnum)
        sqlFormat.setObject(2, "INVBALANCES", "LOCATION", location)
        invbalSet.setWhere(sqlFormat.format())
        invbalSet.reset()
        if not invbalSet.isEmpty():
            qty = float(str(jsonData.get("QUANTITY")))
            invbalMbo = invbalSet.moveFirst()
            while invbalMbo is not None:
                curbal = invbalMbo.getDouble("CURBAL")
                if curbal >= qty:
                    bin = invbalMbo.getString("BINNUM")
                    jsonData.put("BINNUM", bin)
                    break
                invbalMbo = invbalSet.moveNext()
        invbalSet.close()

#-----------------------------------------------------------------------------------------
# Main Execution
#-----------------------------------------------------------------------------------------
erData.breakData()
size = erData.getSize()
"""
for i in range(size):
    so = erData.getStructureObject(i)
    itemnum = so.getCurrentDataAsString("ITEMNUM")
    qty = so.getCurrentDataAsDouble("QUANTITY")
    logger.debug("***mandatorychecks def1***"+str(itemnum))
    logger.debug("***mandatorychecks def2***"+str(qty))
    if qty is None or str(qty).strip() == "":
        setError("Quantity Field is Empty .")
"""    

logger.debug("***Final erData: " + str(erData.getDataAsString()))
logger.debug("============= SYNC.DCLINVISSUEINTERFACE.USEREXIT.IN.BEFORE: END =============")