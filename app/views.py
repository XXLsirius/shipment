from django.http import HttpRequest
from inertia import render


def index(request):
    return render(request, "dashboard", props={"name": "World000"})

def dashboard(request):
    return render(request, "dashboard", props={"pageName": "dashboard"})

def shipping(request):
    return render(request, "shipping", props={"pageName": "shipping"})

def waterArea(request):
    return render(request, "waterArea", props={"pageName": "waterArea"})

def charterer(request):
    return render(request, "charterer", props={"pageName": "charterer"})

def certificate(request):
    return render(request, "certificate", props={"pageName": "certificate"})

def certificateEdit(request):
    id = request.GET.get('id')
    shipPk = request.GET.get('shipPk')
    marinerPk = request.GET.get('marinerPk')
    certtypePk = request.GET.get('certtypePk')
    kind = request.GET.get('kind')

    return render(request, "certificate/edit", props={"id": id, "shipPk" : shipPk, "marinerPk" : marinerPk, "certtypePk" : certtypePk, "kind" : kind})

def ship(request):
    return render(request, "ship", props={"pageName": "ship"})

def shipEdit(request):
    id = request.GET.get('id')
    return render(request, "ship/edit", props={"id": id})

def shipDetail(request):
    id = request.GET.get('id')
    return render(request, "ship/detail", props={"id": id})

def mariner(request):
    return render(request, "mariner", props={"pageName": "mariner"})

def marinerEdit(request):
    id = request.GET.get('id')
    return render(request, "mariner/edit", props={"id": id})

def marinerDetail(request):
    id = request.GET.get('id')
    return render(request, "mariner/detail", props={"id": id})

def certType(request):
    return render(request, "certType", props={"pageName": "certType"})
