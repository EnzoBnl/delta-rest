from overrides import overrides

from flask import Flask, request

from .rest import DeltaRESTAdapter


class DeltaRESTService(Flask):
    def __init__(self,
                 delta_root_path: str,
                 max_response_n_rows: int = 100):
        super().__init__(__name__)
        self.rest_adapter = DeltaRESTAdapter(
            delta_root_path,
            max_response_n_rows
        )

    @overrides
    def run(self, host=None, port=None, debug=None, load_dotenv=True,
            **options):

        @self.route('/', defaults={'path': ''})
        @self.route('/<path:path>', methods=['PUT'])
        def handle_put(path):
            return self.rest_adapter.put(request.full_path.replace("?", ""))

        @self.route('/', defaults={'path': ''})
        @self.route('/<path:path>', methods=['POST'])
        def handle_post(path):
            if request.full_path.endswith("?"):
                uri = request.full_path[:-1]
            else:
                uri = request.full_path
            return self.rest_adapter.post(
                uri,
                # parse as json even if content-type is not json
                request.get_json(force=True, silent=True)
            )

        @self.route('/', defaults={'path': ''})
        @self.route('/<path:path>', methods=['GET'])
        def handle_get(path):
            if request.full_path.endswith("?"):
                uri = request.full_path[:-1]
            else:
                uri = request.full_path
            return self.rest_adapter.get(uri)

        super().run(host, port, debug, load_dotenv, **options)
