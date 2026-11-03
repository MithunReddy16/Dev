conditionName = ifaceName;
if (conditionName.length() > 12)
{
    conditionName = conditionName.substring(0, 12);
}
var MicUtil = Java.type("psdi.iface.mic.MicUtil");
skipMbo = MicUtil.parseCondition(conditionName,mbo);
if (skipMbo)
{
    evalresult= false;
}
else{
    evalresult= true;
}