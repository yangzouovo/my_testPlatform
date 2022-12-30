from utils.downloader import SFTPDownloader
from utils.html_merge import merge_css_and_img_to_html
from backend.settings import BASE_DIR
import re
import os
import asyncio
import aiofiles
import datetime

REPORT_SRC=str(BASE_DIR)+"/dist/reports"

class reportParser:
    def __init__(self, host, port, user, passwd) -> None:
        self.serializedData = []
        self.info = []
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd

    def parseData(self, remote_dir, file_type) -> None:
        """async parse and serialize datas"""

        dowloader = SFTPDownloader(self.host, self.port, self.user, self.passwd)
        FilePath = dowloader.search_file(remote_dir, file_type)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [loop.create_task(self.parse(path, dowloader)) for path in FilePath]

        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
        dowloader.close()

    async def parse(self):
        """解析文件信息的方法，可在子类进行重写/重载"""
        pass

    def getData(self) -> list:
        return self.serializedData
        
    def getInfo(self) -> list:
        return self.info
    
    

class ServerParser(reportParser):

    async def parse(self, path, dowloader):
        version = path.split('/')[0]
        test_type = re.findall(f"{version}/(.*?)/result_",path)[0]
        if '/' in test_type:
            test_type = re.findall(f"{version}/(.*?)/result_",path)[0].replace('/','.')

        remote_dir = '/hdd/hdd5/hzy/test_report/server/'+os.path.split(path)[0]
        remote_filename = os.path.split(path)[1]
        local_dir = f"{REPORT_SRC}/server/{version}"+remote_dir.split(version)[1]
        local_file = local_dir +'/'+remote_filename

        if not os.path.exists(local_dir):
            dowloader.download_dir(remote_dir, local_dir)

        elif not os.path.exists(local_file):
            dowloader.download(remote_dir+'/'+remote_filename, local_file)

        fails = 0
        test_time = ''
        server_build_time = ''
        total_falied = ''
        status = 0
        info_ = ''

        async with aiofiles.open(local_file,'r') as f:
            fileInfo = await f.readlines()
            for msg in fileInfo:
                info_ += msg
                # print(msg)
                if '#Fail/#Total Testing Cases:' in msg:
                    total_falied = msg.split(': ')[1].replace('\n','')
                    fails = int(total_falied.split('/')[0] if total_falied.split('/')[0] !='' else 0)

                elif 'server编译时间:' in msg:
                    server_build_time = msg.split(': ')[1].replace('\n','')

                elif '测试时间:' in msg:
                    test_time = msg.split(': ')[1].replace('\n','')

                elif 'The following cases may crash:' in msg or 'Blocking cases:' in msg:
                    status=1

            cur_time = datetime.datetime.now()
            
            # 只获取最近一个月的测试报告
            if(test_time != '' and cur_time > datetime.datetime.strptime(test_time[:10],"%Y-%m-%d") + datetime.timedelta(days=30)):
                return

            if status != 1 and fails > 0:
                status=2
            elif status != 1 and fails == 0:
                status=0
            self.serializedData.append({
                'test_type': test_type,
                'test_time': test_time,
                'server_build_time': server_build_time,
                'version': version,
                'total_falied': total_falied,
                'status': status})
            self.info.append(info_)


class PluginParser(reportParser):

    async def parse(self, path, dowloader:SFTPDownloader):
        remote_dir = '/hdd/hdd5/hzy/test_report/plugin/'+os.path.split(path)[0]
        remote_filename = os.path.split(path)[1]
        test_time = dowloader.get_file_modify_time(remote_dir+'/'+remote_filename)[:-3]
        cur_time = datetime.datetime.now()
        
        # 只获取最近一个月的测试报告
        if(cur_time > datetime.datetime.strptime(test_time[:10],"%Y-%m-%d") + datetime.timedelta(days=30)):
            return

        version = path.split('/')[0]
        local_dir = f"{REPORT_SRC}/plugin/{version}"+remote_dir.split(version)[1]
        local_file = local_dir +'/'+remote_filename

        if not os.path.exists(local_dir):
            dowloader.download_dir(remote_dir, local_dir)

        elif not os.path.exists(local_file):
            dowloader.download(remote_dir+'/'+remote_filename, local_file)

        async with aiofiles.open(local_file,'r') as f:
            fileInfo = await f.readlines()
            # print(fileInfo)

            type_index = []
            plugin_results = []

            for index, msg in enumerate(fileInfo):
                # print(re.findall(r'\[.+\]',msg))
                if re.findall(r'^\[.+\]$',msg):
                    type_index.append(index)
            # print(type_index)

            for row in range(len(type_index)-1):
                cur_msg = fileInfo[type_index[row]:type_index[row+1]]
                # print(cur_msg)
                plugin_results.append(''.join(cur_msg))
            plugin_results.append(''.join(fileInfo[type_index[-1]:]))

            for single_result in plugin_results:
                # print(single_result)
                test_type = ''
                plugin_build_time = ''
                total_falied = ''
                status = 0
                info_ = ''
                fails = -1
                info_ = single_result
                msgs = single_result.split('\n')
                # print(msgs)
                for msg in msgs:
                    if re.findall(r'^\[.+\]$',msg):
                        test_type=msg[1:-1]

                    elif '编译时间:' in msg:
                        plugin_build_time = msg.split(': ')[1]

                    elif '#Fail/#Total Testing Cases:' in msg:
                        total_falied = msg.split(': ')[1]
                        fails = int(total_falied.split('/')[0] if total_falied.split('/')[0] !='' else 0)
                        
                    elif 'crash' in msg.lower() or 'broken' in msg.lower():
                        status=1
                        
                if status !=1:
                    if fails > 0:
                        status=2
                    elif fails == 0:
                        status=0
                    else:
                        status=1
                        
                self.serializedData.append({
                    'test_type': test_type,
                    'test_time': test_time,
                    'plugin_build_time': plugin_build_time,
                    'version': version,
                    'total_falied': total_falied,
                    'status': status})
                self.info.append(info_)

