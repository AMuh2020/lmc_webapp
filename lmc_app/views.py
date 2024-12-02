from django.shortcuts import render
from .models import Ranking
from .run import run_tests
import time
import os

# Create your views here.

def leaderboard(reqeust):
    order_by = 'mailboxes'
    ld = Ranking.objects.all().order_by(order_by)
    return render(reqeust, 'leaderboard.html',{'data':ld})

def submit(request):
    lmc_file = request.FILES['lmc_file']

    return

def test(request):
    if request.method == 'GET':
        return render(request, "test.html")
    elif request.method == 'POST':
        lmc_file = request.FILES['lmc_file']
        # save file- lmc_file_current_time
        t = time.time()
        file_name = f'lmc_app/lmc_files/lmc_file_{t}'
        with open(file_name, 'wb') as f:
            f.write(lmc_file.read())
        out = run_tests(file_name)
        print(out[2])
        data = {
            'results': out[0],
            'passed': out[1],
            'time_taken': out[2]
        }
        clean_up(file_name)
        return render(request, 'test.html',data)

def clean_up(file_name):
    os.system(f'rm {file_name}')
    return

def howto(request):
    return render(request, 'how_to.html')