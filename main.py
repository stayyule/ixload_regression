import pytest


debug_level = 20
ret = pytest.main(["-o", "log_cli=true",
                   f"--log-cli-level={debug_level}",
                   "-k", "2_arm",
                   ])
