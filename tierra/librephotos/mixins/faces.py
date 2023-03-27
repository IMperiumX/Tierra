import numpy as np


class FaceMixin:
    @property
    def timestamp(self):
        return self.photo.exif_timestamp if self.photo else None

    def get_encoding_array(self):
        return np.frombuffer(bytes.fromhex(self.encoding))