class ApiCppParser(reportParser):

    async def parse(self, path, dowloader):
        version = path.split('/')[0]
        ssl_version = path.split('/')[1]
        test_time = re.findall("result_.+_(.*?)_",path.split('/')[2])[0]
        server_build_time = re.findall(".+_(.*?)\.html",path.split('/')[2])[0]
        total_falied = ''
        status = 0
        success = 0
        fails = 0

        cur_time = datetime.datetime.now()
        # 只获取最近一个月的测试报告
        if(test_time != '' and cur_time > datetime.datetime.strptime(test_time[:10],"%Y-%m-%d") + datetime.timedelta(days=30)):
            return

        build_number = re.findall("result_(.*?)_",path)[0]

        remote_file = "/hdd/hdd5/hzy/test_report/api/cpp/"+path
        local_file = f"{REPORT_SRC}/cpp/{build_number}.html"
        local_dir = os.path.split(local_file)[0]

        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
            dowloader.download(remote_file, local_file)
        elif not os.path.exists(local_file):
            dowloader.download(remote_file, local_file)

        success = int(os.popen(f"""grep -o 'status="success"' {local_file} | wc -l""").readline())
        fails = int(os.popen(f"""grep -o 'status="failure"' {local_file} | wc -l""").readline())
        
        if fails > 0:
            status=2
        elif fails == 0:
            status=0
        else:
            status=1
        total_falied = str(fails) +'/' + str(fails+success)

        self.serializedData.append({
            'test_time': test_time,
            'server_build_time': server_build_time,
            'build_number': build_number,
            'version': version,
            'ssl_version': ssl_version,
            'total_falied': total_falied,
            'status': status})


class ApiJavaParser(reportParser):

    def parseData(self, remote_dir, file_type) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        dowloader = SFTPDownloader(self.host, self.port, self.user, self.passwd)
        FilePath = dowloader.search_file(remote_dir, file_type)

        local_dir = f"{REPORT_SRC}/java/"
        if not os.path.exists(local_dir+'css/'):
            dowloader.download_dir('/hdd/hdd5/hzy/test_report/api/java/release130/css/', local_dir+'css/')

        if not os.path.exists(local_dir+'images/'):
            dowloader.download_dir('/hdd/hdd5/hzy/test_report/api/java/release130/images/', local_dir+'images/')

        tasks = [loop.create_task(self.parse(path, dowloader)) for path in FilePath]

        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
        dowloader.close()

    async def parse(self, path, dowloader):
        version = path.split('/')[0]

        build_number = re.findall("test_result_(.*?).html",path)[0]

        remote_dir = "/hdd/hdd5/hzy/test_report/api/java/"+version+"/"
        local_dir = f"{REPORT_SRC}/java/"
        local_file = local_dir +"test_result_"+build_number+".html"

        if not os.path.exists(local_file):
            dowloader.download(remote_dir+"test_result_"+build_number+".html", local_file)
            merge_css_and_img_to_html(local_file, local_file)

        test_time = ''
        server_build_time = ''
        total_falied = ''
        fails = 0

        async with aiofiles.open(local_file,'r') as f:
            f_info = await f.readlines()

            for i in range(len(f_info)):
                if 'Last Published:' in f_info[i]:
                    test_time = re.findall("""Last Published: (.*?)""",f_info[i])[0]

                elif '<td align="left">' in f_info[i]:
                    total = f_info[i+1].replace(' ','')
                    errors = f_info[i+4].replace(' ','')
                    fails = f_info[i+7].replace(' ','')
                    skips = f_info[i+10].replace(' ','')
                    break
                
            cur_time = datetime.datetime.now()
            # 只获取最近一个月的测试报告
            if(test_time != '' and cur_time > datetime.datetime.strptime(test_time[:10],"%Y-%m-%d") + datetime.timedelta(days=30)):
                return

            try:
                error_int = int(errors) if errors != '' else 0
                if error_int == 0:
                    fail_int = int(fails)
                    if fail_int > 0:
                        status=2
                    elif fail_int == 0:
                        status=0
                else:
                    status=1
            except Exception:
                status = 1
            
            total_falied = fails +'/' + total

            self.serializedData.append({
                'test_time': test_time,
                'server_build_time': server_build_time,
                'build_number': build_number,
                'version': version,
                'total_falied': total_falied,
                'status': status})


if __name__ == "__main__":
    s=PluginParser('192.168.100.27',22,'yzou','DolphinDB123')
    s.parseData("/hdd/hdd5/hzy/test_report/plugin/","txt")
