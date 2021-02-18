from dataclasses import is_dataclass

from dj_cleaner.adapters.minio_gateway import MinIOLocation


class TestMinIOLocation:
    def test_if_dataclass(self):
        assert is_dataclass(MinIOLocation)

    def test_if_annotations_are_correct(self):
        assert all(x in MinIOLocation.__annotations__ for x in ("schema_name", "bucket_name", "location"))
