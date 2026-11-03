#-----------------------------------------------------------------------------------------
# Script Name : SYNC.ES_EMPLOYEE.USEREXIT.IN.BEFORE
# Description : Inbound User Exit Before External Exit for ES_EMPLOYEE interface
#
# Enterprise Service : ES_EMPLOYEE
# Object Structure   : DM_EMPLOYEE
# Event              : Integration --> Enterprise Service --> Request --> User Exit --> Before External Exit
#
# Author             : Mithun Reddy
# Version            : 1.0
# Date               : 01-May-2025
#-----------------------------------------------------------------------------------------

from psdi.iface.mic import StructureData
from psdi.server import MXServer
from psdi.util.logging import MXLoggerFactory
from java.io import StringWriter
from javax.xml.transform import TransformerFactory
from javax.xml.transform.dom import DOMSource
from javax.xml.transform.stream import StreamResult
from org.jdom2.output import XMLOutputter

logger = MXLoggerFactory.getLogger("maximo.custom")
logger.debug("========== START: SYNC.ES_EMPLOYEE.USEREXIT.IN.BEFORE ==========")

#-----------------------------------------------------------------------------------------
# Set default values if missing
#-----------------------------------------------------------------------------------------
def setDefaultValues(erData):
    logger.debug("=***** setDefaultValues***")
    
#-----------------------------------------------------------------------------------------
# Process lookup_employee  logic
#-----------------------------------------------------------------------------------------
def lookup_employee(erData):    
    

    employee_number = ""
    grpemail_Upper=""
    logger.debug("*****DEBUG: PERSONID = " + str(erData.getCurrentDataAsString("PERSONID")))
    
    
    employee_number = erData.getCurrentDataAsString("PERSONID")
    #employee_number = erData.getCurrentDataAsString("EMPLOYEE_NUMBER")
    logger.debug("********before grp_email0.1 ******"+str(employee_number))
    contingent_number = erData.getCurrentDataAsString("CONTINGENT_NUMBER")
    logger.debug("*****DEBUG: contingent_number = " + str(contingent_number))
    
    
    if contingent_number is not None and contingent_number != '':
        employee_number = contingent_number
    
    dm_grpempnum = employee_number   # base employee number

    erData.setCurrentData("DM_GRPEMPNUM", dm_grpempnum)
    erData.setCurrentData("PERSONID", employee_number)


    #grp_email = erData.getCurrentDataAsString("EMAIL_ADDRESS")

    grp_email = erData.getCurrentDataAsString("PRIMARYEMAIL")
    logger.debug("********before grp_email0 ******"+str(grp_email))

    if grp_email is not None and  grp_email !='': 
        grpemail_Upper = grp_email.upper()
   
    
    emailSet = MXServer.getMXServer().getMboSet("EMAIL", runAsUserInfo)    
    emailSet.setWhere(" UPPER(EMAILADDRESS)='" + grpemail_Upper + "'  ")    
    emailSet.reset()
    
    logger.debug("********email Set ******"+str(emailSet.getWhere()))

    
    emailMbo = emailSet.moveFirst()        
    if emailMbo:
        maximo_personid=emailMbo.getString("personid")

        personSet = MXServer.getMXServer().getMboSet("PERSON", runAsUserInfo)
        personSet.setWhere(" PERSONID='" + maximo_personid + "' ")
        personSet.reset()    
        person = personSet.moveFirst()
        if person:
            if person.isNull("DM_GRPEMPNUM") or person.getString("DM_GRPEMPNUM") == dm_grpempnum:
                erData.setCurrentData("EMPLOYEE_NUMBER", maximo_personid)      
            elif person.getString("DM_GRPEMPNUM") != dm_grpempnum:
                erData.setCurrentDataNull("PRIMARYEMAIL")

        personSet.cleanup()
        personSet.close()

    


def org_hierarchy(erData):
    
    emp_section = ""
    emp_department = ""
    emp_sector = ""
    orgid=""
    if not erData.isCurrentDataNull("ORGANIZATION_ID"):
        orgid = erData.getCurrentDataAsString("ORGANIZATION_ID")

    org_hierarchy_set = MXServer.getMXServer().getMboSet("DM_ORGHIERARCHY", runAsUserInfo)
    org_hierarchy_set.setWhere(" UNITID='{}' and UNITTYPE='{}' ".format(orgid,"SECTION"))
    org_hierarchy_set.reset()
    org_hierarchy_mbo = org_hierarchy_set.moveFirst()
    if org_hierarchy_mbo:
        emp_section = orgid
        emp_department = org_hierarchy_mbo.getString("PARENT1ID")
        emp_sector = org_hierarchy_mbo.getString("PARENT2ID")
        
        erData.setCurrentData("DM_SECTOR", emp_sector)
        erData.setCurrentData("DM_DEPARTMENT", emp_department)
        erData.setCurrentData("DM_SECTION", emp_section)

    else:
        erData.setCurrentDataNull("DM_SECTOR")
        erData.setCurrentDataNull("DM_DEPARTMENT")
        erData.setCurrentDataNull("DM_SECTION")

    
    
    org_hierarchy_set.cleanup()
    org_hierarchy_set.close()
 
def person_status(erData):
    
    status = ""
    assignment_status = erData.getCurrentDataAsString("ASSIGNMENT_STATUS_EN")
    if assignment_status == "Active Contingent Assignment" or assignment_status == "Active Assignment":
        status = "ACTIVE"
    else:
        status = "INACTIVE"
    erData.setCurrentData("STATUS", status)

def person_supervisior(erData):
    supervisor_number = erData.getCurrentDataAsString("SUPERVISOR")
    if not supervisor_number or supervisor_number == "":
	    supervisor_number = erData.getCurrentDataAsString("SUPERVISOR_CONTINGENT_NUMBER")
    person_supervisor_set = MXServer.getMXServer().getMboSet("PERSON", MXServer.getMXServer().getSystemUserInfo())
    person_supervisor_set.setWhere(" PERSONID='" + str(supervisor_number) + "'")
    person_supervisor_set.reset()
    person_supervisor_mbo = person_supervisor_set.moveFirst()
    #service.error("B",person_supervisor_mbo.getString("PERSONID"))
    if person_supervisor_mbo:
        erData.setCurrentData("SUPERVISOR", supervisor_number)
    else:
        #service.error("A",supervisor_number)
        erData.setCurrentDataNull("SUPERVISOR")


#-----------------------------------------------------------------------------------------
# Pretty print the erData XML for debugging
#-----------------------------------------------------------------------------------------
def logErData(erData):
    try:
        logger.debug(XMLOutputter().outputString(erData.getData()))

    except Exception, e:
        logger.error("Error while printing erData XML: " + str(e))

#-----------------------------------------------------------------------------------------
# Main Execution
#-----------------------------------------------------------------------------------------
erData.breakData()
runAsUserInfo =MXServer.getMXServer().getSystemUserInfo()

logErData(erData)

setDefaultValues(erData)
lookup_employee(erData)
person_status(erData)
person_supervisior(erData)
org_hierarchy(erData)

logErData(erData)
logger.debug("========== END: SYNC.ES_EMPLOYEE.USEREXIT.IN.BEFORE ==========")