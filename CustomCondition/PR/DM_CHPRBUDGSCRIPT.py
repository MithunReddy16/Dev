from psdi.mbo import MboConstants
from psdi.mbo import Mbo
from psdi.util.logging import MXLoggerFactory
from psdi.server import MXServer
from psdi.security import ConnectionKey
from java.sql import Connection
from java.sql import Statement
from java.text import SimpleDateFormat


logger = MXLoggerFactory.getLogger("maximo.autoscript.PR_CHECKBUDGET")

logger.info(">>>code execution started<<<")

logger.debug(">>>code execution started<<<")

evalresult = True

d =mbo.getDate("issueDate")
#vReportDate = SimpleDateFormat(dd-MMM-yyyy).format(mbo.getDate(Scheduledate))
Pryear = SimpleDateFormat("yyyy").format(d);

prsite =mbo.getString("siteid")
prorg =mbo.getString("orgid")

#Prlines = mbo.getMboSet("prline").getMbo(0)
#proqty = Prlines.getString("orderqty")
#pritemnum = Prlines.getString("itemnum")
#prlinecost = Prlines.getString("linecost")

#PrBudget = mbo.getMboSet("PRBUDGET");

Prlineset = mbo.getMboSet("prline")
line = Prlineset.moveFirst()
while (line!=None):

 pritem= line.getString("itemnum");
 prqty=  line.getString("orderqty");

 conKey = mbo.getThisMboSet().getUserInfo().getConnectionKey()
 con = mbo.getThisMboSet().getMboServer().getDBConnection(conKey)
    
 
 try:
     
    s1 = con.createStatement()
    prval = "select sum(pl.orderqty) as qty,pl.itemnum from prline pl,item i,PR p where pl.itemnum='"+pritem+"' and pl.itemnum=i.itemnum and i.rotating=1 and p.prnum=pl.prnum and p.siteid='"+prsite+"' and p.orgid='"+prorg+"'  group by pl.itemnum"    
    prqty = s1.executeQuery(prval)
    s2 = con.createStatement() 
    buval ="select sum(l.apprqty) as bqty,l.itemnum from dm_budgetline l,dm_budget b where b.budgetnum=l.budgetnum and l.itemnum='"+pritem+"' and year='"+Pryear+"'and b.siteid='"+prsite+"' and b.orgid='"+prorg+"' group by l.itemnum"
    buqty=  s2.executeQuery(buval)
    logger.info(">>>code execution Endxxx1<<<")
    
    while prqty.next():
            pqty = prqty.getDouble("qty")
            pitem = prqty.getString("itemnum")
            logger.info(">>>code execution pitem End13<<<"+pitem)
            
            
            try:
                if (buqty.next()==False):
                     evalresult= False
                    
    
                blqty = buqty.getDouble("bqty")
                bitem = buqty.getString("itemnum")
                
                if pitem == bitem:
                   if pqty> blqty:
                       evalresult= False
            except:
                 print "an error was encountered"              
                              
        
    buqty.close()      
    s2.close()
    prqty.close()
    s1.close()
    con.commit()
    

 finally:
        if s1 != "":
           s1.close()
        elif s2 != "":
           s2.close()   
        if conKey != "" and con != "":
           mbo.getThisMboSet().getMboServer().freeDBConnection(conKey)

 line = Prlineset.moveNext()