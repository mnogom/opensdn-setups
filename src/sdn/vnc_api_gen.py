from warnings import warn

from vnc_api import vnc_api


class WrappedVncApi(vnc_api.VncApi):
    def create(self, obj):
        try:
            return self._object_create(res_type=obj._type, obj=obj)
        except Exception as error:
            message = f"{obj._type} : {obj} : {error}"
            raise (Exception(message))

    def delete(self, obj):
        try:
            return self._object_delete(res_type=obj._type, fq_name=obj.fq_name)
        except Exception as error:
            message = f"{obj._type} : {obj} : {error}"
            raise Exception(message)
