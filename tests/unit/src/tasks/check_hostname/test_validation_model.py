import pytest
from pydantic import ValidationError

from py_tata.tasks.check_hostname import CheckHostnameIn


class TestValidationModel:
    def test_valid_input(self):
        attrs = {"target_hostname": "test-hostname"}

        sut = CheckHostnameIn(**attrs)

        assert sut.target_hostname == "test-hostname"

    def test_error_when_extra_attrs(self):
        attrs = {
            "target_hostname": "test-hostname",
            "extra_var_1": "test-value-1",
        }

        with pytest.raises(ValidationError) as e:
            CheckHostnameIn(**attrs)

        assert e.value.error_count() == 1

        error = e.value.errors()[0]
        assert error["loc"] == ("extra_var_1",)
        assert error["msg"] == "Extra inputs are not permitted"
