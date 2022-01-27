
import os
import sys
import pytest
from os.path import dirname as d
from os.path import abspath

root_dir = d(d(abspath(__file__)))
sys.path.append(root_dir)
sys.path.append('{}/tests/acceptance/'.format(root_dir))

from libs.pages.browser import Browser




import pytest
from libs.pages.browser import Browser


@pytest.fixture(scope='session')
def browser(request):
    browser = Browser()
    driver = browser.launch_chrome()
    def clean():
        driver.quit()
    request.addfinalizer(clean)
    return browser

