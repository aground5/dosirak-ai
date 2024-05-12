import asyncio
import logging

from llmprocess.parser import count_people_parse
from ..http import async_ajax_impl
from ..service import dosirak_service, llm_service
from ..tools import regular_order_post_template, order_post_template, format_date
from ..vo import FlowUser

korean_weekday = ['월', '화', '수', '목', '금', '토', '일']
work_positions = ['본부장', '사원', '대리', '과장', '차장', '부장', '이사', '상무', '소장']


async def regular_order_post_repost(user: FlowUser, month: int):
    regular_order_post = await dosirak_service.get_regular_order_post_by_month(user, 3)
    regular_order_info = \
        await dosirak_service.get_regular_order_info_by_post_no(user, regular_order_post["COLABO_COMMT_SRNO"])

    regular_order_strings = [[f"{person[0]} {person[1]}({person[2]})" for person in each_order]
                             for each_order in regular_order_info]
    regular_html = regular_order_post_template.get_html_template(regular_order_strings)
    regular_cntn = regular_order_post_template.get_cntn_template(regular_order_strings)
    logging.debug(f"regular_order_post_repost: 기존 post에서 파싱됨={regular_order_strings}")

    result = await async_ajax_impl.change_post_content(user,
                                                       post_no=regular_order_post["COLABO_COMMT_SRNO"],
                                                       title=regular_order_post["COMMT_TTL"],
                                                       html_cntn=regular_html,
                                                       cntn=regular_cntn)
    logging.debug(f"regular_order_post_repost: 결과={result}")


def task_check_next_order_post_exist(user: FlowUser, search_date):
    asyncio.create_task(check_next_order_post_exist(user, search_date))


async def check_next_order_post_exist(user: FlowUser, search_date):
    post = await dosirak_service.get_post_by_order_date(user, search_date)
    if post is None:
        regular_order_post = await dosirak_service.get_regular_order_post_by_month(user, search_date.month)
        regular_order_info = \
            await dosirak_service.get_regular_order_info_by_post_no(user, regular_order_post["COLABO_COMMT_SRNO"])
        regular_order_info = [[person for person in each_order
                               if person[2].find(korean_weekday[search_date.weekday()]) != -1]
                              for each_order in regular_order_info]
        logging.debug(f"check_next_order_post_exist: 현재 요일에 정기 신청한 사람={regular_order_info}")

        order_strings = [[f"{person[0]} {person[1]}" for person in each_order]
                         for each_order in regular_order_info]
        order_title = f"{format_date(search_date)} 도시락 주문"
        order_html = order_post_template.get_html_template(order_strings)
        order_cntn = order_post_template.get_cntn_template(order_strings)

        result = await async_ajax_impl.create_post_content(user,
                                                           title=order_title,
                                                           html_cntn=order_html,
                                                           cntn=order_cntn)
        logging.debug(f"check_next_order_post_exist: 게시물 생성 결과={result}")
    else:
        order_info = await dosirak_service.get_order_info_by_post_no(user, post["COLABO_COMMT_SRNO"])
        logging.debug(f"check_next_order_post_exist: 게시물 찾음={order_info}")
        task_check_post_comment(user, post)


def task_check_post_comment(user: FlowUser, post):
    asyncio.create_task(check_post_comment(user, post))


