#-----------------------------------------------------------------------------------------
# Script Name:SYNC.ARCGISASSET.USEREXIT.IN.BEFORE
# Description: Set default values for inbound CRM data
#
# Enterprise Service: ARCGISASSET
#
# Author: Pramod
# Date: 10-Apr-2025
#*****************************************************************************************

from psdi.server import MXServer
from psdi.util.logging import MXLoggerFactory
from org.jdom2.output import XMLOutputter
from psdi.mbo import SqlFormat
from com.ibm.json.java import JSONObject

logger = MXLoggerFactory.getLogger("maximo.integration.userexit")

logger.debug("============= SYNC.ARCGISASSET.USEREXIT.IN.BEFORE=============")

erData.breakData()
logger.debug("getData:"+str(erData.getData()))

jsonStr = erData.getDataAsString()
jsonData = JSONObject.parse(jsonStr)

# Now proceed as before
features = jsonData.get("features")

if features.size() > 0:
    feature = features.get(0)
    attributes = feature.get("attributes")
    geometry = feature.get("geometry")

    parcel_id = attributes.get("PARCEL_ID")
    latitude= attributes.get("LATIITUDE")
    longitude = attributes.get("LONGITUDE")
    logger.debug("----------------parcel_id"+str(parcel_id))
    logger.debug("----------------latitude"+str(latitude))
    logger.debug("----------------longitude"+str(longitude))
    ##*****************Section to add service addresses based on Parcel is and coordinates----
    if parcel_id and latitude and longitude:
        assetSet = MXServer.getMXServer().getMboSet('ASSET',MXServer.getMXServer().getSystemUserInfo())
        assetSet.setWhere("dm_gis_parcel_id = '" + str(parcel_id) + "' ")
        assetSet.reset()
        logger.debug("----------------Asset Count=" +str(assetSet.count()))
        logger.debug("----------------Asset getCompleteWhere1=" +str(assetSet.getCompleteWhere()))
        
        if assetSet.count()==0:
            logger.debug("----------------Asset Count Is Zeror" )
            service.raiseSkipTransaction()
             
        else:        
            serviceAddressSet = MXServer.getMXServer().getMboSet('serviceaddress',MXServer.getMXServer().getSystemUserInfo())
            serviceAddressSet.setWhere("LATITUDEY = " + str(latitude) + "  and LONGITUDEX="+str(longitude)+" ")
            serviceAddressSet.reset()
            
            serviceAddress = serviceAddressSet.moveFirst()
            addresscode=parcel_id
            if serviceAddress:
                addresscode=serviceAddress.getString("ADDRESSCODE")
            else:
                serviceAddress=serviceAddressSet.addAtEnd();
                serviceAddress.setValue("ADDRESSCODE", str(parcel_id))
                serviceAddress.setValue("LATITUDEY", float(latitude))
                serviceAddress.setValue("LONGITUDEX", float(longitude));
                serviceAddress.setValue("ORGID", "DMORG");
                serviceAddress.setValue("SITEID", "DM");
                
            serviceAddressSet.save()
            serviceAddressSet.cleanup()
            serviceAddressSet.close()  
        
        
            assetmbo = assetSet.moveFirst()
            if assetmbo:
                saddresscode=assetmbo.getString("SADDRESSCODE")    
                if not saddresscode:
                  assetmbo.setValue("SADDRESSCODE", str(addresscode))
            
            assetSet.save()
            assetSet.cleanup()
            assetSet.close()