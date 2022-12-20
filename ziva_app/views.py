import base64
import json

import time

from django.shortcuts import render,HttpResponse
from .models import StoreList,Store,Region,UOM,Category,Warehouse,Filter
import requests

class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        return json.JSONEncoder.default(self, obj)


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
                    'storeattachfilename':request.FILES.get("storephoto").name,
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

def item_add(request):


    url = "http://13.235.112.1/ziva/mobile-api/dropdwn-table-list.php"
    payload = "{\r\n    \"accesskey\":\"MDY5MjAyMDIyLTEyLTE3IDA2OjE1OjU4\",\r\n    \"name\":\"UOM\"\r\n}"
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response= response.json()
    uom = response['itemmasterlist']

    for i in uom:
        uom_list = UOM(
            code=i['ddcode'],
            name=i['displayname'])
        uom_list.save()
        uom_data = UOM.objects.all().order_by('-id')
    payload = "{\r\n    \"accesskey\":\"MDY5MjAyMDIyLTEyLTE3IDA2OjE1OjU4\",\r\n    \"name\":\"CATEGORY\"\r\n}"
    headers = {
        'Content-Type': 'text/plain'
    }

    response1 = requests.request("GET", url, headers=headers, data=payload)
    response1 = response1.json()
    category = response1['itemmasterlist']

    for i in category:
        cat_list = Category(
            code=i['ddcode'],
            name=i['displayname'])
        cat_list.save()
        cat_data = Category.objects.all().order_by('-id')

    if request.method == "POST":
        attempt_num = 0
        url = "http://13.235.112.1/ziva/mobile-api/add-item-master.php"
        payload = {

                "accesskey": "MDY5MjAyMDIyLTEyLTE3IDA2OjE1OjU4",
                "itemname":request.POST.get('name'),
                "hsncode":request.POST.get('hsncode') ,
                "lpp": request.POST.get('latestpurchase'),
                "gst": request.POST.get("gst"),
                "category":request.POST.get('category'),
                "mrp": request.POST.get('mrp'),
                "manufacturername":request.POST.get('manufacture'),
                "uom": request.POST.get('uom'),
                "image":base64.b64encode(request.FILES.get("imagefile").file.read()),
            }
        payload = json.dumps(payload, cls=BytesEncoder)
        headers = {
            'Content-Type': 'application/json'
        }
        r = requests.post(url, payload, headers=headers)
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

         return render(request,'Item_master/item_add.html', {'uom_data': uom_data,'cat_data':cat_data})

def item_list(reuest):
    return render(reuest,'Item_master/item_list.html')

def category_list(request):
    return render(request,'Category_master/category_list.html')

'''def category_add(request):
    url = "http://13.235.112.1/ziva/mobile-api/dropdown-filter.php"

    payload = "{\r\n        \"accesskey\": \"LTIwMjIxMjE5MjIyMzcy\"\r\n    }\r\n"
    headers = {
        'Content-Type': 'text/plain'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    filter = response['warehouselist']
    for i in filter :
        filter = Filter(
            des=i['dropdownlist'],
            roles =i['ddcode']
            category = i['ddcode']
            states = i['ddcode']
            levels = i['ddcode']
            city = i['ddcode']
            GST = i['ddcode']
       filter.save()
        data = Category.objects.all().order_by('-id')
    return render(request,'Category_master/category_add.html',{'data':data})'''

