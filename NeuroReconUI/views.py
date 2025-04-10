from django.forms import ValidationError
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ChartPanelCOB,ReconVO,ReconResult,RequestVO,GZTable, Jobs,Sidebar,HeaderPanel,ChartPanel,Table, PipeLine ,GemfireCountTable1,SKReconTable
from .serializers import ItemSerializer,GemfireItemSerializer,ReconResultItemSerializer,SKReconItemSerializer,GreenZoneItemSerializer,JobsItemSerializer
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse


def logout_view(request):
    logout(request)  # This logs the user out
    return redirect('login')  # Redirect to the homepage after logging out



def login_view(request):
    if request.method == 'POST':
        # Process the login form (authentication logic should be added here)
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user using Django's authentication system
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Authentication successful, login the user
            login(request, user)
            
            # Redirect to the 'next' URL if it exists (or to homepage if not)
            next_url = request.GET.get('next', reverse('home'))  # 'home' is the name of the homepage URL
            return HttpResponseRedirect(next_url)
        else:
            # If authentication fails, show an error message
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})

    # If GET request, render the login page
    return render(request, 'login.html')



@login_required
def home(request):
    sideBarList=Sidebar.objects.all().order_by('seq')
    headerPanelList=HeaderPanel.objects.all().order_by('seq')
    chartPanelList=ChartPanel.objects.all().order_by('seq')
    chartPanelListcob=ChartPanelCOB.objects.all().order_by('seq')
    gemfireCountList=GemfireCountTable1.objects.all()
    skReconTableList=SKReconTable.objects.all()
    tablelList=Table.objects.all()
    pipeLineList=PipeLine.objects.all()
    greenList=GZTable.objects.all()
    jobList=Jobs.objects.all()
    context={
      'sideBarList':sideBarList, 
      'headerPanelList':headerPanelList,
      'chartPanelList':chartPanelList,
      'chartPanelListcob':chartPanelListcob,
      'gemfire' : gemfireCountList,
      'tablelList':tablelList ,
      'pipeLineList':pipeLineList,
      'skReconTableList':skReconTableList,
      'greenList':greenList,
      'jobList':jobList,

    }

    return render(request,"home.html",context);

@api_view(['POST'])    
def save_recon_data(request):
       serilizer=ItemSerializer(data=request.data)
       if serilizer.is_valid():
             serilizer.save()
             return Response(serilizer.data)
       else:
             raise ValidationError(serilizer.errors)
             

@api_view(['GET'])
def get_recon_data(request):
        recon=ReconVO.objects.all()
        serializer=ItemSerializer(recon,many=True)
        return Response(serializer.data);


@api_view(['GET'])
def get_regioncount_data(request):
        recon=GemfireCountTable1.objects.all()
        serializer=GemfireItemSerializer(recon,many=True)
        return Response(serializer.data);


@api_view(['GET'])
def get_skrecon_data(request):
        recon=SKReconTable.objects.all()
        serializer=SKReconItemSerializer(recon,many=True)
        return Response(serializer.data);

@api_view(['GET'])
def get_gz_data(request):
        recon=GZTable.objects.all()
        serializer=GreenZoneItemSerializer(recon,many=True)
        return Response(serializer.data);


@api_view(['GET'])
def get_jobs_data(request):
        recon=Jobs.objects.all()
        serializer=JobsItemSerializer(recon,many=True)
        return Response(serializer.data);


@api_view(['GET'])
def get_recon_result(request, req_id=None):
    """
    This view retrieves ReconResult data for a specific reqId or all data if no reqId is provided.
    """
    try:
        if req_id:
            recon = ReconResult.objects.filter(RequestID=req_id)  # Filter by the provided reqId
        else:
            recon = ReconResult.objects.all()  # If no reqId is provided, return all results

        if not recon.exists():
            return Response({'message': 'No data found for the provided reqId.'}, status=200)

        serializer = ReconResultItemSerializer(recon, many=True)
        return Response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


