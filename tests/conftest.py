import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


# conftest.py
def pytest_addoption(parser):
    parser.addoption(
        "--API_BASE_URL",
        action="store",
        default="default_value",
        help="My custom parameter",
    ),
    parser.addoption(
        "--ENV",
        action="store",
        default="dev",
        help="My custom parameter",
    )


# 使用方法，在測試中取得此參數
@pytest.fixture
def api_base_url(request):
    print(
        f'request.config.getoption("API_BASE_URL"): {request.config.getoption("API_BASE_URL")}'
    )
    return request.config.getoption("API_BASE_URL")

@pytest.fixture
def base_env(request):
    print(
        f'request.config.getoption("ENV"): {request.config.getoption("ENV")}'
    )
    return request.config.getoption("ENV")