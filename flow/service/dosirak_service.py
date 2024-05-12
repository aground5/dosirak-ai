import logging
from datetime import date
from urllib.parse import unquote_plus

from ..http import async_ajax_impl
from ..tools import parse_order_info_from_html, parse_regular_order_info_from_html, order_post_template, process_date
from ..vo import FlowUser


async def get_post_by_order_date(user: FlowUser, order_date: date, full_search=False, max_page=20):
    is_next = True
    i = 0
    while is_next:
        i += 1
        post_list, is_next = await async_ajax_impl.get_post_list(user, page=i)
        for post in post_list:
            try:
                post_title = post["COMMT_TTL"]
                post_date = process_date.parse_date_from_title(post_title)
                if post_date == order_date:
                    logging.debug(f"게시물 찾음, order_date={order_date}, post={post}")
                    return post
            except ValueError:
                pass
        if not full_search or i > max_page:
            break

    logging.debug(f"게시물 못 찾음, order_date={order_date}")
    return None


async def get_order_info_by_post_no(user: FlowUser, post_no: str):
    post_data = await async_ajax_impl.get_post(user, post_no=post_no)
    post_data = post_data[0]
    logging.debug(f"게시물 정보, post_no={post_no}, post_data={post_data}")

    order_html = unquote_plus(post_data["HTML_CNTN"])
    return parse_order_info_from_html(order_html)


async def get_regular_order_post_by_month(user: FlowUser, month: int):
    is_next = True
    i = 0
    while is_next:
        i += 1
        post_list, is_next = await async_ajax_impl.get_post_list(user, project_no="1837313", page=i)
        for post in post_list:
            try:
                post_title = post["COMMT_TTL"]
                end = post_title.find("월 도시락 고정 인원")
                if end == -1:
                    pass
                post_month = post_title[:end]
                if post_month == str(month):
                    logging.debug(f"게시물 찾음, month={month}, post={post}")
                    return post
            except ValueError:
                pass


async def get_regular_order_info_by_post_no(user: FlowUser, post_no: str):
    post_data = await async_ajax_impl.get_post(user, project_no="1837313", post_no=post_no)
    post_data = post_data[0]
    logging.debug(f"게시물 정보, post_no={post_no}, post_data={post_data}")

    order_html = unquote_plus(post_data["HTML_CNTN"])
    return parse_regular_order_info_from_html(order_html)


async def get_employee_list(user: FlowUser) -> list:
    employee_list = await async_ajax_impl.get_all_employee_list(user)
    employee_list = [employee for employee in employee_list if employee["FLNM"].find(" ") == -1]
    return employee_list


dosirak_type = ['발열', '보온', '샐러드']


async def create_dosirak_order(user: FlowUser, post, people: [str], orders: [(str, int)]):
    post_no = post["COLABO_COMMT_SRNO"]
    post_title = post["COMMT_TTL"]
    order_info = await get_order_info_by_post_no(user, post_no)
    logging.debug(f"create_dosirak_order: 수정 전 주문 정보={order_info}")
    for person in people:
        for order in orders:
            order_info_index = dosirak_type.index(order[0])
            exist_order = None
            for each_order in order_info[order_info_index]:
                if each_order[0] == person['FLNM'] and each_order[1] == person['JBCL_NM']:
                    exist_order = each_order
                    break
            if exist_order is None:
                order_info[order_info_index].append([person['FLNM'], person['JBCL_NM'], order[1]])
            else:
                exist_order[2] += order[1]
    logging.debug(f"create_dosirak_order: 수정 후 주문 정보={order_info}")
    order_strings = [
        [f"{person[0]} {person[1]}{' ' + str(person[2]) + '개' if person[2] > 1 else ''}" for person in each_order]
        for each_order in order_info]
    order_html = order_post_template.get_html_template(order_strings)
    order_cntn = order_post_template.get_cntn_template(order_strings)
    logging.debug(f"create_dosirak_order: 주문 정보 파싱됨={order_strings}")

    result = await async_ajax_impl.change_post_content(user,
                                                       post_no=post_no,
                                                       title=post_title,
                                                       html_cntn=order_html,
                                                       cntn=order_cntn)
    logging.debug(f"create_dosirak_order: 결과={result}")
    return result


async def delete_dosirak_order(user: FlowUser, post, people: [str], orders: [str]):
    post_no = post["COLABO_COMMT_SRNO"]
    post_title = post["COMMT_TTL"]
    order_info = await get_order_info_by_post_no(user, post_no)
    logging.debug(f"delete_dosirak_order: 수정 전 주문 정보={order_info}")
    for person in people:
        for order in orders:
            order_info_index = dosirak_type.index(order)
            for each_order in order_info[order_info_index]:
                if each_order[0] == person['FLNM'] and each_order[1] == person['JBCL_NM']:
                    order_info[order_info_index].remove(each_order)
                    break
    logging.debug(f"create_dosirak_order: 수정 후 주문 정보={order_info}")
    order_strings = [
        [f"{person[0]} {person[1]}{' ' + str(person[2]) + '개' if person[2] > 1 else ''}" for person in each_order]
        for each_order in order_info]
    order_html = order_post_template.get_html_template(order_strings)
    order_cntn = order_post_template.get_cntn_template(order_strings)
    logging.debug(f"create_dosirak_order: 주문 정보 파싱됨={order_strings}")

    result = await async_ajax_impl.change_post_content(user,
                                                       post_no=post_no,
                                                       title=post_title,
                                                       html_cntn=order_html,
                                                       cntn=order_cntn)
    logging.debug(f"create_dosirak_order: 결과={result}")
    return result


async def change_dosirak_order(user: FlowUser, post, people: [str], orders: [str]):
    delete_order = orders[0]
    create_order = orders[1]
    return [await delete_dosirak_order(user, post, people, delete_order),
            await create_dosirak_order(user, post, people, create_order)]
