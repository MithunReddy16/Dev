#script:DM_CHWPBUDGSCRIPT
#Createdby:Ram
#Creation Date:14-JUL-22
#scope: script checks if work order material quantities for rotating items exceed their allocated budget. 
#It also verifies if the work order's main asset or any linked assets have a budget for refurbishment or replacement.
from psdi.mbo import MboConstants
from psdi.mbo import Mbo
from psdi.util.logging import MXLoggerFactory
from psdi.server import MXServer
from psdi.security import ConnectionKey
from java.sql import Connection
from java.sql import Statement
from java.text import SimpleDateFormat


logger = MXLoggerFactory.getLogger("maximo.autoscript.script")

logger.info(">>>code execution started<<<")

logger.debug(">>>code execution started<<<")

evalresult = True

d =mbo.getDate("reportdate")

wyear = SimpleDateFormat("yyyy").format(d);

wonum =mbo.getString("wonum")
wpsite =mbo.getString("siteid")
wporg =mbo.getString("orgid")
wasset =mbo.getString("assetnum")

wpmset = mbo.getMboSet("WPMATERIALTASK")

#line = wpmset.moveFirst()

#while(line!=None):
for i in range(0,wpmset.count()):
     line = wpmset.getMbo(i)
     wpitem= line.getString("itemnum");
     #wpqty=  line.getString("itemqty");
     logger.info(">>>code execution startedww<<<")
     conKey = mbo.getThisMboSet().getUserInfo().getConnectionKey()
     con = mbo.getThisMboSet().getMboServer().getDBConnection(conKey)
    # line = wpmset.moveNext() 
     try:
       
     
    
           
                    s1 = con.createStatement()
                    
                    #wpval = "select sum(wm.itemqty) as qty,wm.itemnum from wpmaterial wm,item i,workorder w where wm.itemnum in ('"+wpitem+"') and wm.itemnum=i.itemnum and i.rotating=1 and w.wonum='"+wonum+"' and (w.wonum=wm.wonum or wm.WONUM in (select wonum from workorder where parent=wm.wonum and istask=1)) and w.siteid='"+wpsite+"' and w.orgid='"+wporg+"'   group by wm.itemnum"
                    wpval = "select sum(wm.itemqty) as qty,wm.itemnum from wpmaterial wm,item i,workorder w where wm.itemnum in ('"+wpitem+"') and wm.itemnum=i.itemnum and i.rotating=1 and  (w.wonum=wm.wonum or wm.WONUM in (select wonum from workorder where parent=wm.wonum and istask=1)) and w.siteid='"+wpsite+"' and w.orgid='"+wporg+"' and w.status='APPR'  group by wm.itemnum"
                    wpqty = s1.executeQuery(wpval)
       
                    
                    s2 = con.createStatement() 
                    buval ="select sum(l.apprqty) as bqty,l.itemnum from dm_budgetline l,dm_budget b,item i where b.budgetnum=l.budgetnum and l.itemnum='"+wpitem+"' and year='"+wyear+"'and b.siteid='"+wpsite+"' and b.orgid='"+wporg+"' and l.itemnum=i.itemnum and i.rotating=1  group by l.itemnum"
                    buqty=  s2.executeQuery(buval)
                    massetset = mbo.getMboSet("MULTIASSETLOCCI")
                    massetset.setWhere(" isprimary=0 and assetnum is not null")

                    mcount = massetset.count()

                    if mcount >0:
                         mrecord = massetset.moveFirst()
                         while(mrecord):
                                 masset=mrecord.getString("Assetnum")
                                 msiteid=mrecord.getString("siteid")
                                 morgid=mrecord.getString("orgid")
                                 mrecord = massetset.moveNext()

                                 s5 = con.createStatement() 
                                 s6 = con.createStatement() 
                                 mubval= "select l.assetnum from dm_budgetline l,dm_budget b where b.budgetnum=l.budgetnum and l.assetnum in ('"+masset+"') and year='"+wyear+"'and b.siteid='"+msiteid+"' and b.orgid='"+morgid+"' and  l.need in ('Refurbishment / Upgrade','Replacement')"
                                 mrbval= "select sum(l.apprqty) as mqty,l.assetnum from dm_budgetline l,dm_budget b where b.budgetnum=l.budgetnum and l.assetnum in ('"+masset+"') and year='"+wyear+"'and b.siteid='"+msiteid+"' and b.orgid='"+morgid+"'  and l.need in ('Replacement')  group by l.assetnum"  
                                 muqty = s5.executeQuery(mubval)
                                 mrqty = s6.executeQuery(mrbval)
                                 
                                 if(muqty.next()==False):
                                      evalresult = False
                                    # basset = auqty.getString("assetnum")
                                      
                                      #service.error("DM", "genericerror", ['multiasset upgrade'])   
                                      
                                           
                    if(wpqty.next()):
                       wqty = wpqty.getInt("qty")
                       witem = wpqty.getString("itemnum")
                       
                    if(buqty.next()):
                       blqty = buqty.getInt("bqty")
                       bitem = buqty.getString("itemnum")
                       logger.info(">>>code execution started2333333<<<"+bitem)
                       #if witem == bitem:
                       
                               
                              # service.error("DM", "genericerror", ['fweafge'])
                       if (witem!=None):      
                                
                                if wqty> blqty:
                                      evalresult = False
                                      
                                      #service.error("DM", "genericerror", ['test'])      
                    
                       if wasset!= "":
                                                    logger.info(">>>code executionwdfq 4654<<<"+wasset)
                                                  #  service.error("DM", "genericerror", ['testasset'])      
                                                    asset= mbo.getMboSet("Asset").getMbo(0)
                                                    assetn=   asset.getString("Assetnum")
                                                    aitemnum= asset.getString("itemnum")
                                                    asiteid= asset.getString("siteid")
                                                    aorgid= asset.getString("orgid")
                                                    s3 = con.createStatement() 
                                                    s4 = con.createStatement() 
                                                    aubval= "select l.assetnum from dm_budgetline l,dm_budget b where b.budgetnum=l.budgetnum and l.assetnum in ('"+assetn+"') and year='"+wyear+"'and b.siteid='"+asiteid+"' and b.orgid='"+aorgid+"' and  l.need in ('Refurbishment / Upgrade','Replacement')"
                                                    arbval= "select sum(l.apprqty) as asqty,l.assetnum from dm_budgetline l,dm_budget b where b.budgetnum=l.budgetnum and l.assetnum in ('"+assetn+"') and year='"+wyear+"'and b.siteid='"+asiteid+"' and b.orgid='"+aorgid+"'  and l.need in ('Replacement')  group by l.assetnum"  
                                                    auqty = s3.executeQuery(aubval)
                                                    arqty = s4.executeQuery(arbval)
                                                    logger.info(">>>code execution asset <<<")
                                                    if(auqty.next()==False):
                                                            evalresult = False
                                                           # basset = auqty.getString("assetnum")
                                                            logger.info(">>>code execution aus<<<")
                                                            #service.error("DM", "genericerror", ['upgrade'])   
                                                   
                                                   
                                      
                          
                                       
        
     except Exception as e:
                      print "an error was encountered" 
                    #  throw new MXApplicationException("DM", "genericerror", ['53'])
                      logger.info(">>>code executionwdfq End544xxx1<<<")
                      logger.error(e)
                      
     finally:
            if s1 != "":
               s1.close() 
            elif s2 != "":
               s2.close() 
            elif s3 != "":
               s3.close() 
            elif s4 != "":
               s4.close()
            elif s5 != "":
               s5.close() 
            elif s6 != "":
               s6.close()           
          
            if conKey != "" and con != "":
               mbo.getThisMboSet().getMboServer().freeDBConnection(conKey)