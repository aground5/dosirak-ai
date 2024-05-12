import json
import logging as l
from urllib.parse import quote_plus

from ..vo import FlowUser

api_dict = {
    "LOGIN": "COLABO2_LOGIN_R003",
    "LOGOUT": "COLABO2_LOGOUT_R001",
    "CUR_TIME": "FLOW_CUR_TIME_R001",
    "AUTO_LOGIN": "COLABO2_AUTO_LOGIN_R001",
    "FLOW_JOIN_REQ": "FLOW_JOIN_REQ_R001",
    "ICON_INFO": "COLABO2_FLD_L102",
    "EXPIRE_PW": "ACT_PWD_LIMIT_SELECT",
    "NOTICE_FIND_DEPLOY": "ACT_NOTICE_FIND_DEPLOY",
    "LANGUAGE": "ACT_LANG_U001",
    "TOOLTIP": "COLABO_TOOLTIP_LOG_R001",
    "TIMEZONE": "SET_USER_TIMEZONE",
    "BANNER": "ACT_BANNER_OPEN",
    "CHATTING": "CHATTING",
    "ALARM": "ALARM",
    "FETCH_PROJECT_LIST": "ACT_PROJECT_LIST",
    "FETCH_COMMENT": "COLABO2_REMARK_R101",
    "FETCH_FEED": "COLABO2_R104",
    "FETCH_POST_LIST": "ACT_POST_LIST",
    "EMPLOYEE_LIST": "COLABO2_CHAT_CNPL_R001",
    "UPDATE_POST": "COLABO2_COMMT_U101",
    "CREATE_POST": "COLABO2_COMMT_C101",
    "EMOJI_COMMENT": "COLABO2_REMARK_EMT_U001"
}


async def execute_api(user: FlowUser, api, input_json=None) -> (dict, int):
    if input_json is None:
        input_json = {}

    _user_id = user.user_id
    _rgsn_dttm = user.rgsn_dttm
    input_json.setdefault("USER_ID", _user_id)
    input_json.setdefault("RGSN_DTTM", _rgsn_dttm)

    url = "https://flow.team/" + api_dict[api] + ".jct"
    data = {
        "_JSON_": quote_plus(json.dumps(input_json))
    }
    session = user.get_session()
    l.debug("{}에 대한 요청: {}".format(api_dict[api], input_json))
    # session.cookie_jar.clear(predicate=lambda cookie: cookie.key == "AWSALBTG" or cookie.key == "AWSALBTGCORS")
    # session.cookie_jar.clear_domain("flow.team")
    async with session.post(url, data=data, ssl=False) as response:
        response_text = await response.text()
        l.debug("{}에 대한 응답: {}".format(api_dict[api], response_text))
        response_json = json.loads(response_text)
        response_code = response.status
        if response_json["COMMON_HEAD"]["ERROR"]:
            l.error("{}에서 에러: {}".format(api_dict[api], response_json["COMMON_HEAD"]["MESSAGE"]))
            response_json, response_code = await execute_api(user, api, input_json)
        return response_json, response_code


async def execute_page(user: FlowUser, page, data=None) -> (str, int):
    url = "https://flow.team/" + page + ".act"
    session = user.get_session()
    if data is None:
        l.debug("{}에 대한 요청: {}".format(page, "get 요청"))
        async with session.get(url) as response:
            response_text = await response.text()
            l.debug("{}에 대한 응답: {}".format(page, [response.strip() for response in response_text.split('\n')]))
            response_code = response.status
            return response_text, response_code
    else:
        l.debug("{}에 대한 요청: {}".format(page, "post 요청"))
        async with session.post(url, data=data) as response:
            response_text = await response.text()
            l.debug("{}에 대한 응답: {}".format(page, [response.strip() for response in response_text.split('\n')]))
            response_code = response.status
            return response_text, response_code


