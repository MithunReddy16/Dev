from psdi.server import MXServer
from psdi.util.logging import MXLoggerFactory

evalresult = False

myLogger = MXLoggerFactory.getLogger("maximo.custom")

prnum = mbo.getString('prnum')
prlineSet = mbo.getMboSet("prline")
#prlineSet.setWhere("prnum = '{}' AND dm_appr = 0 and dm_ccappr=0".format(prnum))

prlineSet.setOrderBy("prlinenum ASC")
#prlineSet.reset()

prMbo=prlineSet.moveFirst()

if prMbo:

		myLogger.info('Processing {} lines for pr: {}'.format(prlineSet.count(), prnum))
		found=False
		for i in range(prlineSet.count()):
				prline = prlineSet.getMbo(i)
				if not prline.getBoolean('dm_appr') and not prline.getBoolean('dm_ccappr'):
				    #service.error("dm", "genericerror", [  str(prMbo.getString("itemnum"))+"-Gdzd-"+str(prMbo.getBoolean("dm_ccappr")) )])
				    found=True
				    break;
		if found:
			#service.error("dm", "genericerror", [  str(prMbo.getString("itemnum"))+"-Gdzd-"+str(prMbo.getBoolean("dm_ccappr")) )])
			itemnum = prline.getString("ITEMNUM")
			prlinenum = prline.getInt("prlineNUM")
			myLogger.info('Processing line {} with item number: {}'.format(prlinenum, itemnum))
			itemnum = prline.getString("ITEMNUM")
			dm_ccappr = prline.getBoolean("dm_ccappr")
			
			dm_appr = prline.getBoolean("dm_appr")
			#service.error("dm", "genericerror", [str(prlineSet.count())+"dfds-"+itemnum+"-m-"+str(prlinenum)+"-so-"+str(dm_ccappr)+"-sob-"+str(dm_appr)])    
			myLogger.info("ctLog - dm_ccappr: {}, dm_appr: {}".format(dm_ccappr, dm_appr))
			ItemSet = MXServer.getMXServer().getMboSet("ITEM", mbo.getUserInfo())
			ItemSet.setWhere("itemnum = '{}'".format(itemnum))
			if not ItemSet.isEmpty():
				item = ItemSet.getMbo(0)
				commodity = item.getString("COMMODITY")
			
				commodity_parts = commodity.split('-')
				if len(commodity_parts) > 1:
					commodity_prefix = commodity_parts[0]
					commodity_number = int(commodity_parts[1])
					commodity_suffix = commodity_parts[1]
					#service.error("dm", "genericerror", [str(prlineSet.count())+"dfds-"+itemnum+"-m-"+str(prlinenum)+"-so-"+str(dm_ccappr)+"tha-"+str(dm_appr)])    
					DM_MRA_Set = MXServer.getMXServer().getMboSet("DM_MRA", mbo.getUserInfo())
					DM_MRA_Set.reset()

					if DM_MRA_Set.count() > 0:
					    cprefix=False
					    csuffix=False
					    for j in range(DM_MRA_Set.count()):
							DM_MRA = DM_MRA_Set.getMbo(j)
							from_category = DM_MRA.getString("fromcategory")
							to_category = DM_MRA.getString("tocategory")
							approver_assigned = DM_MRA.getString("approveby")
							
							from_category_parts = from_category.split('-')
							to_category_parts = to_category.split('-')
							#service.error("dm", "genericerror", [str(prlineSet.count())+"dfds-"+itemnum+"-m-"+str(prlinenum)+"-so-"+str(dm_ccappr)+"-sob-"+str(dm_appr)])    
							if len(from_category_parts) > 1 and len(to_category_parts) > 1:
								from_category_prefix = from_category_parts[0]
								from_category_number = int(from_category_parts[1])
								from_category_suffix = from_category_parts[1]

								to_category_prefix = to_category_parts[0]
								to_category_number = int(to_category_parts[1])
								to_category_suffix = to_category_parts[1]

								if commodity_prefix == from_category_prefix == to_category_prefix:
								    cprefix=True
								    #service.error("dm", "genericerror", [str(prlineSet.count())+"dfds-"+itemnum+"-m-"+str(prlinenum)+"-so-"+str(dm_ccappr)+"-sob-"+str(dm_appr)])    
								    myLogger.info('Prefix match: {} == {} == {}'.format(commodity_prefix, from_category_prefix, to_category_prefix))
								    if from_category_number <= commodity_number <= to_category_number:
								        csuffix=True
								        #service.error("dm", "genericerror", [str(prlineSet.count())+"dfds-"+itemnum+"-m-"+str(prlinenum)+"-so-"+str(dm_ccappr)+"-sob-"+str(dm_appr)])    
								        myLogger.info('Found match for commodity: {}-{} ({}-{}) within range {}-{} in DM_MRA.'.format(
								            commodity_prefix, commodity_number, from_category_prefix, from_category_number, from_category_number, to_category_number))
								        myLogger.info('before Approver found: {}'.format(approver_assigned))  
								        evalresult = True
											  

				
service.log("Evaluation result: {}".format(evalresult))