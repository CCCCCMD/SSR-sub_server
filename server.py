#coding=utf-8
import flask

server=flask.Flask(__name__)#__name__代表当前的python文件。把当前的python文件当做一>个服务启动
from gevent.pywsgi import WSGIServer
@server.route('/sub_ssr',methods=['get'])#只有在函数前加上@server.route (),这个函数才是>个接口，不是一般的函数
def reg():
    with open('ssr_res','r') as f:
        res=f.read()
    return res
#server.run(port=7777,debug=True,host='0.0.0.0')
#端口不写默认是5000.debug=True表示改了代码后不用重启，会自动帮你重启.host写0.0.0.0，别人就可以通过ip访问接口。否则就是127.0.0.1
WSGIServer(('0.0.0.0', 80), server).serve_forever()