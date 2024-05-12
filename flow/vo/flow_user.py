import logging

import aiohttp

from ..tools import encrypt_password


async def on_request_end(session, trace_config_ctx, params):
    logging.debug('Request for %s. Sent headers: %s' % (params.url, params.response.request_info.headers))


headers = {
    'Host': 'flow.team',
    # 'Content-Length': '397',
    'Sec-Ch-Ua': '"Chromium";v="121", "Not A(Brand";v="99"',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.160 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Origin': 'https://flow.team',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://flow.team/main.act?detail',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Priority': 'u=1, i',
}


class FlowUser:
    user_id = ""
    _plain_pw = ""
    rgsn_dttm = ""
    duid = "914719-795-117-557935"
    duid_nm = "PC-CHROME_914719-795-117-557935"
    _session = None
    _data = None

    def __init__(self, user_id, plain_pw):
        self.user_id = user_id
        self._plain_pw = plain_pw
        self.init_session()

    def __str__(self):
        return "user_id={} rgsn_dttm={} duid={} duid_nm={} update_dt={}".format(self.user_id, self.rgsn_dttm, self.duid,
                                                                                self.duid_nm, self.update_dt)

    def init_session(self, session=None):
        if session is None:
            conn = aiohttp.TCPConnector()
            trace_config = aiohttp.TraceConfig()
            trace_config.on_request_end.append(on_request_end)
            self._session = aiohttp.ClientSession(connector=conn, headers=headers, trace_configs=[trace_config])
        else:
            self._session = session

    def get_session(self):
        return self._session

    def get_password(self, cur_time):
        return encrypt_password(self._plain_pw, cur_time)

    def set_data(self, data):
        self._data = data

    def set_plain_pw(self, pw):
        self._plain_pw = pw

    def get_name(self):
        return self._data["USER_NM"]

    def get_email(self):
        return self._data["EML"]