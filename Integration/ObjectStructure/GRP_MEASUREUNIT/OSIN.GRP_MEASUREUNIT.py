#-----------------------------------------------------------------------------------------
# Script Name : OSIN.GRP_MEASUREUNIT
# Description : OBJECT STRUCTURE In script for GRP_MEASUREUNIT inbound interface.
#
# Enterprise Service : GRP_MEASUREUNIT
# Object Structure   : GRP_MEASUREUNIT
# Event              : Integration --> Object Structure  --> Inbound--> OSIN 
#
# Author             : Mithun Reddy
# Version            : 1.0
# Date               : 18-Apr-2025
#-----------------------------------------------------------------------------------------

from psdi.util.logging import MXLoggerFactory
from org.jdom2.output import XMLOutputter
from psdi.mbo import SqlFormat
from psdi import server 
from psdi.server import MXServer 
from psdi import mbo 
from psdi.util import MXApplicationException
logger = MXLoggerFactory.getLogger("maximo.integration.userexit")
logger.debug("============= OSIN.GRP_MEASUREUNIT: START=============")

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
    else :
        raise MXApplicationException("userexit", "invalidbaseunit")
    UoMSet.cleanup()
    UoMSet.close()
    
    return  MaximoUoM




def beforeProcess(ctx):
	mxServer = MXServer.getMXServer()
	baseUnit=ctx.getData().getCurrentDataAsString("FROMMEASUREUNIT")
	upperbaseUnit=getMaximoUoM(baseUnit)
	logger.debug("*** logger 1**"+str(upperbaseUnit))
	uomCode=ctx.getData().getCurrentDataAsString("MEASUREUNITID")
	upperuomCode=uomCode.upper()
	logger.debug("*** logger 2**"+str(upperuomCode))
	conversion=ctx.getData().getCurrentDataAsDouble("CONVERSION")
	logger.debug("*** logger 3**"+str(conversion))
	if baseUnit != uomCode:
		logger.debug("*** Units are NOT equal ***")
		conversionMboSet = mxServer.getMboSet("CONVERSION", mxServer.getSystemUserInfo())
		conversionMboSet.setWhere("FROMMEASUREUNIT ='"+upperbaseUnit+"' and TOMEASUREUNIT='"+upperuomCode+"' and CONVERSION="+str(conversion))
		logger.debug(conversionMboSet.getWhere())
		conversionMboSet.reset()
		logger.debug("*** logger3.1 combination count is **"+str(conversionMboSet.count()))
		if conversionMboSet.isEmpty() :
			logger.debug("*** logger3.2 combination count ")
			conversionMbo=conversionMboSet.add()
			conversionMbo.setValue("FROMMEASUREUNIT", upperbaseUnit, 11L)
			conversionMbo.setValue("TOMEASUREUNIT", upperuomCode, 11L)
			conversionMbo.setValue("CONVERSION", conversion, 11L)
			conversionMboSet.save()
			logger.debug("*** logger 4added **FROMMEASUREUNIT ='"+upperbaseUnit+"' and TOMEASUREUNIT='"+upperuomCode+"' and CONVERSION="+str(conversion))

	logger.debug("============= OSIN.GRP_MEASUREUNIT: END=============")