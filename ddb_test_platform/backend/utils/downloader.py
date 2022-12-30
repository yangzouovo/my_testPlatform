from .SFTPClient import SSHConnection
import re
import os

class SFTPDownloader:
    def __init__(self,host,port,user,password) -> None:
        self.conn = SSHConnection(host, port, user, password)
        self.conn.connect()

    def download(self,remote_file, local_file) -> bool:
        """从远程服务器下载单个文件"""
        # print(remote_file, local_file)
        if not self.conn.download(remote_file, local_file):
            print('download remote file: ' + remote_file+'failed.')
        return True

    def download_dir(self, remote_dir, local_dir) -> bool:
        """下载远程服务器指定目录下的所有文件到本地目录, 且子目录结构一致"""
        if local_dir[-1] != '/':
            local_dir = local_dir + '/'

        if remote_dir[-1] != '/':
            remote_dir = remote_dir + '/'
        files = self.search_file(remote_dir,'*')

        for file_dir in files:
            local = local_dir+ os.path.split(file_dir)[0]
            if not os.path.exists(local):
                os.makedirs(local)
            self.download(remote_dir+ file_dir, local_dir+ file_dir)
        return True


    def search_file(self, remote_dir, type)->list:
        """查询远程服务器指定目录下的，指定类型文件"""
        if type == '*':
            file0=self.conn.cmd("cd "+ remote_dir +" && find . -name '*."+type+"'")[1:]
        else:
            file0=self.conn.cmd("cd "+ remote_dir +" && find . -name '*."+type+"'")
        return [path.replace('\n','').replace('./','') for path in file0]

    def get_fileinfo(self, remote_file_dir, show_detail=False):
        """列出指定文件内容, 返回一个list"""
        return self.conn.cmd("cat {}".format(remote_file_dir), show_detail)

    def get_file_modify_time(self, remote_file_dir) -> list:
        """查询指定文件的最近修改时间"""
        srcipt = 'stat {} | grep "Modify" | awk'.format(remote_file_dir)
        srcipt = srcipt + """ '{printf($2);printf(" ");print($3)}'"""
        temp = self.conn.cmd(srcipt, False)[0].replace('\n','')
        return temp

    def close(self):
        return self.conn.close()


if __name__ == "__main__":
    do = SFTPDownloader("192.168.100.27", 22, 'yzou', 'DolphinDB123')
    path = '/hdd/hdd5/hzy/test_report/api/java/release130/'
    local = "/home/yzou/Desktop/ddb_test_platform/backend/dist/java/result_122/"
    print(do.get_file_modify_time("/hdd/hdd5/hzy/test_report/api/javascript/master/*.html"))