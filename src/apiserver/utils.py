

class Utils:

    @staticmethod
    def is_none_or_empty_str(str):

        if str == None or len(str) == 0:
            return True

        return False

    @staticmethod
    def is_int(num):

        if isinstance(num, int):
            return True

        return False