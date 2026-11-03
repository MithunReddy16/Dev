from psdi.iface.mic import StructureData
from psdi.server import MXServer
from psdi.util import MXException
from psdi.mbo import MboRemote,MboSetRemote
from psdi.util.logging import MXLoggerFactory

logger = MXLoggerFactory.getLogger("maximo.integration.userexit")

logger.debug("============= PUBLISH.PC_ASSETRETIREMENT.USEREXIT.OUT.AFTER STARTED=============")

irData.breakData();
curMbo=irData.getCurrentMbo()
'''
if (not irData.isInCurrentData("pCostRetired") or irData.isCurrentDataNull("pCostRetired")):
    logger.debug("============= PUBLISH.PC_ASSETRETIREMENT.USEREXIT.OUT.AFTER \r\n pCostRetired is None \r\n \r\n=============")
    irData.setCurrentData("pCostRetired","0.00")
    logger.debug("============= PUBLISH.PC_ASSETRETIREMENT.USEREXIT.OUT.AFTER \r\n pCostRetired is "+irData.getCurrentDataAsString('pCostRetired')+" \r\n \r\n=============")
    
if (not irData.isInCurrentData("pSoldTo") or irData.isCurrentDataNull("pSoldTo")):
    logger.debug("============= PUBLISH.PC_ASSETRETIREMENT.USEREXIT.OUT.AFTER \r\n pSoldTo is None=============")
    DisposalMbo = curMbo.getMboSet('DM_ASSETRETIREMENT').moveFirst()
    if DisposalMbo:
        if not DisposalMbo.isNull('AWARDCOMPANY'):
            irData.setCurrentData("pSoldTo",DisposalMbo.getString('AWARDCOMPANY'))
    logger.debug("============= PUBLISH.PC_ASSETRETIREMENT.USEREXIT.OUT.AFTER \r\n pCostRetired is "+irData.getCurrentDataAsString('pSoldTo')+"\r\n \r\n=============")
'''
irData.setCurrentData("pCostRetired","0.00")
irData.setCurrentData("pProceedsOfSale","0.00")
if curMbo:
    DisposalMbo = curMbo.getMboSet('DM_ASSETRETIREMENT').moveFirst()
    if DisposalMbo:
        if not DisposalMbo.isNull('AUCPRICE'):
            irData.setCurrentData("pCostRetired",str(DisposalMbo.getFloat('AUCPRICE')))
            irData.setCurrentData("pProceedsOfSale",str(DisposalMbo.getFloat('AUCPRICE')))

logger.debug("============= PUBLISH.PC_ASSETRETIREMENT.USEREXIT.OUT.AFTER \r\n pCostRetired is "+irData.getCurrentDataAsString('pCostRetired')+" \r\n \r\n=============")
logger.debug("============= PUBLISH.PC_ASSETRETIREMENT.USEREXIT.OUT.AFTER ENDED=============")