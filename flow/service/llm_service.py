import logging
import re

from llmprocess import create_order_chain, change_order_chain, delete_order_chain


async def create_order_parse(redacted_content):
    parsed_order = await create_order_chain.ainvoke({"input": redacted_content})
    orders = re.findall('\([보온발열도시락오늘의샐러드]*, [0-9]*\)', parsed_order['final_answer'])
    orders = [order[1:len(order) - 1].split(', ') for order in orders]
    if len(orders) <= 0:
        logging.warning(f"create_order_parse: 파싱 실패 - 도시락 주문이 존재하지 않음.")
        return False
    for order in orders:
        order[0] = sanitize_dosirak_type(order[0])
        order[1] = int(order[1])
        if not order[0]:
            logging.warning(f"create_order_parse: 파싱 실패 - 도시락 종류 구분 실패")
            return False
    parsed_order['final_answer'] = orders
    return parsed_order


async def change_order_parse(redacted_content):
    parsed_order = await change_order_chain.ainvoke({"input": redacted_content})
    order = [o.strip() for o in parsed_order["final_answer"].split('to')]
    if len(order) != 2:
        logging.warning(f"change_order_parse: 파싱 실패 - 예상과 다른 출력값={parsed_order['final_answer']}")
        return False
    if order[0] == "Nothing":
        order[0] = ["발열", "보온", "샐러드"]
    else:
        order[0] = [sanitize_dosirak_type(order[0])]
        if not order[0]:
            logging.warning(f"change_order_parse: 파싱 실패 - 도시락 종류 구분 실패")
            return False
    order[1] = re.findall('\([보온발열도시락오늘의샐러드]*, [0-9]*\)', order[1])
    order[1] = [order[1:len(order) - 1].split(', ') for order in order[1]]
    if len(order[1]) <= 0:
        logging.warning(f"change_order_parse: 파싱 실패 - 도시락 주문이 존재하지 않음.")
        return False
    for o in order[1]:
        o[0] = sanitize_dosirak_type(o[0])
        o[1] = int(o[1])
        if not o[0]:
            logging.warning(f"create_order_parse: 파싱 실패 - 도시락 종류 구분 실패")
            return False
    parsed_order['final_answer'] = order
    return parsed_order


async def delete_order_parse(redacted_content):
    parsed_order = await delete_order_chain.ainvoke({"input": redacted_content})
    orders = parsed_order['final_answer'].split(', ')
    if 'entire order' in orders:
        orders = ['발열', '보온', '샐러드']
    else:
        for i in range(len(orders)):
            orders[i] = sanitize_dosirak_type(orders[i])
            if not orders[i]:
                logging.warning(f"delete_order_parse: 파싱 실패 - 도시락 종류 구분 실패")
                return False
    parsed_order['final_answer'] = orders
    return parsed_order


def sanitize_dosirak_type(raw_type):
    if raw_type in ['발열', '발열도시락', '발열 도시락']:
        return '발열'
    if raw_type in ['보온', '보온도시락', '보온 도시락']:
        return '보온'
    if raw_type in ['샐러드', '오늘의샐러드', '오늘의 샐러드']:
        return '샐러드'
    return False
