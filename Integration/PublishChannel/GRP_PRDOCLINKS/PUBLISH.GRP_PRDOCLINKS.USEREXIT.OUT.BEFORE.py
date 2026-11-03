############################################
# Script: GRP_PRDOCLINKS Service userexit out
# Author Mithun Reddy 
# Version 1 - 26-03-2025
# Version 2 - Amir - 11-02-2025
###########################################
from com.ibm.tivoli.maximo.oslc.provider import LocalURIGenerator, OslcResourceCache
from psdi.iface.mic import StructureData
from org.jdom2.output import XMLOutputter
from psdi.server import MXServer
from java.lang import String 
from psdi.util import MXException
from psdi.mbo import MboRemote,MboSetRemote
from psdi.util.logging import MXLoggerFactory
#from psdi.webclient.applet.attachimage import Base64
from psdi.mbo import SqlFormat

logger = MXLoggerFactory.getLogger("maximo.integration.userexit")
logger.debug("============= PUBLISH.GRP_PRDOCLINKS.USEREXIT.OUT.BEFORE: START =============")





irData.breakData();
irData.moveToFirstObjectStruture()
StructureExists = True
while StructureExists:
    logger.debug("===== Pretty Printed erData before =====")
    logger.debug(XMLOutputter().outputString(irData.getData()))
    logger.debug("===== Pretty Printed erData After =====")
    logger.debug("*******1")
    curMbo=irData.getCurrentMbo()
    logger.debug("*******1")
    prnum= irData.getCurrentDataAsString("PRNUM");
    siteid= irData.getCurrentDataAsString("SITEID");
    
    combined = prnum + "/" + siteid
    logger.debug("*******1")
    #encodedStr = Base64.encode(combined)
    encodedStr = ""
    
    prSet = MXServer.getMXServer().getMboSet("PR", MXServer.getMXServer().getSystemUserInfo())
    where = SqlFormat(prSet.getUserInfo(), "PRNUM = :1 AND SITEID=:2")
    where.setObject(1, "PR", "PRNUM", prnum)
    where.setObject(2, "PR", "SITEID", siteid)
    prSet.setWhere(where.format())
    prMbo = prSet.moveFirst()
    
    if prMbo:   
        oslcResourceInfo = OslcResourceCache.getInstance().getOslcResourceInfo("GRP_PRDOCLINKS")
        if oslcResourceInfo:
            encodedStr= LocalURIGenerator().getEncodedMboID(prMbo, oslcResourceInfo)        
                 
    prSet.close()  

        
    logger.debug("*******2")
    ApiKey="jcn2hndpjqk6coiqh5go3fm9v9r61vlp35ngdfli" 
    # manipulating childern Data 
    doclinksList=irData.getChildrenData("DOCLINKS")
    logger.debug("*******3")
    noOfDoclinksLines=doclinksList.size()
    logger.debug("*******4***"+str(noOfDoclinksLines))
    if (doclinksList is not None and noOfDoclinksLines > 0):
        for i in range(noOfDoclinksLines):    
            logger.debug("*******5")
            irData.setAsCurrent(doclinksList,i)   
            doclinksid= irData.getCurrentDataAsString("DOCLINKSID");
            #s1="https://:HOSTNAME/maximo/api/os/DM_PRDOC/"
            #Amir 22-10 - OS should be PR based
            s1="https://:HOSTNAME/maximo/api/os/GRP_PRDOCLINKS/"
            s2="/doclinks/"
            s3="?apikey=" +ApiKey
            logger.debug("*******6")
            url=s1+'_'+encodedStr+s2+doclinksid+s3
            #url=s1+s2+doclinksid+s3
            sqf=SqlFormat(curMbo, url)
            logger.debug("*******7")
            sqf.setIgnoreUnresolved(True)
            logger.debug("*******8")
            url=sqf.resolveContent()
            
            logger.debug("** final url is  **"+url)
            irData.setCurrentData("URLNAME", url)
            irData.setCurrentData("URLTYPE", "URL")
            logger.debug("**line2 child Data **")
        irData.setParentAsCurrent()
        
        logger.debug("===== Pretty Printed erData before2 =====")
        logger.debug(XMLOutputter().outputString(irData.getData()))
        logger.debug("===== Pretty Printed erData After2 =====")
    StructureExists = irData.moveToNextObjectStructure()