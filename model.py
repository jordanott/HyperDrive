from keras.models import load_model

class Model:
    def __init__(self, args, file_name=None):
        self.args = args

        if file_name is not None:
            self._load_model(file_name)
        else:
            self._build_model()

    def _build_model(self):
        pass

    def _load_model(self, file_name):
        self.model = load_model(file_name)

    def save_model(self, file_name):
        self.model.save(file_name)
