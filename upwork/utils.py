import time
from bs4 import Tag
from typing import List


def smart_split(st: str, delimiter: str = ",") -> List[str]:
    """
    Function that reads a string that will be split by the delimiter, but if not found, returns a valid value.
    Important to prevent the code from breaking each strings format from being different
    :param st:
    :param delimiter:
    :return:
    """
    return [s.strip() for s in st.split(delimiter)] if len(
        st.split(delimiter)) == 2 else st.split(None, 1)


def letters_only(word: str) -> str:
    """
    Filters the string by removing no letters
    :param word:
    :return:
    """
    return ''.join(x for x in word if x.isalpha())


def sleep(sleep_time: int):
    """
    Helper to invoke sleep function
    :type sleep_time: object
    """
    time.sleep(sleep_time)


def get_value(tag: Tag, strip=True, default_value="") -> str:
    """
    Function used in reading the tags, if the selected tag does not exist, it is possible to return a default value.
    That way, we guarantee that all tag calls will have a valid value
    :param tag:
    :param strip:
    :param default_value:
    :return:
    """
    if tag:
        return tag.get_text(strip=strip)
    return default_value