async def check_post_comment(user: FlowUser, post):
    comments = await async_ajax_impl.get_post_comment(user, post_no=post["COLABO_COMMT_SRNO"])
    unread_comments = [comment for comment in comments if comment["EMT_SELF_YN"] == "N"]
    logging.debug(f"check_post_comment: 읽지 않은 댓글={unread_comments}")

    if len(unread_comments) > 0:
        employee_list = await dosirak_service.get_employee_list(user)
        known_people_list = [employee["FLNM"] for employee in employee_list]
    else:
        return

    for c in unread_comments:
        operation, people, order = await comment_process(c, known_people_list)
        people = [employee_list[known_people_list.index(person)] for person in people]
        logging.debug(f"다음 파싱된 댓글 정보를 바탕으로 주문을 진행합니다. operation={operation} people={people} order={order}")
        print(operation, people, order)
        if operation == 'create':
            result = await dosirak_service.create_dosirak_order(user, post, people, order)
            await async_ajax_impl.mark_emoji_comment(user, post_no=post["COLABO_COMMT_SRNO"],
                                                     comment_no=c["COLABO_REMARK_SRNO"])
        elif operation == 'cancel':
            result = await dosirak_service.delete_dosirak_order(user, post, people, order)
            await async_ajax_impl.mark_emoji_comment(user, post_no=post["COLABO_COMMT_SRNO"],
                                                     comment_no=c["COLABO_REMARK_SRNO"])
        elif operation == 'change':
            result = await dosirak_service.change_dosirak_order(user, post, people, order)
            await async_ajax_impl.mark_emoji_comment(user, post_no=post["COLABO_COMMT_SRNO"],
                                                     comment_no=c["COLABO_REMARK_SRNO"])


async def comment_process(c, known_people_list, attempt=1) -> (str, [str], [(str, int)]):
    if attempt > 5:
        logging.error(f"댓글 파싱 완전 실패. 로그 확인 후 로직 수정 바랍니다. 댓글={c}")
        return
    from llmprocess.operation_parse_tool import chain as operation_parse_chain
    from llmprocess.count_people_tool import chain as count_people_chain
    content = c["CNTN"]
    parsed_operation = await operation_parse_chain.ainvoke({"input": content})
    logging.debug(f"operation_parse_chain: content={c['CNTN']} parsed_content={parsed_operation}")
    parse_people = await count_people_chain.ainvoke({"people_list": known_people_list, "input": content})
    order_people = count_people_parse(parse_people, known_people_list)
    if len(order_people) == 0 and parse_people['qa_list'][0][1].find('No.') != -1:
        order_people = [c['RGSR_NM']]
    elif len(order_people) == 0:
        logging.warning(f"comment_process: attempt={attempt} failure while people_count_parse.")
        return await comment_process(c, known_people_list, attempt=attempt + 1)
    logging.debug(f"count_people_chain: content={c['CNTN']} parse_people={parse_people} order_people={order_people}")
    # logging.debug(f"operation_parse: {parsed_content['final_answer']} -> {c['CNTN']}")
    redacted_content = content
    for person in order_people:
        redacted_content = redacted_content.replace(person, '')
    for position in work_positions:
        redacted_content = redacted_content.replace(position, '')
    redacted_content = redacted_content.strip()
    if parsed_operation['final_answer'] == 'create':
        parsed_order = await llm_service.create_order_parse(redacted_content)
    elif parsed_operation['final_answer'] == 'cancel':
        parsed_order = await llm_service.delete_order_parse(redacted_content)
    elif parsed_operation['final_answer'] == 'change':
        parsed_order = await llm_service.change_order_parse(redacted_content)
    else:
        logging.warning(f"comment_process: attempt={attempt} failure while operation_parse.")
        return await comment_process(c, known_people_list, attempt=attempt + 1)
    logging.debug(f"parse_order_chain: content={redacted_content} parsed_order={parsed_order}")
    return parsed_operation['final_answer'], order_people, parsed_order['final_answer']


def get_all_dates_of_month(year, month):
    import calendar
    from datetime import date
    num_days = calendar.monthrange(year, month)[1]
    return [date(year, month, day) for day in range(1, num_days + 1)]


async def export_month_order(user: FlowUser, month: int):
    from datetime import date
    year = date.today().year
    all_dates = get_all_dates_of_month(year, month)
    coroutines = [dosirak_service.get_post_by_order_date(user, date, full_search=True, max_page=5) for date in all_dates]
    results = await asyncio.gather(*coroutines)
    posts = [result for result in results if result is not None]
    orders = await asyncio.gather(*[dosirak_service.get_order_info_by_post_no(user, post["COLABO_COMMT_SRNO"]) for post in posts])
    exports = []
    for i in range(len(orders)):
        exports.append({"post": posts[i], "order": orders[i]})
    return exports



