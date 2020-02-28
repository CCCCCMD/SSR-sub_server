import requests
import base64
import socket

url="https://ncuc.xyz/link/wgD3WQua7Txejttf?mu=1"

def decode_base64(string):
    if(len(string)%4==1):
        string=string+'==='
    elif(len(string)%4==2):
        string=string+'=='
    elif(len(string)%4==3):
        string=string+'='
    return base64.b64decode(string).decode("utf-8")

def connection_host(host, port):
    """
    测试防火墙是否开通
    :param host: 主机ip
    :param port: 主机端口
    :return:
    """
    cli = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    cli.settimeout(1)
    try:
        """
        处理正常连接
        """
        cli.connect((host, int(port)))
        cli.close()
        return 0
    except ConnectionRefusedError as cre:
        """
        处理端口关闭
        """
        return 1
    except socket.timeout as scto:
        """
        处理主机不通
        """
        return -1
 
def get_ssr_list(url):
    response=requests.get(url)
    decrypt_msg=decode_base64(response.text)
    decrypt_msg=decrypt_msg.replace(' ','')
    ssr_list=decrypt_msg.split('ssr://')[1:]
    return ssr_list

def decode_ssr_list(ssr_list):
    decode_list=[]
    for i in range(0,len(ssr_list)):
        if('_' in ssr_list[i]):
            tmp=ssr_list[i].split('_')
            decode_list.append(decode_base64(tmp[0])+'?'+decode_base64(tmp[1]))
        else:
            decode_list.append(decode_base64(ssr_list[i]))
    return decode_list

def trans_config_list(decode_list):
    config_list=[]
    for t in range(0,len(decode_list)):
        i=decode_list[t]
        former_data=i.split('/?')[0]
        params=former_data.split(':')
        config_dict={
            'server_ip': params[0],
            'server_port': params[1],
            'protocol':  params[2],
            'method': params[3],
            'obfs': params[4],
            'password': decode_base64(params[5]),
            'data':i,
            'index':t
        }
        config_list.append(config_dict)
    return config_list

def test_ip(config_list,ssr_list):
    green_list=[]
    for i in config_list:
        if(connection_host(i['server_ip'],i['server_port'])==0):
            green_list.append(ssr_list[i['index']])
    return green_list

def generate_res(green_list):
    res=''
    for i in green_list:
        res=res+'ssr://'+i+' '
    res=base64.b64encode(bytes(res, encoding = "utf8")  )
    return res

def get_res(url):
    ssr_list=get_ssr_list(url)
    decode_list=decode_ssr_list(ssr_list)
    config_list=trans_config_list(decode_list)
    green_list=test_ip(config_list,ssr_list)
    res=generate_res(green_list)
    with open('ssr_res','w') as f:
        f.write(str(res, encoding = "utf8"))

get_res(url)