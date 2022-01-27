import pytest
import time

class TestAddItems:

    @pytest.mark.ui
    def test_add_items(self, browser):
        """
        Scenario :
        """
        current_temperature = browser.browser.find_element_by_xpath("//span[@id='temperature']").text.split()[0]
        if int(current_temperature) < 19:
            browser.browse_items(item_type='Buy moisturizers', first_item='Aloe', second_item='Almond')
        else:
            browser.browse_items(item_type='Buy sunscreens', first_item='SPF-50', second_item='SPF-30')
        browser.proced_checkout()
        time.sleep(10)
        confirmation_message = browser.browser.find_element_by_xpath("//div[@class='row justify-content-center']").text
        assert 'PAYMENT SUCCESS' in confirmation_message, 'Fail to verify success message. ' \
                                                          f'Actual text {confirmation_message} '
