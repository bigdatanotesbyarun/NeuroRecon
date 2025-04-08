from django.urls import path
from . import ChatExcel,views,Chat,ClientServices,Chart,ChatDB,Recon


urlpatterns = [
    path('home/', views.home,name="home"),
    path('audit/',Recon.audit, name='audit'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('get_recon_data/', views.get_recon_data, name='get_recon_data'),
    path('get_recon_result/', views.get_recon_result, name='get_recon_result'),
    path('save_recon_data/', views.save_recon_data, name='save_recon_data'),
    path('get_regioncount_data/', views.get_regioncount_data, name='get_regioncount_data'),
    path('get_skrecon_data/', views.get_skrecon_data, name='get_skrecon_data'),
    path('get_gz_data/', views.get_gz_data, name='get_gz_data'),
    path('get_jobs_data/', views.get_jobs_data, name='get_jobs_data'),
    path('get_jobs_data/', views.get_jobs_data, name='get_jobs_data'),
    path('get_chat_dataPDF/', Chat.get_chat_dataPDF, name='get_chat_dataPDF'),
    path('get_chat_dataEXCEL/', ChatExcel.get_chat_dataEXCEL, name='get_chat_dataEXCEL'),
    path('get_data_from_natural_language_query/',ChatDB.get_data_from_natural_language_query, name='get_data_from_natural_language_query'),
    path('get_cloud_data/', ClientServices.get_cloud_data, name='get_cloud_data'),
    path('get_kafka_data/', ClientServices.get_kafka_data, name='get_kafka_data'),
    path('get_impala_data/',ClientServices.get_impala_data, name='get_impala_data'),
    path('get_gemfire_data/',ClientServices.get_gemfire_data, name='get_gemfire_data'),
  
    path('chart1/', Chart.chart1, name='chart1'),
    path('chart2/', Chart.chart2, name='chart2'),
    path('chart3/', Chart.chart3, name='chart3'),
    path('chart4/', Chart.chart4, name='chart4'),
    path('chart5/', Chart.chart5, name='chart5'),
    path('chart6/', Chart.chart6, name='chart6'),
    path('chart7/', Chart.chart7, name='chart7'),
    path('chart8/', Chart.chart8, name='chart8'),
   
]