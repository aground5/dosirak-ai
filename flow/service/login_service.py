import logging as l

from yarl import URL

from ..http import async_ajax_impl, async_ajax
from ..vo import FlowUser


async def login(id, pw) -> FlowUser:
    new_user = FlowUser(id, pw)

    await async_ajax.execute_page(new_user, "signin")
    new_user.get_session().cookie_jar.update_cookies({
        "ps_mode": "trackingV1",
        "LAST_SUB_PATH": "",
        "PS_CUSTOMER_KEY": "",
        "electronYn": "N",
        "FLOW_LANG": "ko",
        "FLOW_DUID": "",
        "googleLoginYn": ""
    }, URL("https://flow.team/"))

    data = await async_ajax_impl.login(new_user)
    new_user.get_session().cookie_jar.update_cookies({
        "FLOW_DUID": "914719-795-117-557935",
        "googleLoginYn": "N"
    }, URL("https://flow.team/"))

    rand_key = await async_ajax_impl.auto_login(new_user)
    await async_ajax.execute_page(new_user, "main", data={
        "INVT_KEY": "",
        "T_COLABO_SRNO": "",
        "T_COLABO_COMMT_SRNO": "",
        "T_COLABO_REMARK_SRNO": "",
        "SUB_DOM": "",
        "DESKTOP_GUIDE_YN": "",
        "FIRST_LOGIN_YN": "N",
    })
    l.debug("로그인 성공: id={}, data={}".format(id, data))
    new_user.set_data(data)
    new_user.get_session().cookie_jar.update_cookies({
        "MINI_USER_ID": new_user.user_id,
        "flowLogin": "",
        "isAutoLoginBlock": "Y",
        "useIndexDBYn": "Y"
    }, URL("https://flow.team/"))
    return new_user


async def socket_io_login(user: FlowUser):
    chat_data = await async_ajax_impl.get_chat_list(user)
    unread_alarm_data = await async_ajax_impl.get_alarm_list(user, mode="UNREAD")
    all_proj_data = await async_ajax_impl.get_project_list(user, mode="ALL")
    count_alarm_data = await async_ajax_impl.get_alarm_list(user, mode="COUNT")
    join_req_data = await async_ajax_impl.flow_join_req(user)
    recent_proj_data = await async_ajax_impl.get_project_list(user, mode="RECENT")
    icon_data = await async_ajax_impl.icon_info(user)
    pw_expire_data = await async_ajax_impl.get_expire_pw_date(user)
    notice_deploy_data = await async_ajax_impl.notice_find_deploy(user)
    set_language_data = await async_ajax_impl.set_language(user)
    tooltip_data = await async_ajax_impl.get_tooltip(user)
    set_timezone_data = await async_ajax_impl.set_language(user)
    banner_data = await async_ajax_impl.open_banner(user)
    # l.debug(f"{[chat_data, unread_alarm_data, all_proj_data, count_alarm_data, join_req_data, recent_proj_data, icon_data, pw_expire_data, notice_deploy_data, set_language_data, tooltip_data, set_timezone_data, banner_data]}")
