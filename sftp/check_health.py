from .worker import SFTP


def _check_health(config: dict) -> bool:
    try:
        obj = SFTP(config)
        obj.check()
        return True
    except Exception as e:
        raise Exception(e)