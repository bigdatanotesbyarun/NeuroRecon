from django.db import models


class Sidebar(models.Model):
    name=models.CharField(max_length=1000)
    idV=models.CharField(max_length=1000)
    eventType=models.CharField(max_length=1000)
    formName=models.CharField(max_length=1000)
    seq=models.IntegerField()

class HeaderPanel(models.Model):
    name=models.CharField(max_length=1000)
    idV=models.CharField(max_length=1000)
    seq=models.IntegerField()
    formName=models.CharField(max_length=1000)
    eventType=models.CharField(max_length=1000)

class ChartPanel(models.Model):
    name=models.CharField(max_length=1000)
    idV=models.CharField(max_length=1000)
    seq=models.IntegerField()
    formName=models.CharField(max_length=1000)
    eventType=models.CharField(max_length=1000)

class ChartPanelCOB(models.Model):
    name=models.CharField(max_length=1000)
    idV=models.CharField(max_length=1000)
    seq=models.IntegerField()
    formName=models.CharField(max_length=1000)
    eventType=models.CharField(max_length=1000)

class Table(models.Model):
    name=models.CharField(max_length=1000)
    lebal=models.CharField(max_length=1000)
    isRTTable=models.CharField(max_length=1000)

class GemfireCountTable1(models.Model):
    tblname=models.CharField(max_length=1000)
    name=models.CharField(max_length=1000)
    countDiff=models.IntegerField()
    hiveCount=models.IntegerField()
    gemfireCount=models.IntegerField()
    created=models.DateTimeField()
    env=models.CharField(max_length=1000,default="Test")
    

class SKReconTable(models.Model):
    tblname=models.CharField(max_length=1000,default="Test")
    env=models.CharField(max_length=1000,default="Test")
    name=models.CharField(max_length=1000)
    mismatchFreq=models.IntegerField()
    mismatchCount=models.IntegerField()
    created=models.DateTimeField()

class GZTable(models.Model):
    name=models.CharField(max_length=1000)
    statts=models.DateTimeField()
    endts=models.DateTimeField()
    env=models.CharField(max_length=1000,default="Test")
    ps=models.CharField(max_length=1000,default="Test")
    pltps=models.CharField(max_length=1000,default="Test")
    eapps=models.CharField(max_length=1000,default="Test")

class PipeLine(models.Model):
    name=models.CharField(max_length=1000)
    lebal=models.CharField(max_length=1000)

class RequestVO(models.Model):
    reqId=models.CharField(max_length=1000)
    name=models.CharField(max_length=1000)
    reconType=models.CharField(max_length=1000)
    tblName=models.CharField(max_length=1000)
    flow=models.CharField(max_length=1000)
    startOffSet=models.CharField(max_length=1000)
    endOffSet=models.CharField(max_length=1000)

class ReconVO(models.Model):
    reqId=models.CharField(max_length=1000)
    name=models.CharField(max_length=1000)
    created=models.DateTimeField(auto_now_add=True)
    tblName=models.CharField(max_length=1000)
    pipeline=models.CharField(max_length=1000)
    temporal=models.CharField(max_length=1000)
    onBoarding=models.CharField(max_length=1000)
    batch=models.CharField(max_length=1000)
    date=models.CharField(max_length=1000)
    startOffSet=models.CharField(max_length=1000)
    endOffSet=models.CharField(max_length=1000)
    field1=models.CharField(max_length=1000 ,default='test')
    field2=models.CharField(max_length=1000,default='test')
    field3=models.CharField(max_length=1000,default='test')
    field4=models.CharField(max_length=1000,default='test')
    field5=models.CharField(max_length=1000,default='test')
    field6=models.CharField(max_length=1000,default='InProgress')


class Jobs(models.Model):
    table=models.CharField(max_length=1000)
    type=models.CharField(max_length=1000)
    jobName=models.CharField(max_length=1000)
    POC=models.CharField(max_length=1000)
    onBoarding=models.CharField(max_length=1000)
    env=models.CharField(max_length=1000,default="Test")
    lastts=models.CharField(max_length=1000,default="Test")
    executionTime=models.CharField(max_length=1000,default="Test")

class ReconResult(models.Model):
    JoinKey = models.CharField(max_length=1000)  # Allow null and blank values
    FieldName = models.CharField(max_length=1000, null=True, blank=True)
    Kafka = models.CharField(max_length=1000, null=True, blank=True)
    Impala = models.CharField(max_length=1000, null=True, blank=True)
    Gemfire = models.CharField(max_length=1000, null=True, blank=True)
    ReconStatus = models.CharField(max_length=1000, null=True, blank=True)
    RequestID = models.CharField(max_length=1000, null=True, blank=True)
    env = models.CharField(max_length=1000, default="Test")
    class Meta:
        db_table = 'neuroreconui_reconresult' 
  
   