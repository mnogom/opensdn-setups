import requests


def monkey_patch_requests(lvl: int):
    class Session(requests.Session):
        def prepare_request(self, request):
            req = super().prepare_request(request)
            if lvl >= 1:
                print(
                    f"[{request.method} {request.url}]: {request.json or request.data}"
                )
            return req

        def request(self, *args, **kwargs):
            response = super().request(*args, **kwargs)
            if lvl >= 2:
                print(response.json())
            return response

    requests.Session = Session
    requests.sessions.Session = Session
