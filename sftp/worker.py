import paramiko
from connectors.core.connector import get_logger, ConnectorError
from connectors.core.utils import update_connnector_config

logger = get_logger("sftp")


class SFTP:
    def __init__(self,config):
        self.username = config.get("username")
        self.password = config.get("password")
        self.host = config.get("host")
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh_client.connect(hostname=self.host, username=self.username, password=self.password)
            self.sftp_client = self.ssh_client.open_sftp()
        except Exception as err:
            raise err

    def check(self):
        self.sftp_client.close()
        self.ssh_client.close()

    def find_files(self,sftp_client, remotepath):
        files = []
        sftp_client.chdir(remotepath)
        elements = sftp_client.listdir_iter()
        for element in elements:
            element = str(element)
            if not element.startswith("d"):
                files.append(element.split()[-1])
        return files


    def runner(self,localpath="",remotepath="",recursive=False,op=""):
        if not recursive:
            if op=="get":
                remote_file_name = remotepath.split("/")[-1]
                if localpath.endswith("/"):
                    localpath = localpath+remote_file_name
                else:
                    localpath = localpath+"/"+remote_file_name

                self.sftp_client.get(remotepath=remotepath,localpath=localpath)
                self.sftp_client.close()
                self.ssh_client.close()
                return f"{remote_file_name} was downloaded..."

            elif op == "put":
                local_file_name = localpath.split("/")[-1]
                if remotepath.endswith("/"):
                    localpath = remotepath + local_file_name
                else:
                    remotepath = remotepath + "/" + local_file_name
                self.sftp_client.put(remotepath=remotepath, localpath=localpath)
                self.sftp_client.close()
                self.ssh_client.close()
                return f"{local_file_name} was uploaded..."


        if recursive:
            if op == "get":
                files = self.find_files(self.sftp_client,remotepath=remotepath)
                files_downloaded = []
                for f in files:
                    if not remotepath.endswith("/"):
                        remotepath = remotepath + "/"
                    if not localpath.endswith("/"):
                        localpath = localpath + "/"

                    abs_remote_path = remotepath + f
                    abs_local_path = localpath + f
                    self.sftp_client.get(remotepath=abs_remote_path, localpath=abs_local_path)
                    files_downloaded.append(f)
                self.sftp_client.close()
                self.ssh_client.close()
                return f"These files was downloaded ------>>  {'--'.join(files_downloaded)}   <<------"



            elif op == "put":
                pass



