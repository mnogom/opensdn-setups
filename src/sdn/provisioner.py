from warnings import warn

from rich.progress import track

from src.sdn.constants import ORDER_TO_PROVISION
from src.sdn.repo import SdnReourcesRepo
from src.sdn.vnc_api_gen import WrappedVncApi


class SdnProvisioner:
    def __init__(self, conf_file: str):
        self._vnc = WrappedVncApi(conf_file=conf_file)

    def provision(self, repo: SdnReourcesRepo, raise_error: bool = True):
        repo._list.sort(
            key=lambda res: ORDER_TO_PROVISION.index(res._type),
            reverse=False,
        )

        for res in track(repo._list, description="SDN Creating"):
            try:
                self._vnc.create(res)
            except Exception as error:
                if raise_error:
                    raise
                warn(error)

    def find(self, repo: SdnReourcesRepo):
        for res in repo._list:
            res.uuid = self._vnc.fq_name_to_id(res._type, res.fq_name)

    def erase(self, repo: SdnReourcesRepo, raise_error: bool = True):
        self.find(repo=repo)
        repo._list.sort(
            key=lambda res: ORDER_TO_PROVISION.index(res._type),
            reverse=True,
        )
        for res in track(repo._list, description="SDN Deleting"):
            try:
                self._vnc.delete(res)
            except Exception as error:
                message = f"{res._type} : {res} : {error}"
                if raise_error:
                    raise Exception(message)
                warn(message)
