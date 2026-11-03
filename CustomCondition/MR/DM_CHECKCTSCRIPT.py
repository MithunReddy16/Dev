from psdi.server import MXServer
from psdi.util.logging import MXLoggerFactory

evalresult = False

myLogger = MXLoggerFactory.getLogger("maximo.custom")

mrnum = mbo.getString('MRNUM')
MRLineSet = mbo.getMboSet("MRLINE")
#MRLineSet.setWhere("mrnum = '{}' AND dm_appr = 0 and dm_ccappr=0".format(mrnum))

MRLineSet.setOrderBy("mrlinenum ASC")
#MRLineSet.reset()

MrMbo=MRLineSet.moveFirst()

if MrMbo:

		myLogger.info('Processing {} lines for MR: {}'.format(MRLineSet.count(), mrnum))
		found=False
		for i in range(MRLineSet.count()):
				MRLine = MRLineSet.getMbo(i)
				if not MRLine.getBoolean('dm_appr') and not MRLine.getBoolean('dm_ccappr'):
				    #service.error("dm", "genericerror", [  str(MrMbo.getString("itemnum"))+"-Gdzd-"+str(MrMbo.getBoolean("dm_ccappr")) +" and " +str(MrMbo.getBoolean("dm_muappr"))])
				    found=True
				    break;
		if found:
			#service.error("dm", "genericerror", [  str(MrMbo.getString("itemnum"))+"-Gdzd-"+str(MrMbo.getBoolean("dm_ccappr")) +" and " +str(MrMbo.getBoolean("dm_muappr"))])
			itemnum = MRLine.getString("ITEMNUM")
			mrlinenum = MRLine.getInt("MRLINENUM")
			myLogger.info('Processing line {} with item number: {}'.format(mrlinenum, itemnum))
			itemnum = MRLine.getString("ITEMNUM")
			dm_ccappr = MRLine.getBoolean("dm_ccappr")
			dm_muappr = MRLine.getBoolean("dm_muappr")
			dm_appr = MRLine.getBoolean("dm_appr")
			#service.error("dm", "genericerror", [str(MRLineSet.count())+"dfds-"+itemnum+"-m-"+str(mrlinenum)+"-so-"+str(dm_ccappr)+"-sob-"+str(dm_muappr)+"-itha-"+str(dm_appr)])    
			myLogger.info("ctLog - dm_ccappr: {}, dm_muappr: {}, dm_appr: {}".format(dm_ccappr, dm_muappr, dm_appr))
			ItemSet = MXServer.getMXServer().getMboSet("ITEM", mbo.getUserInfo())
			ItemSet.setWhere("itemnum = '{}'".format(itemnum))
			if not ItemSet.isEmpty():
				item = ItemSet.getMbo(0)
				commodity = item.getString("COMMODITY")
				mainuser = item.getString("dm_mainuser")
				commodity_parts = commodity.split('-')
				if len(commodity_parts) > 1:
					commodity_prefix = commodity_parts[0]
					commodity_number = int(commodity_parts[1])
					commodity_suffix = commodity_parts[1]
					#service.error("dm", "genericerror", [str(MRLineSet.count())+"dfds-"+itemnum+"-m-"+str(mrlinenum)+"-so-"+str(dm_ccappr)+"-sob-"+str(dm_muappr)+"-itha-"+str(dm_appr)])    
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
							#service.error("dm", "genericerror", [str(MRLineSet.count())+"dfds-"+itemnum+"-m-"+str(mrlinenum)+"-so-"+str(dm_ccappr)+"-sob-"+str(dm_muappr)+"-itha-"+str(dm_appr)])    
							if len(from_category_parts) > 1 and len(to_category_parts) > 1:
								from_category_prefix = from_category_parts[0]
								from_category_number = int(from_category_parts[1])
								from_category_suffix = from_category_parts[1]

								to_category_prefix = to_category_parts[0]
								to_category_number = int(to_category_parts[1])
								to_category_suffix = to_category_parts[1]

								if commodity_prefix == from_category_prefix == to_category_prefix:
								    cprefix=True
								    #service.error("dm", "genericerror", [str(MRLineSet.count())+"dfds-"+itemnum+"-m-"+str(mrlinenum)+"-so-"+str(dm_ccappr)+"-sob-"+str(dm_muappr)+"-itha-"+str(dm_appr)])    
								    myLogger.info('Prefix match: {} == {} == {}'.format(commodity_prefix, from_category_prefix, to_category_prefix))
								    if from_category_number <= commodity_number <= to_category_number:
								        csuffix=True
								        #service.error("dm", "genericerror", [str(MRLineSet.count())+"dfds-"+itemnum+"-m-"+str(mrlinenum)+"-so-"+str(dm_ccappr)+"-sob-"+str(dm_muappr)+"-itha-"+str(dm_appr)])    
								        myLogger.info('Found match for commodity: {}-{} ({}-{}) within range {}-{} in DM_MRA.'.format(
								            commodity_prefix, commodity_number, from_category_prefix, from_category_number, from_category_number, to_category_number))
								        myLogger.info('before Approver found: {}'.format(approver_assigned))  
								        evalresult = True
											  

					#if commodity and not cprefix and not csuffix:
					 #   MrMbo.setValue("dm_appr", True, 2L)
					  #  MrMbo.setValue("dm_ccappr", True, 2L)
						    
				#				service.error("dm", "genericerror", [
				#					"Checking row {} in DM_MRA. Item {} with commodity code {}-{} is not matching with mid route approval.".format(mrlinenum,itemnum, commodity_prefix, commodity_suffix)
				#				])
	#	if MrMbo.getBoolean("dm_ccappr")==1 and MrMbo.getBoolean("dm_muappr")==1:
		#service.error("dm", "genericerror", [  str(MrMbo.getString("itemnum"))+"-Gdzd-"+str(MrMbo.getBoolean("dm_ccappr")) +" and " +str(MrMbo.getBoolean("dm_muappr"))])
	#			     MrMbo.setValue("dm_appr", True, 2L)                

service.log("Evaluation result: {}".format(evalresult))