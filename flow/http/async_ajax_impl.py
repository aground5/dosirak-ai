import datetime
import logging

from yarl import URL

from constants import DOSIRAK_COLABO_SRNO
from .async_ajax import execute_api
from ..vo import FlowUser


async def login(user: FlowUser):
    cur_time = await current_time(user)
    pwd = user.get_password(cur_time).decode() + '\n'
    data, code = await execute_api(user, "LOGIN", {
        'DUID': user.duid,
        'DUID_NM': user.duid_nm,
        'PWD': pwd,
        'ID_GB': 1,
        'ENCRYPT_YN': 'YC',
        'OBJ_CNTS_NM': '',
        'SUB_DOM': '',
        'CMPN_CD': '',
        'packetOption': 1,
        'CP_CODE': ''
    })
    if code == 200:
        user.get_session().cookie_jar.update_cookies({"DATE_TIME": ""})
        user.rgsn_dttm = data["RGSN_DTTM"]
        return data
    else:
        logging.debug("login failure with code {}", code)
        exit(-1)


async def current_time(user: FlowUser):
    data, code = await execute_api(user, "CUR_TIME", {})
    if code == 200:
        user.get_session().cookie_jar.update_cookies({"DATE_TIME": data["CUR_DTTM"]}, URL("https://flow.team/"))
        return data["CUR_DTTM"]
    else:
        logging.debug("current_time failure with code {}", code)
        exit(-1)


async def auto_login(user: FlowUser):
    temp_user = FlowUser(user.user_id, "")
    temp_user.init_session(user.get_session())
    data, code = await execute_api(temp_user, "AUTO_LOGIN", {})
    if code == 200:
        return data["RAND_KEY"]
    else:
        logging.debug("auto_login failure with code {}", code)
        exit(-1)


async def logout(user: FlowUser):
    data, code = await execute_api(user, "LOGOUT", {})
    if code == 200:
        return not data["COMMON_HEAD"]["ERROR"]
    else:
        logging.debug("logout failure with code {}", code)
        exit(-1)


async def flow_join_req(user: FlowUser):
    data, code = await execute_api(user, "FLOW_JOIN_REQ", {})
    if code == 200:
        return not data["COMMON_HEAD"]["ERROR"]
    else:
        logging.debug("flow_join_req failure with code {}", code)
        exit(-1)


async def icon_info(user: FlowUser):
    data, code = await execute_api(user, "ICON_INFO", {})
    if code == 200:
        return data["COLABO_FLD_REC"]
    else:
        logging.debug("icon_info failure with code {}", code)
        exit(-1)


async def get_expire_pw_date(user: FlowUser):
    data, code = await execute_api(user, "EXPIRE_PW", {})
    if code == 200:
        return data["PWD_CHG_YN"], data["REASON"]
    else:
        logging.debug("get_expire_pw_date failure with code {}", code)
        exit(-1)


async def notice_find_deploy(user: FlowUser):
    data, code = await execute_api(user, "NOTICE_FIND_DEPLOY", {
        "FILTER_A": "WEB",
        "NOW_DATE": datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    })
    if code == 200:
        return data["NOTICE_DETAIL_REC"]
    else:
        logging.debug("get_expire_pw_date failure with code {}", code)
        exit(-1)


async def set_language(user: FlowUser):
    data, code = await execute_api(user, "LANGUAGE", {
        "LANG_CODE": "ko",
        "TYPE": "BULK"
    })
    if code == 200:
        return not data["COMMON_HEAD"]["ERROR"]
    else:
        logging.debug("set_language failure with code {}", code)
        exit(-1)


async def set_timezone(user: FlowUser):
    data, code = await execute_api(user, "TIMEZONE", {
        "TIMEZONE": "Asia/Seoul"
    })
    if code == 200:
        return not data["COMMON_HEAD"]["ERROR"]
    else:
        logging.debug("set_timezone failure with code {}", code)
        exit(-1)


