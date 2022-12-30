import paramiko

# 1. 基于用户名密码上传
def sftp_put(local_file, remote_file):
    transport = paramiko.Transport(('10.37.2.2', 22))
    transport.connect(username='root', password='***')

    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_file, remote_file)

    transport.close()

# 1. 基于用户名密码下载
def sftp_get(remote_file, local_file):
    transport = paramiko.Transport(('10.37.2.2', 22))
    transport.connect(username='root', password='***')

    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get(remote_file, local_file)

    transport.close()

# 2. 基于公钥秘钥上传下载
# def sftp_rsa_put_get():
#     private_key = paramiko.RSAKey.from_private_key_file('C:/Users/**/.ssh/id_rsa')

#     transport = paramiko.Transport(('123.57.2.2', 22))
#     transport.connect(username='root', pkey=private_key)

#     sftp = paramiko.SFTPClient.from_transport(transport)
#     sftp.put('file/123.txt', '/vrfct_test/test/123.txt')
#     sftp.get('/vrfct_test/test/abc.txt', 'file/abc.txt')

#     transport.close()



class SSHConnection(object):

    def __init__(self, host:str, port:int, username:str, pwd:str):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.__transport = None

    def upload(self,local_file,remote_file)->bool:
        self.connect()  
        self.uploadInternal(local_file,remote_file)
        # self.cmd('df')  # 执行df 命令
        self.close()    # 关闭连接
        return True

    def download(self,remote_file,local_file)->bool:
        self.connect()  
        self.downloadInternal(remote_file, local_file)
        # self.cmd('df')  # 执行df 命令
        self.close()    # 关闭连接
        return True

    def connect(self)->bool:
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.pwd)
        self.__transport = transport
        return True

    def close(self)->bool:
        self.__transport.close()
        return True

    def uploadInternal(self,local_file,remote_file):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.put(local_file,remote_file)

    def downloadInternal(self,remote_file,local_file):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.get(remote_file,local_file)

    def cmd(self, command, printFlag=True):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host,self.port,self.username,self.pwd)

        (stdin, stdout, stderr) = ssh.exec_command(command)

        errs = stderr.readlines()
        if errs:
            for err in errs:
                raise RuntimeError(err)

        files = stdout.readlines()
        if printFlag:
            for i in files:
                # 打印执行反馈结果
                print(i, end='')
        ssh.close()
        return files

if __name__ == '__main__':
    # 1. 基于用户名密码上传下载
    # sftp_put()
    # sftp_get()

    # 2. 基于公钥秘钥上传下载
    # transport_rsa_put_get()

    # 3. 实现远程命令执行和文件上传
    pass
    # conn = SSHConnection("192.168.100.27", 22, 'yzou', 'DolphinDB123')
    # serverFilePath = conn.cmd(r"cd /hdd/hdd5/hzy/test_report/server/ && find . -name '*.txt'")
    # # print(serverFilePath)
    # # conn.cmd("cat /hdd/hdd5/hzy/test_report/server/release130/olap_engine/cluster_mode/*")

    # for path0 in serverFilePath:
    #     test_time = ''
    #     server_build_time = ''
    #     version = ''
    #     total_falied = ''
    #     status = 0
    #     info = ''
    #     fails = 0
    #     path = path0.replace('\n','')
    #     # path = serverFilePath[0].replace('\n','')
    #     version = path.split('/')[1]

    #     fileInfo = conn.cmd("cd /hdd/hdd5/hzy/test_report/server/ && cat {}".format(path), False)
    #     # print(fileInfo)
    #     for msg in fileInfo:
    #         info += msg
    #         # print(msg)
    #         if '#Fail/#Total Testing Cases:' in msg:
    #             total_falied = msg.split(': ')[1].replace('\n','')
    #             fails = int(total_falied.split('/')[0] if total_falied.split('/')[0] !='' else 0)

    #         elif 'server编译时间:' in msg:
    #             server_build_time = msg.split(': ')[1].replace('\n','')

    #         elif '测试时间:' in msg:
    #             test_time = msg.split(': ')[1].replace('\n','')

    #         elif 'The following cases may crash:' in msg or 'Blocking cases:' in msg:
    #             status=1

    #     if status != 1 and fails > 0:
    #         status=2
    #     elif status != 1 and fails == 0:
    #         status=0
        
    #     print("{}, {}, {}, {}, {}".format(test_time,server_build_time,version,total_falied,status))
        
        
        
        


