#-----------------------------------------------------------------------------------------
# Name:		SYNC.INVTRANS.USEREXIT.OUT.AFTER
# Description: Sets formatted values during outbound publish from INVTRANS
#
# Publish Channel: SYNCINVTRANS
# Event: Integration --> Publish Channel --> User Exit --> After External Exit
# Version: 1.0 -Mithun Reddy - 26-Mar-2025
# Version: 2.0 - Amir Anwar - 26-NOV-2025
#-----------------------------------------------------------------------------------------

from psdi.iface.mic import StructureData
from psdi.server import MXServer
from psdi.util import MXException
from psdi.mbo import MboRemote, MboSetRemote
from psdi.util.logging import MXLoggerFactory
from org.jdom2.output import XMLOutputter
from psdi.mbo import SqlFormat
from java.text import SimpleDateFormat


def setError(Msg):	
	params=[Msg]
	service.error('scriptval','scriptvalidationerror',params)

logger = MXLoggerFactory.getLogger("maximo.custom")
logger.debug("*** SYNC.INVTRANS.USEREXIT.OUT.AFTER: START ***")

logger.debug(XMLOutputter().outputString(irData.getData()))
logger.debug("*** after erData ***")


erData.breakData()



logger.debug(XMLOutputter().outputString(erData.getData()))
curMbo = irData.getCurrentMbo()

#-----------------------------------------------------------------------------------------
# Format bin number into required format
#-----------------------------------------------------------------------------------------
def formatBinNumber(bin_num):
	if not bin_num or bin_num=="":
		return None
	parts = bin_num.split("-")
	if len(parts) != 4:
		#setError("Invalid bin number format")
		## TODO
		## STOP Transaction
		return bin_num

	seg1, seg2, seg3, seg4 = parts
	merged_seg = seg1 + seg2
	#formatted_seg4 = seg4.zfill(3)
	#return merged_seg + "-" + seg3 + "-" + formatted_seg4
	return merged_seg + "-" + seg3 + "-" + seg4

#-----------------------------------------------------------------------------------------
# Set basic transaction data
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
# Set basic transaction data
#-----------------------------------------------------------------------------------------
def setBaseData():
	erData.setCurrentData("pSourceCode", "MAXIMO")
	erData.setCurrentData("pTransactionDate", str(irData.getCurrentDataAsString("TRANSDATE")))
	erData.setCurrentData("pUnitPrice", str(irData.getCurrentDataAsString("NEWCOST")))
	qty = curMbo.getDouble("QUANTITY")
	logger.debug("** quantity is ***" + str(qty))
	if qty is not None:
		erData.setCurrentData("pTransactionQty", str(abs(qty)))
	
	# unitOfMeasure
	invMboSet=curMbo.getMboSet("INVENTORY")
	invMboSet.moveFirst()
	if invMboSet :
		erData.setCurrentData("pUnitOfMeasure", str(getGRPUoM(invMboSet.getString("ISSUEUNIT"))))
	else:
		erData.setCurrentData("pUnitOfMeasure", str(""))
		
	cost = curMbo.getDouble("NEWCOST")
	if cost is not None:
		erData.setCurrentData("pUnitPrice", str(cost))
		logger.debug("Set pUnitPrice = " + str(cost))
		
	ActualDate = curMbo.getDate("TRANSDATE")
	if ActualDate is not None:
		dateFormat = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss")
		formattedActualDate = dateFormat.format(ActualDate)
		erData.setCurrentData("pTransactionDate", str(formattedActualDate))
		logger.debug("Set pTransactionDate = " + str(formattedActualDate))	  
		

#-----------------------------------------------------------------------------------------
# Set item number segments
#-----------------------------------------------------------------------------------------
def setItemSegments():
	itemNum = irData.getCurrentDataAsString("ITEMNUM")
	if itemNum is not None:
		if '-' in itemNum:
			DM_ITEMSEG1, DM_ITEMSEG2 = itemNum.split('-', 1)
			erData.setCurrentData("pItemSegment1", DM_ITEMSEG1)
			erData.setCurrentData("pItemSegment2", DM_ITEMSEG2)
		else:
			erData.setCurrentData("pItemSegment1",itemNum)
			erData.setCurrentDataNull("pItemSegment2")
	else:
		erData.setCurrentDataNull("pItemSegment1")
		erData.setCurrentDataNull("pItemSegment2")

#-----------------------------------------------------------------------------------------
# Set BIN locator and subinventory
#-----------------------------------------------------------------------------------------
def setBinLocator():
	transType = irData.getCurrentDataAsString("TRANSTYPE")
	logger.debug("trans type is ***" + transType)
	if transType is not None and transType in ('RECBALADJ', 'CURBALADJ'):
		bin = irData.getCurrentDataAsString("BINNUM")
		bin_format = formatBinNumber(bin)
		erData.setCurrentData("pLocator", bin_format)

		if bin and len(bin_format) > 0:
			subinventory = "Shed "+bin[0:1]
			erData.setCurrentData("pSubInventory", subinventory)

#-----------------------------------------------------------------------------------------
# Set store and lot number
#-----------------------------------------------------------------------------------------
def setStoreAndLot():
	transType = irData.getCurrentDataAsString("TRANSTYPE")
	if transType is not None and transType in ('RECBALADJ', 'CURBALADJ'):
		locMboSet=curMbo.getMboSet("locations")
		if not locMboSet.isEmpty() :
			erData.setCurrentData("pOrganizationId", str(locMboSet.moveFirst().getInt("DM_GRPORGID")))
				
		erData.setCurrentData("pLotNumber", irData.getCurrentDataAsString("LOTNUM"))