async def open_banner(user: FlowUser):
    data, code = await execute_api(user, "BANNER", {
        "CHANNEL": "ALL-TEXT"
    })
    if code == 200:
        return data["BANNER_DETAIL_REC"]
    else:
        logging.debug("open_banner failure with code {}", code)
        exit(-1)


async def get_tooltip(user: FlowUser):
    data, code = await execute_api(user, "TOOLTIP", {
        "TOOLTIP_ID": "QUICK_GUIDE",
        "SHOW_YN": "N",
        "QUICKGUIDE_YN": "Y"
    })
    if code == 200:
        return data["VIEW_YN"]
    else:
        logging.debug("get_tooltip failure with code {}", code)
        exit(-1)


async def get_chat_list(user: FlowUser, page=1, page_offset=0):
    data, code = await execute_api(user, "CHATTING", {
        "PG_NO": page,
        "PG_PER_CNT": 20,
        "NEXT_YN": "Y",
        "PG_OFFSET": page_offset,
        "SRCH_WORD": "",
        "packetOption": 1
    })
    if code == 200:
        return data["LIST_REC"]
    else:
        logging.debug("get_chat_list failure with code {}", code)
        exit(-1)


async def get_alarm_list(user: FlowUser, page=1, mode="UNREAD"):
    data, code = await execute_api(user, "ALARM", {
        "PG_NO": page,
        "PG_PER_CNT": 50,
        "NEXT_YN": "Y",
        "SRCH_WORD": "",
        "GUBUN": "0,1,2,",
        "MODE": mode
    })
    if code == 200:
        return data["ALARM_COUNT"], data["ALARM_REC"]
    else:
        logging.debug("get_alarm_list failure with code {}", code)
        exit(-1)


async def get_project_list(user: FlowUser, page=1, mode="ALL"):
    data, code = await execute_api(user, "FETCH_PROJECT_LIST", {
        "PG_NO": page,
        "PG_PER_CNT": 50,
        "NEXT_YN": "Y",
        "COLABO_FLD_KIND": "1",
        "COLABO_FLD_SRNO": "9" if mode == "ALL" else "11",
        "MODE": mode,
        "MNGR_YN": "N",
        "SORT_DESC": "",
        "packetOption": 2
    })
    if code == 200:
        return data["PROJECT_RECORD"]
    else:
        logging.debug("get_proect_list failure with code {}", code)
        exit(-1)


async def get_post_list(user: FlowUser, project_no=DOSIRAK_COLABO_SRNO, page=1):
    data, code = await execute_api(user, "FETCH_POST_LIST", {
        "PG_NO": page,
        "PG_PER_CNT": 20,
        "PREV_YN": "Y",
        "NEXT_YN": "Y",
        "COLABO_SRNO": project_no,
        "RENEWAL_YN": "Y",
        "MORE_BUTTON": False,
        "SEARCH_COMMT_SRNO": "",
        "SRCH_COLABO_REMARK_SRNO": "",
        "ORDER_TYPE": "N",
        "GUBUN": "DETAIL",
        "TAG_NM": "",
        "TMPL_TYPE": ""
    })
    if code == 200:
        return data["POST_RECORD"], data["NEXT_YN"] == "Y"
    else:
        logging.debug("get_post_list failure with code {}", code)
        exit(-1)


async def get_post(user: FlowUser, project_no=DOSIRAK_COLABO_SRNO, post_no="41093897"):
    data, code = await execute_api(user, "FETCH_FEED", {
        "GUBUN": "DETAIL",
        "COLABO_SRNO": project_no,
        "COLABO_COMMT_SRNO": post_no,
        "COLABO_REMARK_SRNO": "-1",
        "RENEWAL_YN": "Y",
        "PG_NO": 1,
        "PG_PER_CNT": 1,
        "COPY_YN": "N"
    })
    if code == 200:
        return data["COMMT_REC"]
    else:
        logging.debug("get_post failure with code {}", code)
        exit(-1)


