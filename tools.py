import time
from config import USERNAME, PASSWORD


def login(driver):
    """LOGIN:

    set username and password, then click login, then confirm if there are conflicting saves:
    document.getElementById("loginUserName").value = 'alskgj'
    document.getElementById("loginPassword").value = '5sv8dIONs9qP'
    playFabLoginWithPlayFab()
    playFabFinishLogin(true)

    """

    driver.execute_script('cancelTooltip(); toggleSetting("usePlayFab");')
    driver.execute_script('document.getElementById("loginUserName").value = "%s";' % USERNAME)
    driver.execute_script('document.getElementById("loginPassword").value = "%s";' % PASSWORD)
    driver.execute_script('playFabLoginWithPlayFab();')
    time.sleep(2)
    driver.execute_script('playFabFinishLogin(true);')


