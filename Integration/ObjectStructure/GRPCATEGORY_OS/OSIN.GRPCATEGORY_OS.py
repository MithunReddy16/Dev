#-----------------------------------------------------------------------------------------
# Script Name : OSIN.GRPCATEGORY_OS
# Description : OBJECT STRUCTURE In script for GRPCATEGORY_OS inbound interface.
#
# Enterprise Service : GRPCATEGORY_ES
# Object Structure   : GRPCATEGORY_OS
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
from psdi.util import MXException


logger = MXLoggerFactory.getLogger("maximo.integration.userexit")
logger.debug("============= OSIN.GRPCATEGORY_OS: START=============")

from psdi import server 
from psdi.server import MXServer 
from psdi import mbo 
def beforeProcess(ctx):
	mxServer = MXServer.getMXServer()
	mbo = ctx.getMbo()
	parent=None
	commodityCode=ctx.getData().getCurrentData("COMMODITY") 
	description=ctx.getData().getCurrentData("DESCRIPTION") 
	cg = commodityCode.split("-")[1]
	
	#ctx.error("ASSET", cg, None)
	#below commented on 02March26
	#if (cg is not None and cg!='000'):
	parent = commodityCode.split("-")[0]
	ctx.getData().setCurrentData("PARENT",parent)
	
	mboSet = mxServer.getMboSet("COMMODITIES", mxServer.getSystemUserInfo())
	mboSet.setWhere("COMMODITY='"+parent+"' ");
	mboSet.reset();
	if (mboSet.isEmpty()):
	    if parent is not None and parent!="" :
    		parentCommodityMbo = mboSet.add()
    		parentCommodityMbo.setValue("ITEMSETID", "ITEMSET", 11L)
    		parentCommodityMbo.setValue("COMMODITY", parent, 2L)
    		parentCommodityMbo.setValue("DESCRIPTION", description , 11L)
    		parentCommodityMbo.setValue("DM_CLASS", parent[:3], 11L)
    		mboSet.save()
    		
	logger.debug("============= OSIN.GRPCATEGORY_OS: END=============")