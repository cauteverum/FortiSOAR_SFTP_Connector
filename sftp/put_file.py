from .worker import SFTP


def put_file(config: dict, params: dict) -> dict:
    wobj = SFTP(config)
    localpath = params.get("localpath")
    remotepath = params.get("remotepath")
    rsp = wobj.runner(localpath=localpath, remotepath=remotepath, recursive=False, op="put")
    return rsp