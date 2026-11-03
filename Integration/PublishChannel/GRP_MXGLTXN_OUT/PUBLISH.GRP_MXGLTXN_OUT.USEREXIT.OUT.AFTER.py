############################################
# Script: MXGLTXN object transcation to GRP by userexit out after 
# Author Mithun Reddy 
# Version 1 - 26-03-2025
###########################################
from psdi.iface.mic import StructureData
from psdi.server import MXServer
from psdi.util import MXException
from psdi.mbo import MboRemote,MboSetRemote
print "***Mithun Publish Channel started after ****"
erData.breakData();
curMbo=irData.getCurrentMbo()

matrectrans =curMbo.getString("MATRECTRANS")
matusetrans= curMbo.getString("MATRECTRANS")

if matrectrans is not None :
    #systemsourceid
    erData.setCurrentData("pSourceCode","MAXIMO")
    
    # pUnitOfMeasure, receivedunit in maximo 
    receivedunit=curMbo.getString("receivedunit")
    print("*** unit of measure is ***"+receivedunit)
    erData.setCurrentData("pUnitOfMeasure",irData.getCurrentDataAsString("receivedunit"))
    
    #itemnum
    itemNum= irData.getCurrentDataAsString("ITEMNUM")
    if itemNum is not None :
        DM_ITEMSEG1,DM_ITEMSEG2=itemNum.split('-',1)
        erData.setCurrentData("pItemSegment1", DM_ITEMSEG1)
        erData.setCurrentData("pItemSegment2", DM_ITEMSEG2)
    else :
        erData.setCurrentDataNull("pItemSegment1")
        erData.setCurrentDataNull("pItemSegment2")
    
    #Bin Logic 
    issuetype= irData.getCurrentDataAsString("ISSUETYPE")
    print("Issue type is ***"+irData.getCurrentDataAsString("ISSUETYPE"))
    if issuetype is not None and issuetype=="SHIPTRANSFER" :
        erData.setCurrentData("pLocator", irData.getCurrentDataAsString("FROMBIN"))
        bin=irData.getCurrentDataAsString("FROMBIN")
    if issuetype is not None and issuetype=="SHIPRECEIPT" :
        erData.setCurrentData("pLocator", irData.getCurrentDataAsString("TOBIN"))
        bin=irData.getCurrentDataAsString("TOBIN")
    
    # subinventory , starting letter of bin in maximo , DM_SHED
    print("**** bin is***"+bin)
    if bin :
        subinventory=bin[0]
        erData.setCurrentData("pSubInventory", subinventory)
    
    # Store logic 
    issuetype= irData.getCurrentDataAsString("ISSUETYPE")
    if issuetype is not None and issuetype=="SHIPTRANSFER" :
        erData.setCurrentData("pOrganizationId", irData.getCurrentDataAsString("FROMSTORELOC"))
    if issuetype is not None and issuetype=="SHIPRECEIPT" :
        erData.setCurrentData("pOrganizationId", irData.getCurrentDataAsString("TOSTORELOC"))
    
    # lot logic
    issuetype= irData.getCurrentDataAsString("ISSUETYPE")
    if issuetype is not None and issuetype=="SHIPTRANSFER" :
        erData.setCurrentData("pLotNumber", irData.getCurrentDataAsString("FROMLOT"))
    if issuetype is not None and issuetype=="SHIPRECEIPT" :
        erData.setCurrentData("pLotNumber", irData.getCurrentDataAsString("TOLOT"))
    
    #GLDEBITACCT
    
    gldebit=curMbo.getString("GLDEBITACCT")
    print("*** gldebit is ***"+gldebit)
    if gldebit is not None :
        seg1,seg2,seg3,seg4,seg5,seg6,seg7,seg8=gldebit.split('-',7)
        erData.setCurrentData("psegment1",seg1 )
        erData.setCurrentData("psegment2",seg2 )
        erData.setCurrentData("psegment3",seg3 )
        erData.setCurrentData("psegment4",seg4 )
        erData.setCurrentData("psegment5",seg5)
        erData.setCurrentData("psegment6",seg6 )
        erData.setCurrentData("psegment7",seg7 )
        erData.setCurrentData("psegment8",seg8 )
    else :
        erData.setCurrentDataNull("psegment1")
        erData.setCurrentDataNull("psegment2")
        erData.setCurrentDataNull("psegment3")
        erData.setCurrentDataNull("psegment4")
        erData.setCurrentDataNull("psegment5")
        erData.setCurrentDataNull("psegment6")
        erData.setCurrentDataNull("psegment7")
        erData.setCurrentDataNull("psegment8")
        
    # pTransRef
    pTransRef= irData.getCurrentDataAsString("MATRECTRANSID")
    if pTransRef is not None :
        erData.setCurrentData("pTransRef", pTransRef)
    else :
        erData.setCurrentDataNull("pTransRef")
        
        
