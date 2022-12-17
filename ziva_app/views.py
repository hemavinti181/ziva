from django.shortcuts import render

import requests

from .models import StoreList,Store
# Create your views here.
def index(request):
    return render(request,'base.html')

def store_master(request):
    if request.method == 'POST':
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
        return render(request,'masters/store_master_list.html')


def add_store(request):
    url = "http://13.235.112.1/ziva/mobile-api/add-storemaster.php"

    payload = "{\r\n   \"accesskey\":\"MDY5MjAyMDIyLTEyLTE3IDA2OjE1OjU4\",\r\n   \r\n   \"storename\":\"test\",\r\n   \"gstnumber   \":\"12\",\r\n   \"pancard\":\"523\",\r\n   \"contactperson\":\"523\",\r\n   \"mobileno\":\"523\",\r\n   \"remarks\":\"523\",\r\n   \"region\":\"523\",\r\n   \"emailid\":\"523\",\r\n   \"legalname   \":\"523\",\r\n   \"storephoto\":\"523\",\r\n   \"tradelicenceno  \":\"23\",\r\n   \"tlattach\":\"\",\r\n   \"foodlicence\":\"5\",\r\n   \"flattach\":\"test.pdf\",\r\n   \"storelocation\":\"currentlocation\",\r\n   \"storeaddress\":\"sdgfdgf\",\r\n   \"state\":\"sgfh\",\r\n   \"pincode\":\"58896\",\r\n   \"panattach\":\"test.pdf\",\r\n   \"gstattach\":\"test.pdf\",\r\n   \"panattachfilename\":\"\",\r\n   \"gstattachfilename\":\"\",\r\n   \"flattachfilename\":\"\",\r\n   \"tlattachfilename\":\"\",\r\n   \"storeattachfilename\":\"\"\r\n}"
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    print(data)
    #store_masterlist = data['']

    for i in data:
        store_add = StoreList(store_name=i['storename'],gst_No=i['gstnumber'],store_file =i['storephoto'],legal_name =i['legalname'],
                              select_region = i['region'], gst_attach =i['gstattach'], pan_card =i['pancard'],pan_attach = i['panattach'],
                              food_licence=i['foodlicence'],food_attach = i['flattach'],trade_licence = i['tradelicenceno'],trade_attach =i['tlattach'],
                              store_location =i['storelocation'],address = i['storeaddress'],pincode =i['pincode'],state=i['state'],contact_person = i['contactperson'],
                              mobile =i['mobileno'], remarks =i['remarks'])
        store_add.save()
        all_data = Store.objects.all().order_by('-id')
    return render(request,'masters/store_master_add.html')

def item_master(request):
    return render(request,'Item_master/item_list.html')

def item_add(request):
    return render(request,'Item_master/item_add.html')

def category_master(request):
    return render(request,'Category_master/category_list.html')

def category_add(request):
    return render(request,'Category_master/category_add.html')

