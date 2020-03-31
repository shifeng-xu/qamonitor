import paramiko
import six
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.db import models
from common.models import User
from functools import wraps

# Create your views here.
#用户登录接口
from common import sshutils

# 说明：这个装饰器的作用，就是在每个视图函数被调用时，都验证下有没法有登录，
# 如果有过登录，则可以执行新的视图函数，
# 否则没有登录则自动跳转到登录页面。
def check_login(f):
    @wraps(f)
    def inner(request,*arg,**kwargs):
        if request.session.get('is_login')=='1':
            return f(request,*arg,**kwargs)
        else:
            return redirect('/login/')
    return inner

def login(request):
    if request.method=="GET":
        return render(request, "login.html")
    elif request.method=="POST":
         username=request.POST.get('username')
         password=request.POST.get('password')
         user=User.objects.filter(username=username,password=password)
         num=len(user)
         response_data = {}
         if(num>0):
         #if(username=='admin' and password=='admin'):
            #return HttpResponse("Hello".encode('utf-8'))

             response_data['port'] = 8680
             response_data['status'] = 'alive'
             response_data['username'] = username
             #return render(request, "index.html", response_data)
             # 登录成功
             # 1，生成特殊字符串
             # 2，这个字符串当成key，此key在数据库的session表（在数据库存中一个表名是session的表）中对应一个value
             # 3，在响应中,用cookies保存这个key ,(即向浏览器写一个cookie,此cookies的值即是这个key特殊字符）
             request.session['is_login'] = '1'  # 这个session是用于后面访问每个页面（即调用每个视图函数时要用到，即判断是否已经登录，用此判断）
             # request.session['username']=username  # 这个要存储的session是用于后面，每个页面上要显示出来，登录状态的用户名用。
             # 说明：如果需要在页面上显示出来的用户信息太多（有时还有积分，姓名，年龄等信息），所以我们可以只用session保存user_id
             request.session['user_id'] = user[0].id

             #return render(request,"bugsoffline_new.html",response_data)
             #return render(request,"index.html",response_data)
             return redirect('/quality/bugsoffline')
         else:
             response_data['iserror']=True
             response_data['errmsg']='用户名或密码不正确!'
             return render(request, "login.html",response_data)
    else:
        return redirect('/login/')

def logout(request):
    request.session.flush()
    return redirect('/login/')

@check_login
def index(request):
    return render(request,"index.html")

#展示监控页面
def monitorTable(request):
    response_data=execmd('netstat -an|grep 8680')
    return render(request, "tables2.html", response_data)




def table(request):
    # 配置私人密钥文件位置
    private_key_path = '/Users/a10998/.ssh/privatekey.pem'
    key = paramiko.RSAKey.from_private_key_file(private_key_path)
    # 实例化SSHClient
    ssh = paramiko.SSHClient()
    # 自动添加策略，保存服务器的主机名和密钥信息，如果不添加，那么不再本地know_hosts文件中记录的主机将无法连接
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接SSH服务端，以用户名和密码进行认证
    ssh.connect(hostname='13.114.100.129', port=22, username='work', pkey=key)
    stdin, stdout, stderr = ssh.exec_command('netstat -an|grep 8680')
    # 获取命令结果
    res = to_str(stdout.read())
    str_res=str(res,'utf-8')
    # 获取错误信息
    error = to_str(stderr.read())
    str_error = str(res, 'utf-8')
    #关闭连接
    ssh.close()
    # 如果有错误信息，返回error
    # 否则返回res
    response_data = {}

    if error.strip():
        return HttpResponse(str_error)
        #return str_error
    else:
        response_data['port'] = 8680
        response_data['status'] = 'alive'
        return render(request, "tables2.html", response_data)
        #return str_res


def to_str(input_, encoding='utf-8', errors='replace'):
    '''Convert objects to string, encodes to the given encoding

    :rtype: str

    >>> to_str('a')
    b'a'
    >>> to_str(u'a')
    b'a'
    >>> to_str(b'a')
    b'a'
    >>> class Foo(object): __str__ = lambda s: u'a'
    >>> to_str(Foo())
    'a'
    >>> to_str(Foo)
    "<class 'python_utils.converters.Foo'>"
    '''
    if isinstance(input_, six.binary_type):
        pass
    else:
        if not hasattr(input_, 'encode'):
            input_ = six.text_type(input_)

        input_ = input_.encode(encoding, errors)
    return input_


def connect():
    # 配置私人密钥文件位置
    private_key_path = '/Users/a10998/.ssh/privatekey.pem'
    key = paramiko.RSAKey.from_private_key_file(private_key_path)
    # 实例化SSHClient
    ssh = paramiko.SSHClient()
    # 自动添加策略，保存服务器的主机名和密钥信息，如果不添加，那么不再本地know_hosts文件中记录的主机将无法连接
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接SSH服务端，以用户名和密码进行认证
    ssh.connect(hostname='13.114.100.129', port=22, username='work', pkey=key)
    return ssh

def execmd(cmd):
    # 配置私人密钥文件位置
    private_key_path = '/Users/a10998/.ssh/privatekey.pem'
    key = paramiko.RSAKey.from_private_key_file(private_key_path)
    # 实例化SSHClient
    ssh = paramiko.SSHClient()
    # 自动添加策略，保存服务器的主机名和密钥信息，如果不添加，那么不再本地know_hosts文件中记录的主机将无法连接
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接SSH服务端，以用户名和密码进行认证
    ssh.connect(hostname='13.114.100.129', port=22, username='work', pkey=key)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    # 获取命令结果
    res = to_str(stdout.read())
    str_res=str(res,'utf-8')
    # 获取错误信息
    error = to_str(stderr.read())
    str_error = str(res, 'utf-8')
    #关闭连接
    ssh.close()
    # 如果有错误信息，返回error
    # 否则返回res
    response_data = {}
    response_data['port'] = 8680
    response_data['status'] = 'alive'
    return response_data

def readlog(request):
    pos = 0
    str_re=""
    index=0
    while index<3:
        con = open("/Users/a10998/mytest/service.debug.log.wf")
        if pos != 0:
            con.seek(pos, 0)
        while True:
            line = con.readline()
            if line.strip():
                str_re+=line.strip()+'\r\n'
            pos = pos + len(line)
            if not line.strip():
                break
        con.close()
        index=index+1
    return HttpResponse(str_re)


def db_handle(request):
    models.UserInfo.objects.create(username='andy',password='123456',age=33)
    return HttpResponse('OK')