#-----------------------------------------------------------------------------------------
# Set GL account segments (unchanged as requested)
#-----------------------------------------------------------------------------------------
def setGLSegments():
	
	gldebit = curMbo.getString("GLDEBITACCT")
	glcredit = curMbo.getString("GLCREDITACCT")		
	transtype = irData.getCurrentDataAsString("TRANSTYPE")
	logger.debug("*** TransactionType ***"+str(transtype))
	logger.debug("*** gldebit is  ***"+str(gldebit))
	logger.debug("*** glcredit is ***"+str(glcredit))
	#Since Transaction in Maximo in minus, then Debit Account will always have store Account hence always sending Credit Account
	if transtype in ('RECBALADJ', 'CURBALADJ'):
		if glcredit is not None and glcredit != '':
			seg1, seg2, seg3, seg4, seg5, seg6, seg7, seg8 = glcredit.split('-', 7)
			erData.setCurrentData("psegment1", seg1)
			erData.setCurrentData("psegment2", seg2)
			erData.setCurrentData("psegment3", seg3)
			erData.setCurrentData("psegment4", seg4)
			erData.setCurrentData("psegment5", seg5)
			erData.setCurrentData("psegment6", seg6)
			erData.setCurrentData("psegment7", seg7)
			erData.setCurrentData("psegment8", seg8)
		'''
		qty = curMbo.getDouble("QUANTITY")
		logger.debug("** setTransactionType qty is ***" + str(qty))
		if qty is not None:
			if qty >= 0:
				gldebit = curMbo.getString("GLCREDITACCT")
				logger.debug("*** gldebit is ***" + gldebit)
				if gldebit is not None and gldebit != '':
					segments = gldebit.split('-')
					seg_count = len(segments)
					logger.debug("*** seg_count is ***" + str(seg_count))
					if seg_count == 8:
						logger.debug("***entered 7 seg_count*")
						seg1, seg2, seg3, seg4, seg5, seg6, seg7, seg8 = gldebit.split('-', 7)
						erData.setCurrentData("psegment1", seg1)
						erData.setCurrentData("psegment2", seg2)
						erData.setCurrentData("psegment3", seg3)
						erData.setCurrentData("psegment4", seg4)
						erData.setCurrentData("psegment5", seg5)
						erData.setCurrentData("psegment6", seg6)
						erData.setCurrentData("psegment7", seg7)
						erData.setCurrentData("psegment8", seg8)
					else:
						setError("Invalid debit GL format")
			else:
				glcredit = curMbo.getString("GLDEBITACCT")
				logger.debug("*** glcredit is ***" + glcredit)
				if glcredit is not None and glcredit != '':
					segments = glcredit.split('-')
					seg_count = len(segments)
					logger.debug("*** seg_count is ***" + str(seg_count))
					if seg_count == 8:
						logger.debug("***entered 7 seg_count*")
						seg1, seg2, seg3, seg4, seg5, seg6, seg7, seg8 = glcredit.split('-', 7)
						erData.setCurrentData("psegment1", seg1)
						erData.setCurrentData("psegment2", seg2)
						erData.setCurrentData("psegment3", seg3)
						erData.setCurrentData("psegment4", seg4)
						erData.setCurrentData("psegment5", seg5)
						erData.setCurrentData("psegment6", seg6)
						erData.setCurrentData("psegment7", seg7)
						erData.setCurrentData("psegment8", seg8)
					else:
						setError("Invalid credit GL format")
		'''

#-----------------------------------------------------------------------------------------
# Set transaction reference
#-----------------------------------------------------------------------------------------
def setTransactionRef():
	pTransRef = irData.getCurrentDataAsString("INVTRANSID")
	if pTransRef is not None:
		erData.setCurrentData("pTransRef", "INVTRANS-" + pTransRef)
	else:
		erData.setCurrentDataNull("pTransRef")

#-----------------------------------------------------------------------------------------
# Set transaction Type
#-----------------------------------------------------------------------------------------
def setTransactionType():

	transtype = irData.getCurrentDataAsString("TRANSTYPE")
	logger.debug("*** setTransactionType ***"+str(transtype))
	if transtype == "RECBALADJ":
		qty = curMbo.getDouble("QUANTITY")
		logger.debug("** setTransactionType qty is ***" + str(qty))
		if qty is not None:
			if qty >= 0:
				erData.setCurrentData("pTransactionType", "Miscellaneous receipt")
				erData.setCurrentData("pTransactionQty", str(abs(qty)))
			else:
				erData.setCurrentData("pTransactionType", "Miscellaneous issue")
				erData.setCurrentData("pTransactionQty", str(abs(qty)))			
	elif transtype == "CURBALADJ":
		logger.debug("*** 1 ***")
		qty = curMbo.getDouble("QUANTITY")
		logger.debug("*** 2 ***")
		logger.debug("** setTransactionType quantity is ***" + str(qty))
		if qty is not None:
			logger.debug("*** 3 ***")
			if qty >= 0:
				logger.debug("*** 4 ***")
				erData.setCurrentData("pTransactionType", "Miscellaneous receipt")
				logger.debug("*** 5 ***")
				erData.setCurrentData("pTransactionQty", str(qty))
				logger.debug("*** 6 ***")
			else:
				erData.setCurrentData("pTransactionType", "Miscellaneous issue")
				erData.setCurrentData("pTransactionQty", str(abs(qty)))

#-----------------------------------------------------------------------------------------
# Execute all logic
#-----------------------------------------------------------------------------------------
setBaseData()
setItemSegments()
setBinLocator()
setStoreAndLot()
setGLSegments()
setTransactionRef()
setTransactionType()
logger.debug(XMLOutputter().outputString(erData.getData()))

logger.debug("*** SYNC.INVTRANS.USEREXIT.OUT.AFTER: END ***")