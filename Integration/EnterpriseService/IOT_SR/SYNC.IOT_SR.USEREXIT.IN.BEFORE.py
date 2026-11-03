from psdi.iface.mic import StructureData
from psdi.server import MXServer
from psdi.util import MXException
from psdi.mbo import MboRemote,MboSetRemote
from psdi.mbo import SqlFormat

# breaking message 
#erData.breakData();
isStructurePresent = True
erData.breakData()
mxServer=MXServer.getMXServer()
#userInfo=mxServer.getUserInfo("MAXADMIN")
userInfo=mxServer.getSystemUserInfo()
assetSet =  mxServer.getMboSet("ASSET", userInfo);
erData.moveToFirstObjectStruture()
while (isStructurePresent):
	engTag= erData.getCurrentDataAsString("DM_ASSET_TAG")
	
	# Verifying DM_ASSET_TAG in Asset Table, if found setting the assetnum
	assetSet.setWhere("dm_asset_tag='"+engTag+"' and  status in ('ACTIVE','OPERATING')")
	assetSet.reset();
	assetnum=""
	if assetSet.count()>0:
	    asset = assetSet.getMbo(0);
	    siteID=asset.getString("SITEID")
	    assetnum=asset.getString("ASSETNUM")
	    maintSec=asset.getString("DM_MAINTSEC")
	    #service.error("","maintSec:"+maintSec)
	    erData.setCurrentData("SITEID", siteID)
	    erData.setCurrentData("ASSETNUM", assetnum)
	    erData.setCurrentData("DM_MAINTSEC", maintSec)
	    
	else:
	    erData.setCurrentData("ASSETNUM", "")
	    
        
	isStructurePresent = erData.moveToNextObjectStructure()