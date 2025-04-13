from django.contrib import admin
from .models import SCDVO,GZTable,ChartPanelCOB,ReconResult,Jobs,ReconVO,RequestVO, Sidebar,Table,ChartPanel,PipeLine,HeaderPanel,GemfireCountTable1,SKReconTable

admin.site.register(Sidebar)
admin.site.register(HeaderPanel)
admin.site.register(ChartPanel)
admin.site.register(RequestVO)
admin.site.register(Table)
admin.site.register(PipeLine)
admin.site.register(GemfireCountTable1)
admin.site.register(ChartPanelCOB)
admin.site.register(SKReconTable)
admin.site.register(ReconVO)
admin.site.register(GZTable)
admin.site.register(Jobs)
admin.site.register(ReconResult)
admin.site.register(SCDVO)

