import inspect
import winreg
import logging


class RegistryHandler:
    def __init__(self, computer_name: str = None, reg_location: str = 'HKEY_LOCAL_MACHINE',
                 key: str = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'):
        """
        Initiate Registry handler
        :param computer_name: if None takes localhost
        :param reg_location: HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, HKEY_CURRENT_USER, HKEY_USERS, etc.
        :param key: registry path to the sub key
        """
        logging.info(F"called by: {inspect.stack()[1][3]}")
        self.reg_key = winreg.ConnectRegistry(None, getattr(winreg, reg_location))
        self.access_key = winreg.OpenKey(self.reg_key, key)
        self.resp = 'Success'

    def read_key(self, sub_key: str, *args):
        """
        read the value from the DisplayName attribute within the sub_key
        :param sub_key: the final endpoint identification of the key. e.g. 'DE393C6A9AB085F9E19765D003555C3D360497DB'
        :return: Success if succeeded in reading the reg key(sub_key) value, Fail if sub_key not found
        """
        logging.info(F"in {inspect.currentframe().f_code.co_name}: reading from registry, key: {self.reg_key}")
        try:
            open_key = winreg.OpenKey(self.access_key, sub_key)
            winreg.QueryValueEx(open_key, "DisplayName")
        except EnvironmentError:
            self.resp = 'Fail'
        return self.resp

    # marked as internal function to avoid running
    def _update_key(self, sub_key: str, value: str) -> str:
        """
        associates a value with a specified key.
        :param sub_key: the final endpoint identification of the key
        :param value: the value for the sub_key to be updated with.
        :return: Success if succeeded in updating the reg key(sub_key) value, Fail if sub_key not found or update fails
        """
        try:
            open_key = winreg.OpenKey(self.access_key, sub_key)
            # winreg.SetValue('open_key', sub_key, winreg.REG_SZ, value)
        except EnvironmentError:
            self.resp = 'Fail'
        return self.resp

    # marked as internal function to avoid running
    def _delete_key(self, sub_key: str) -> str:
        """
        deletes the specified key.
        :param sub_key: the final endpoint identification of the key
        :return: Success if succeeded in deletion, Fail if sub_key not found or deletion fails
        """
        try:
            open_key = winreg.OpenKey(self.access_key, sub_key)
            # winreg.DeleteKey('open_key', sub_key)
        except EnvironmentError:
            self.resp = 'Fail'
        return self.resp


if __name__ == '__main__':
    reg_acc = RegistryHandler()
    print(reg_acc.read_key(sub_key='DE393C6A9AB085F9E19765D003555C3D360497DB'))

