import logging
import re

def parse_order_info_from_html(order_html: str) -> list:
    logging.debug("order_html={}".format(order_html))
    heat = re.search("발열 도시락\([\d]*명\)", order_html)
    warm = re.search("보온 도시락\([\d]*명\)", order_html)
    salad = re.search("오늘의 샐러드\([\d]*명\)", order_html)
    if heat is None or warm is None or salad is None:
        logging.critical(f"파싱을 진행할 수 없음! order_html={order_html}")
    ordered_text = [
        order_html[heat.span()[1]:warm.span()[0]], order_html[warm.span()[1]:salad.span()[0]], order_html[salad.span()[1]:]
    ]
    orders = []
    pattern = "<[a-zA-Z/\&\;]*>"
    for text in ordered_text :
        split_text = re.split(pattern, text)
        orders.append([i.strip().split(' ') for i in split_text if is_hangul(i)])
    for order in orders:
        for o in order:
            if len(o) == 2:
                o.append(1)
            else:
                o[2] = int(o[2][:len(o[2]) - 1])
    return orders

def parse_regular_order_info_from_html(order_html: str) -> list:
    logging.debug("order_html={}".format(order_html))
    heat = order_html.find("발열 도시락")
    warm = order_html.find("보온 도시락", heat)
    salad = order_html.find("오늘의 샐러드", warm)
    ordered_text = [
        order_html[heat + 6:warm], order_html[warm + 6:salad], order_html[salad + 7:]
    ]
    order = []
    pattern = "<[a-zA-Z/\&\;]*>"
    for text in ordered_text :
        split_text = re.split(pattern, text)
        each_order = [i.strip().split(' ') for i in split_text if is_hangul(i)]
        each_order = [[i[0], i[1][:i[1].find('(')], i[1][i[1].find('(') + 1:-1]] for i in each_order]
        order.append(each_order)

    return order

def is_hangul(text):
    hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', text))
    return hanCount > 0