def region_add(request):
    url = "http://13.235.112.1/ziva/mobile-api/warehousemaster-list.php"

    payload = "{\r\n    \"accesskey\":\"MDY5MjAyMDIyLTEyLTE3IDA2OjE1OjU4\"\r\n   \r\n}"
    headers = {
        'Content-Type': 'text/plain'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    warehouse = response['warehouselist']

    for i in warehouse:
        list = Warehouse(
            code=i['warehouseid'],
            name=i['warehousename'])
        list.save()
        data =Warehouse .objects.all().order_by('-id')
    if request.method == "POST":
        attempt_num = 0
        url = "http://13.235.112.1/ziva/mobile-api/add-regionmaster.php"

        payload ={
            "accesskey": "MDY5MjAyMDIyLTEyLTE3IDA2OjE1OjU4",
            "regionname": request.POST.get("regionname"),
            "gstnumber": request.POST.get("gstnumber"),
            "address":request.POST.get("address") ,
            "region_manager": request.POST.get("regionmanager"),
            "location": request.POST.get("location"),
            "region_contact_no":request.POST.get('mobileno') ,
            "gstattach":base64.b64encode(request.FILES.get("gstattach").file.read()),
            "gstattachfilename": request.FILES.get("gstattach").name,
            "licence":base64.b64encode(request.FILES.get("licattach").file.read()),
            "licencefilename":request.FILES.get("licattach").name,
            #"regionattach":base64.b64encode(request.FILES.get("regionfile").file.read()) ,
             #"regionattachfilename":request.FILES.get("regionfile").name,
            "warehouseid":request.POST.get('wa_id'),
            "warehouse": request.POST.get('warehouse'),
         }
        payload = json.dumps(payload, cls=BytesEncoder)
        # loaded_r = json.loads(payload)
        # data=payload.json()
        headers = {
        'Content-Type': 'application/json'
        }
        r = requests.post(url, payload, headers=headers)
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

        return render(request,'region/region_add.html',{'data':data})

def region_list(request):
    return render(request,'region/region_list.html')
def warehouse_list(request):
    return render(request,'warehouse/warehouse_list.html')
def warehouse_add(request):

    '''ip = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(ip.text)
    response1 = requests.get('http://ip-api.com/json/' + ip_data["ip"])
    res_data = response1.text
    users = json.loads(res_data)'''


    attempt_num = 0
    url = "http://13.235.112.1/ziva/mobile-api/region-list.php"
    payload = json.dumps({
        "accesskey": "MDgxNzcyMDIyLTExLTA5IDE1OjI0OjQ2",
        "regionid": ""
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    res_region = response.json()
    print(res_region)
    region = res_region['regionlist']

    for i in region:
        region_list = Region(
            code=i['regionid'],
            name=i['regionname'])
        region_list.save()
        all_data = Region.objects.all().order_by('-id')
    if request.method == "POST":

        url = "http://13.235.112.1/ziva/mobile-api/add-warehousemaster.php"
        payload = {
            "accesskey": "MDY5MjAyMDIyLTEyLTE3IDA2OjE1OjU4",
            "regionid": request.POST.get('region'),
            "warehousename": request.POST.get('warehousename'),
            "gstnumber": request.POST.get('gstnumber'),
            "licenseno": request.POST.get('licenceno'),
            "panno": request.POST.get('pancard'),
            "address": request.POST.get('storeaddress'),
            "wh_manager": request.POST.get('warehousemamager'),
            "location": request.POST.get('location'),
            "wh_contact_no": request.POST.get('mobileno'),
            "gstattachfilename": request.FILES.get("gstattach").name,
            "panattachfilekename": request.FILES.get('panattach').name,
            "licencefilename": request.FILES.get('licattach').name,
            "warehouseattachfilename": request.FILES.get('warehousefile').name,
            "panattach": base64.b64encode(request.FILES.get('panattach').file.read()),
            "warehouseattach": base64.b64encode(request.FILES.get('warehousefile').file.read()),
            "gstattach": base64.b64encode(request.FILES.get('gstattach').file.read()),
            "licence": base64.b64encode(request.FILES.get('licattach').file.read()),
        }
        payload = json.dumps(payload, cls=BytesEncoder)

        headers = {
            'Content-Type': 'application/json'
        }
        r = requests.post(url, payload, headers=headers)
        print(r)
        if r.status_code == 200:
            data = r.json()
            return HttpResponse('success fully submitted')
        else:
            attempt_num += 1
            # You can probably use a logger to log the error here
            time.sleep(5)  # Wait for 5 seconds before re-trying
            return HttpResponse("Request failed")


    return render(request,'warehouse/warehouse_add.html',{'data':all_data})

def vendor_add(request):
    return render(request,'vendor/vendor_add.html')

def user_add(request):
    return  render(request,'user/user_add.html')

def user_list(request):
    return render(request,'user/user_list.html')