# ==============================================================================
# Created By      : Ram
# CREATED DATE: June 12, 2026
# Purpose : Evaluates whether the exntersion hours has been entered or not 

# ==============================================================================
from psdi.server import MXServer
from psdi.util.logging import MXLoggerFactory

evalresult = False

if mbo:
    
    extnum_value = mbo.getMboValue("EXTNUM")
    
    # Compare the original database value with the current active value
    if extnum_value.getInitialValue().asString() != extnum_value.getCurrentValue().asString():
        evalresult = True