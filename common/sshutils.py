import paramiko
import six


def connect(ip,port,uname):
    # 配置私人密钥文件位置
    private_key_path = '/Users/a10998/.ssh/privatekey.pem'
    key = paramiko.RSAKey.from_private_key_file(private_key_path)
    # 实例化SSHClient
    ssh = paramiko.SSHClient()
    # 自动添加策略，保存服务器的主机名和密钥信息，如果不添加，那么不再本地know_hosts文件中记录的主机将无法连接
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接SSH服务端，以用户名和密码进行认证
    ssh.connect(hostname=ip, port=port, username=uname, pkey=key)
    a=1
    b=2
    return ssh

def execmd(ssh,cmd):
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


def to_str(slef,input_, encoding='utf-8', errors='replace'):
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


