from logging import error as log_error, exception as log_exception, info as log_info
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from utils import access_page, assert_button_click, safe_get_element
from wizard import DRIVER

exit_code = 0

try:
    log_info("Navigating to the logs page ...")
    access_page(DRIVER, "/html/body/aside[1]/div[2]/ul[1]/li[11]/a", "logs")

    file_button = safe_get_element(DRIVER, By.CSS_SELECTOR, ".logs-toolbar-files .dropdown-toggle")
    assert isinstance(file_button, WebElement), "Log file button is not a WebElement"
    assert_button_click(DRIVER, file_button)

    file_links = safe_get_element(DRIVER, By.CSS_SELECTOR, "#types-dropdown-menu a", multiple=True)
    assert isinstance(file_links, list), "Log file links are not a list"
    if len(file_links) == 0:
        log_error("No log files found, exiting ...")
        exit(1)
    assert_button_click(DRIVER, file_links[0])
    sleep(1)

    search_button = safe_get_element(DRIVER, By.ID, "logs-search")
    assert isinstance(search_button, WebElement), "Search button is not a WebElement"
    assert_button_click(DRIVER, search_button)

    search_box = safe_get_element(DRIVER, By.CSS_SELECTOR, ".ace_search")
    assert isinstance(search_box, WebElement), "ACE search box is not a WebElement"
    DRIVER.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(1)

    search_z_index, sticky_z_index = DRIVER.execute_script(
        "return [getComputedStyle(arguments[0]).zIndex, " "getComputedStyle(document.querySelector('.sticky-card')).zIndex];",
        search_box,
    )
    if int(search_z_index) <= int(sticky_z_index):
        log_error(f"Search box z-index ({search_z_index}) must be above the sticky toolbar " f"z-index ({sticky_z_index}) after scrolling")
        exit(1)

    log_info("✅ Log search remains above the sticky toolbar after scrolling")
except SystemExit as e:
    exit_code = e.code
except KeyboardInterrupt:
    exit_code = 1
except:
    log_exception("Something went wrong, exiting ...")
    exit_code = 1
finally:
    if exit_code:
        DRIVER.save_screenshot("error.png")
    DRIVER.quit()
    exit(exit_code)
