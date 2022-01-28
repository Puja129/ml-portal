import requests
import re
import os
import json
import base64
import time

config=[]
gw_tkn = r'/v1/api/token/validate'
gw_adm = r'/v1/admin/accounts/validate'
gw_rep = r'/v1/reports/usage'
srv = r'/v1/api/gateways'
cfg=[]

# Parse IPs
def parse_ip(token, svc_id, docx_file):
    with open(docx_file, 'r') as fr:
    	fstring = fr.readlines()

    agt_gtw=[]
    agt_gtw_tkn=[]
    agt_gtw_adm=[]
    agt_srv=[]
    agt_non=[]

    gw_rep_lst=[]
    gw_tkn_lst=[]
    gw_adm_lst=[]
    srv_lst=[]
    lst=[]

    for line in fstring:
        if line.find(gw_rep) != -1:
            agt_gtw.append(line.strip())
            result = re.findall(r'[0-9]+(?:\.[0-9]+){3}',line)
            tmp0=[]
            for ip in result:
                tmp0.append(ip)
            for ip in tmp0:
                if ip not in gw_rep_lst:
                    gw_rep_lst.append(ip)
        elif line.find(gw_adm) != -1:
            agt_gtw_adm.append(line.strip())
            m = line[line.find(start:='/v1/admin/accounts/validate?')+len(start):line.find(' HTTP')]
            tmp=[]
            if m.find('. (EC Internal API') == -1:
                m = m.replace('agtId1','client-id')
                m = m.replace('agtId2','server-id')
                tmp.append(m)
            for item in tmp:
                if item not in cfg:
                    cfg.append(item)
            result1 = re.findall(r'[0-9]+(?:\.[0-9]+){3}',line)
            tmp1=[]
            for ip1 in result1:
                tmp1.append(ip1)
            for ip1 in tmp1:
                if ip1 not in gw_adm_lst:
                    gw_adm_lst.append(ip1)
        elif line.find(gw_tkn) != -1:
            agt_gtw_tkn.append(line.strip())
            result2 = re.findall(r'[0-9]+(?:\.[0-9]+){3}',line)
            tmp2=[]
            for ip2 in result2:
                tmp2.append(ip2)
            for ip2 in tmp2:
                if ip2 not in gw_tkn_lst:
                    gw_tkn_lst.append(ip2)
        elif line.find(srv) != -1:
            agt_srv.append(line.strip())
            result3 = re.findall(r'[0-9]+(?:\.[0-9]+){3}',line)
            tmp3=[]
            for ip3 in result3:
                tmp3.append(ip3)
            for ip3 in tmp3:
                if ip3 not in srv_lst:
                    srv_lst.append(ip3)
        else:
            agt_non.append(line.strip())
            result4 = re.findall(r'[0-9]+(?:\.[0-9]+){3}',line)
            tmp4=[]
            for ip4 in result4:
                tmp4.append(ip4)
            for ip4 in tmp4:
                if ip4 not in lst:
                    lst.append(ip4)
    payload_rep = json.dumps(gw_rep_lst)
    proc_rep = proc(payload_rep, gw_rep)
    print(proc_rep)

    payload_adm = json.dumps(gw_adm_lst)
    proc_adm = proc(payload_adm, gw_adm)

    payload_tkn = json.dumps(gw_tkn_lst)
    proc_tkn = proc(payload_tkn, gw_tkn)

    payload_srv = json.dumps(srv_lst)
    proc_srv = proc(payload_srv, srv)

    payload_non = json.dumps(lst)
    proc_non = proc(payload_non, '')

    result = str(proc_non)

    ## uncomment below line and provide app-name
    #result2 = ('{\"parent\":\"app-name\",\"'+svc_id+'\":'+result+'}')

    os.remove(docx_file)

    kv = {key:svc_id}
    if os.path.exists('geoloc.json'):
        a_file = open("geoloc.json", "r")
        json_object = json.load(a_file)
        a_file.close()

        json_object.update(kv)
        a_file = open("geoloc.json", "w")
        json.dump(json_object, a_file)
        a_file.close()

    else:
        a_file = open("geoloc.json", "w")
        json.dump(kv, a_file)
        a_file.close()

    return result

# Get the geo-location for the IPs
def proc(payload, path):
    print(path)
    response = requests.post("http://ip-api.com/batch", data=payload).json()
    resp = json.dumps(response)
    for ip_info in response:
        sts = ip_info["status"]
        if sts == 'success':
            ip = ip_info["query"]
            if path == srv:
                y = {"agent":"server","config":"null","path":path,"ip":ip}
            elif path == gw_tkn:
                y = {"agent":"gateway","config":"null","path":path,"ip":ip}
            elif path == gw_rep:
                y = {"agent":"gateway","config":"null","path":path,"ip":ip}
            elif path == gw_adm:
                y = {"agent":"gateway","config":cfg,"path":path,"ip":ip}
            else:
                y = {"agent":"unknown","config":"null","path":path,"ip":ip}
            ip_info.update(y)
            config.append(ip_info)
    respNew = json.dumps(config)
    return respNew

#Get Refreshed hash
def get_refreshed_hash(hash):
    headersAPI = {
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded',
    }
    data = {
    'hash': hash
    }
    ### uncomment the below line for 'url01' and provide the seeder/app URL
    #url01 = "app-url/v1.2beta/crypto/refreshed"
    response = requests.post(url01, headers=headersAPI, data=data)
    api_response = response.json()
    return api_response

# Get token
def get_tkn(username, password):
    consumer_key_secret = username+":"+password
    consumer_key_secret_enc = base64.b64encode(consumer_key_secret.encode()).decode()
    headersAuth = {
    'Authorization': 'Basic '+ str(consumer_key_secret_enc),
    }
    data = {
    'grant_type': 'client_credentials'
    }
    ### uncomment the below line for 'oauth2Url' and provide the SDC URL
    #oauth2Url = "sdc-url/oauth/token"
    response = requests.post(oauth2Url, headers=headersAuth, data=data, verify=True)
    j = response.json()
    return j['access_token']

# Validate token
def validate_token(token):
    headersAPI = {
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded',
    'Authorization': 'Bearer '+token,
    }
    data = {
    'token': token
    }
    ### uncomment the below line for 'urlV' and provide the SDC URL
    #urlV = "sdc-url/introspect"
    response = requests.post(urlV, headers=headersAPI, data=data)
    return response.status_code

# Post data to embedded db
def post_data(tkn, svc_id, req):
    headersAPI = {
    'accept': 'application/json',
    'Authorization': 'Bearer '+tkn,
    }
    ## uncomment the below line for 'url01' and provide the seeder/app URL
    #url0 = "app-url/v1.2beta/ec/api/"+svc_id
    response = requests.post(url0, headers=headersAPI, data=req)
    api_response = response.json()
    return api_response['key']
