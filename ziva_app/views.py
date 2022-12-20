import base64
import json

import time

from django.shortcuts import render,HttpResponse

import requests

class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        return json.JSONEncoder.default(self, obj)

from .models import StoreList,Store,Region
# Create your views here.
def index(request):
    return render(request,'base.html')

def store_master(request):

        url = "http://13.235.112.1/ziva/mobile-api/store-master-list.php"


        payload = "{\r\n    \"accesskey\":\"MDY5MjAyMDIyLTEyLTE3IDA2OjE1OjU4\"\r\n  \r\n}"
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        print(data)
        store_masterlist= data['storemasterlist']

        for i in store_masterlist :
            store_list =  StoreList(
                store_name =i['storename'],
                gst_No =i['gstnumber'],
                trade_licence=i['tradelicenceno'],
                food_licence =i['foodlicence'],
                store_location =i['storelocation'],

            )
            store_list.save()
            all_data = StoreList.objects.all().order_by('-id')

            return render(request, 'masters/store_master_list.html', {"list":all_data})




def add_store(request):
    url = "http://13.235.112.1/ziva/mobile-api/region-list.php"
    payload = json.dumps({
        "accesskey": "MDgxNzcyMDIyLTExLTA5IDE1OjI0OjQ2",
        "regionid": ""
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    res_region=response.json()
    print(res_region)
    region = res_region['regionlist']

    for i in region:
        region_list = Region(
            code=i['regionid'],
            name=i['regionname'])
        region_list.save()
        all_data = Region.objects.all().order_by('-id')

    url = "http://13.235.112.1/ziva/mobile-api/statelist.php"

    payload = json.dumps({
        "accesskey": "MDgxNzcyMDIyLTExLTA5IDE1OjI0OjQ2",
        "category": "Indian"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    res_state = response.json()
    state_list = res_state['statelist']
    #data = state_list['state']
    for i in state_list:
        state = Store(state=i['state'])
    state.save()

    data = Store.objects.all().order_by('-id')


    if request.method == "POST":
        attempt_num = 0
        url = "http://13.235.112.1/ziva/mobile-api/add-storemaster.php"
        payload ={
                    'accesskey': 'MDY5MjAyMDIyLTEyLTE3IDA2OjE1OjU4',
                    "storename": request.POST.get("storename"),
                    'storeattachfilename' : request.FILES.get("storephoto").name,
                    'storephoto': base64.b64encode(request.FILES.get("storephoto").file.read()),
                    'legalname': request.POST.get("legalname"),
                    'region': request.POST.get("region"),
                    'gstnumber':request.POST.get("gstnumber"),
                    'gstattachfilename': request.FILES.get("gstattach").name,
                    'pancard': request.POST.get("pancard"),
                    'panattachfilename': request.FILES.get("panattach").name,
                    'foodlicence': request.POST.get("foodlicence"),
                    'flattachfilename': request.FILES.get("flattach").name,
                    'tradelicenceno': request.POST.get("tradelicenceno"),
                    'tlattachfilename': request.FILES.get("tlattach").name,
                    'storelocation': request.POST.get("storelocation"),
                    'emailid':request.POST.get("email"),
                    'storeaddress': request.POST.get("storeaddress"),
                    'pincode': request.POST.get("pincode"),
                    'state': request.POST.get('state'),
                    'contactperson': request.POST.get("contactperson"),
                    'mobileno': request.POST.get("mobileno"),
                    'remarks': request.POST.get("remarks"),
                    'gstattach': base64.b64encode(request.FILES.get("gstattach").file.read()),
                    'panattach': base64.b64encode(request.FILES.get("panattach").file.read()),
                    'flattach': base64.b64encode(request.FILES.get("flattach").file.read()),
                    'tlattach':base64.b64encode(request.FILES.get("tlattach").file.read()),


                }
        payload=json.dumps(payload,cls=BytesEncoder)
        #loaded_r = json.loads(payload)
        #data=payload.json()
        headers = {
                'Content-Type': 'application/json'
                }
        r = requests.post(url, payload , headers=headers)
        print(r)
        if r.status_code == 200:
            data = r.json()
            return HttpResponse('success fully submitted')
        else:
            attempt_num += 1
            # You can probably use a logger to log the error here
            time.sleep(5)  # Wait for 5 seconds before re-trying
            return HttpResponse("Request failed")
    else:
        return render(request,'masters/store_master_add.html',{'state':data, 'data1': all_data})

def item_add(reuest):
    return render(reuest,'Item_master/item_add.html')

def item_list(reuest):
    return render(reuest,'Item_master/item_list.html')

def category_list(request):
    return render(request,'Category_master/category_list.html')

def category_add(request):
    return render(request,'Category_master/category_add.html')

def region_add(request):
    return render(request,'region/region_add.html')

def region_list(request):
    return render(request,'region/region_list.html')
def warehouse_list(request):
    return render(request,'warehouse/warehouse_list.html')
def warehouse_add(request):
    return render(request,'warehouse/warehouse_add.html')

