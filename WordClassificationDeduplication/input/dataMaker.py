import pyhs2
from input.infoLoader import get_account
import traceback


class DataMaker():
    def __init__(self, sql):
        self._result = None
        info = get_account()
        if not info:
            raise ValueError("keep hive info first")
        try:
            conn = pyhs2.connect(host="bj01-tst-hadoop06.vivo.lan",
                                 port=10000,
                                 authMechanism="PLAIN",
                                 user=info.get("config").get("user"),
                                 password=info.get("config").get("password"),
                                 database="default",
                                 )
            cursor = conn.cursor()
            cursor.execute(sql)
            self._result = cursor.fetchall()
        except Exception as e:
            traceback.print_exc()
        finally:
            cursor.close()

    @property
    def result(self):
        return self._result

    @result.setter
    def set_result(self, val):
        self._result = val


if __name__ == '__main__':
    print(get_account())