async def get_post_comment(user: FlowUser, project_no=DOSIRAK_COLABO_SRNO, post_no="41093897"):
    data, code = await execute_api(user, "FETCH_COMMENT", {
        "MODE": "M",
        "ORDER_TYPE": "P",
        "COLABO_SRNO": project_no,
        "COLABO_COMMT_SRNO": post_no,
        "SRCH_COLABO_REMARK_SRNO": "",
        "REPEAT_DTTM": "",
        "packetOption": 1
    })
    if code == 200:
        return data["COLABO_REMARK_REC"]
    else:
        logging.debug("get_post_comment failure with code {}", code)
        exit(-1)


async def get_all_employee_list(user: FlowUser):
    data = None
    employee_list = []
    page = 1
    while data is None or data['NEXT_YN'] == "Y":
        data, code = await execute_api(user, "EMPLOYEE_LIST", {
            "PG_NO": page,
            "PG_PER_CNT": 30,
            "NEXT_YN": "Y",
            "SRCH_WD": "",
            "SRCH_WORD": "",
            "COLABO_SRNO": "",
            "packetOption": 2
        })
        if code == 200:
            page += 1
            employee_list += data["CNPL_LIST"]
        else:
            logging.debug("get_all_employee_list failure with code {}", code)
            exit(-1)

    return employee_list


async def change_post_content(user: FlowUser,
                              project_no=DOSIRAK_COLABO_SRNO,
                              post_no="41093897",
                              title="",
                              cntn="",
                              html_cntn=""):
    data, code = await execute_api(user, "UPDATE_POST", {
        "COLABO_SRNO": project_no,
        "COLABO_COMMT_SRNO": post_no,
        "RANGE_TYPE": "A",
        "SCRN_NO": "1",
        "RGSR_ID": user.user_id,
        "COMMT_TTL": title,
        "CNTN": cntn,
        "HTML_CNTN": html_cntn,
        "EDITOR_YN": "Y",
        "TMPL_TYPE": "91"
    })
    if code == 200:
        return data
    else:
        logging.debug("change_post_content failure with code {}", code)
        exit(-1)


async def create_post_content(user: FlowUser,
                              project_no=DOSIRAK_COLABO_SRNO,
                              title="",
                              cntn="",
                              html_cntn=""):
    data, code = await execute_api(user, "CREATE_POST", {
        "COLABO_SRNO": "",
        "COLABO_COMMT_SRNO": "",
        "RANGE_TYPE": "A",
        "SCRN_NO": "1",
        "RGSR_ID": user.user_id,
        "COMMT_TTL": title,
        "CNTN": cntn,
        "HTML_CNTN": html_cntn,
        "EDITOR_YN": "Y",
        "PRJ_REC": [
            {
                "COLABO_SRNO": project_no,
                "TTL": "점심 도시락",
                "BG_COLOR_CD": "3",
                "CHAT_SRCH_GB": "E",
                "ROOM_KIND": "",
                "TEMP_CHAT_SRNO": "Q0"
            }
        ],
        "packetOption": 1
    })
    if code == 200:
        return data
    else:
        logging.debug("create_post_content failure with code {}", code)
        exit(-1)


async def mark_emoji_comment(user: FlowUser,
                             project_no=DOSIRAK_COLABO_SRNO,
                             post_no="41093897",
                             comment_no="1234"):
    data, code = await execute_api(user, "EMOJI_COMMENT", {
        "COLABO_SRNO": project_no,
        "COLABO_COMMT_SRNO": post_no,
        "COLABO_REMARK_SRNO": comment_no,
        "EMT_CD": 1
    })
    if code == 200:
        return data
    else:
        logging.debug("mark_emoji_comment failure with code {}", code)
        exit(-1)


async def unmark_emoji_comment(user: FlowUser,
                               project_no=DOSIRAK_COLABO_SRNO,
                               post_no="41093897",
                               comment_no="1234"):
    data, code = await execute_api(user, "EMOJI_COMMENT", {
        "COLABO_SRNO": project_no,
        "COLABO_COMMT_SRNO": post_no,
        "COLABO_REMARK_SRNO": comment_no,
        "EMT_CD": 0
    })
    if code == 200:
        return data
    else:
        logging.debug("unmark_emoji_comment failure with code {}", code)
        exit(-1)
