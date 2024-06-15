from .worker import SFTP

def get_folder(config: dict, params: dict) -> dict:
    wobj = SFTP(config)
    localpath = params.get("localpath")
    remotepath = params.get("remotepath")
    rsp = wobj.runner(localpath=localpath, remotepath=remotepath, recursive=True, op="get")
    return rsp