### Matusetrans Begins 

if matusetrans is not None:
    #systemsourceid
    erData.setCurrentData("pSourceCode","MAXIMO")
    
    # pUnitOfMeasure, receivedunit in maximo 
    receivedunit=curMbo.getString("receivedunit")
    print("*** unit of measure is ***"+receivedunit)
    erData.setCurrentData("pUnitOfMeasure",irData.getCurrentDataAsString("receivedunit"))
    
    #itemnum
    itemNum= irData.getCurrentDataAsString("ITEMNUM")
    if itemNum is not None :
        DM_ITEMSEG1,DM_ITEMSEG2=itemNum.split('-',1)
        erData.setCurrentData("pItemSegment1", DM_ITEMSEG1)
        erData.setCurrentData("pItemSegment2", DM_ITEMSEG2)
    else :
        erData.setCurrentDataNull("pItemSegment1")
        erData.setCurrentDataNull("pItemSegment2")
    
    #Bin Logic 
    issuetype= irData.getCurrentDataAsString("ISSUETYPE")
    print("Issue type is ***"+irData.getCurrentDataAsString("ISSUETYPE"))
    if issuetype is not None and issuetype=="SHIPTRANSFER" :
        erData.setCurrentData("pLocator", irData.getCurrentDataAsString("FROMBIN"))
        bin=irData.getCurrentDataAsString("FROMBIN")
    if issuetype is not None and issuetype=="SHIPRECEIPT" :
        erData.setCurrentData("pLocator", irData.getCurrentDataAsString("TOBIN"))
        bin=irData.getCurrentDataAsString("TOBIN")
    
    # subinventory , starting letter of bin in maximo , DM_SHED
    print("**** bin is***"+bin)
    if bin :
        subinventory=bin[0]
        erData.setCurrentData("pSubInventory", subinventory)
    
    # Store logic 
    issuetype= irData.getCurrentDataAsString("ISSUETYPE")
    if issuetype is not None and issuetype=="SHIPTRANSFER" :
        erData.setCurrentData("pOrganizationId", irData.getCurrentDataAsString("FROMSTORELOC"))
    if issuetype is not None and issuetype=="SHIPRECEIPT" :
        erData.setCurrentData("pOrganizationId", irData.getCurrentDataAsString("TOSTORELOC"))
    
    # lot logic
    issuetype= irData.getCurrentDataAsString("ISSUETYPE")
    if issuetype is not None and issuetype=="SHIPTRANSFER" :
        erData.setCurrentData("pLotNumber", irData.getCurrentDataAsString("FROMLOT"))
    if issuetype is not None and issuetype=="SHIPRECEIPT" :
        erData.setCurrentData("pLotNumber", irData.getCurrentDataAsString("TOLOT"))
    
    #GLDEBITACCT
    
    gldebit=curMbo.getString("GLDEBITACCT")
    print("*** gldebit is ***"+gldebit)
    if gldebit is not None :
        seg1,seg2,seg3,seg4,seg5,seg6,seg7,seg8=gldebit.split('-',7)
        erData.setCurrentData("psegment1",seg1 )
        erData.setCurrentData("psegment2",seg2 )
        erData.setCurrentData("psegment3",seg3 )
        erData.setCurrentData("psegment4",seg4 )
        erData.setCurrentData("psegment5",seg5)
        erData.setCurrentData("psegment6",seg6 )
        erData.setCurrentData("psegment7",seg7 )
        erData.setCurrentData("psegment8",seg8 )
    else :
        erData.setCurrentDataNull("psegment1")
        erData.setCurrentDataNull("psegment2")
        erData.setCurrentDataNull("psegment3")
        erData.setCurrentDataNull("psegment4")
        erData.setCurrentDataNull("psegment5")
        erData.setCurrentDataNull("psegment6")
        erData.setCurrentDataNull("psegment7")
        erData.setCurrentDataNull("psegment8")
        
    # pTransRef
    pTransRef= irData.getCurrentDataAsString("MATRECTRANSID")
    if pTransRef is not None :
        erData.setCurrentData("pTransRef", pTransRef)
    else :
        erData.setCurrentDataNull("pTransRef")
        
# -- end of Matusetrans