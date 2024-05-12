import logging

import aiohttp

cookies = {
    'NNB': 'D72N2X2RS7AGK',
    'page_uid': 'iNuUTdqVOswss4lTRllssssstHs-360552',
}

headers = {
    'authority': 'search.naver.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ko',
    'cache-control': 'no-cache',
    # 'cookie': 'NNB=D72N2X2RS7AGK; page_uid=iNuUTdqVOswss4lTRllssssstHs-360552',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': 'https://www.naver.com/',
    'sec-ch-ua': '"Chromium";v="121", "Not A(Brand";v="99"',
    'sec-ch-ua-arch': '"arm"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version-list': '"Chromium";v="121.0.6167.139", "Not A(Brand";v="99.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"macOS"',
    'sec-ch-ua-platform-version': '"14.2.1"',
    'sec-ch-ua-wow64': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
}

params = {
    'where': 'nexearch',
    'sm': 'top_sug.pre',
    'fbm': '0',
    'acr': '1',
    'acq': '맞춤',
    'qdt': '0',
    'ie': 'utf8',
    'query': '맞춤법검사기',
}

async def get_passport_key() :
    session = aiohttp.ClientSession()
    async with session.get('https://search.naver.com/search.naver', params=params, cookies=cookies, headers=headers) as response:
        response_text = await response.text()
        left = response_text.find("passportKey=") + len("passportKey=")
        right = response_text.find("\"", left)
        passport_key = response_text[left: right]
        logging.debug("get passport: left={} right={} passport_key={}".format(left, right, passport_key))
        await session.close()
        return passport_key

if __name__ == "__main__" :
    logging.basicConfig(level=logging.DEBUG)
    import asyncio
    asyncio.run(get_passport_key())