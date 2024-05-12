import asyncio
import logging

from hanspell import spell_checker
from mecab import MeCab
from pykospacing import Spacing

from naver.http.passport_key import get_passport_key

spacing = Spacing()


def auto_space(text):
    return spacing(text)


async def auto_spell(text):
    passport_key = await get_passport_key()
    result = spell_checker.check(text, passport_key)
    logging.debug("네이버 맞춤법 검사기 결과: {}".format(result))
    print(result)
    mecab_morph(result.checked)
    return result.checked

def mecab_morph(text):
    mecab = MeCab()
    result = mecab.morphs(text)
    print(result)
    return result



if __name__ == "__main__":
    text = "신지인 차장 화~목 취소요청드립니다. 감사합니다!"
    mecab_morph(text)
    asyncio.run(auto_spell(text))
