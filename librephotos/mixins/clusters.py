import numpy as np
from django.contrib.auth import get_user_model


from librephotos.conf import UNKNOWN_CLUSTER_ID, UNKNOWN_CLUSTER_NAME

User = get_user_model()


class ClusterMixin:
    def get_mean_encoding_array(self) -> np.ndarray:
        return np.frombuffer(bytes.fromhex(self.mean_face_encoding))

    def set_metadata(self, all_vectors):
        from librephotos.models import Cluster

        self.mean_face_encoding = (
            Cluster.calculate_mean_face_encoding(all_vectors).tobytes().hex()
        )

    @staticmethod
    def get_or_create_cluster_by_name(user: User, name):
        from librephotos.models import Cluster

        return Cluster.objects.get_or_create(owner=user, name=name)[0]

    @staticmethod
    def get_or_create_cluster_by_id(user: User, cluster_id: int):
        from librephotos.models import Cluster

        return Cluster.objects.get_or_create(owner=user, cluster_id=cluster_id)[0]

    @staticmethod
    def calculate_mean_face_encoding(all_encodings):
        return np.mean(a=all_encodings, axis=0, dtype=np.float64)

    def get_unknown_cluster():
        from librephotos.models import Cluster, Person

        unknown_cluster = Cluster.get_or_create_cluster_by_id(
            User.get_deleted_user(),
            UNKNOWN_CLUSTER_ID,
        )
        unknown_person = Person.get_unknown_person()
        if unknown_cluster.person is not unknown_person:
            unknown_cluster.person = unknown_person
            unknown_cluster.name = UNKNOWN_CLUSTER_NAME
            unknown_cluster.save()
        return unknown_cluster
