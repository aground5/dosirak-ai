# 문단 사이를 nbsp로 표현하는 듯

preface = ("<p>** 댓글에 이름과 직급을 적어주세요. (홍길동 사원)<br>"
           "** 이번달 발열팩은 모두 서비스로 제공됩니다.<br>"
           "** 도시락 종류 언급 없을 시 보온 도시락으로 신청됩니다.</p>"
           "<p>&nbsp;</p>"
           "<p>발열 도시락(+ 발열팩) : 7,000원<br>"
           "보온 도시락 : 6,500원<br>"
           "오늘의 샐러드 : 6,500원</p>"
           "<p>&nbsp;</p>"),
preface = preface[0]

template = ["<p>총 {}명</p>",
            "<p>발열 도시락({}명)</p>",
            "<p>보온 도시락({}명)</p>",
            "<p>오늘의 샐러드({}명)</p>"]


def get_html_template(strings: list) -> str:
    html = preface
    total_len = len(strings[0]) + len(strings[1]) + len(strings[2])
    html += template[0].format(total_len)
    for i in range(3):
        if i != 0:
            html += "<p>&nbsp;</p>"
        name_list = strings[i]
        html += template[i + 1].format(len(name_list))
        for name in name_list:
            html += "<p>{}</p>".format(name)
    return html


cntn_preface = """** 댓글에 이름과 직급을 적어주세요. (홍길동 사원)\\n
** 이번달 발열팩은 모두 서비스로 제공됩니다.\\n
** 도시락 종류 언급 없을 시 보온 도시락으로 신청됩니다.\\n
\\n
발열 도시락(+ 발열팩) : 7,000원\\n
보온 도시락 : 6,500원\\n
오늘의 샐러드 : 6,500원\\n"""

cntn_preface = cntn_preface[0]
cntn_template = ["총 {}명\\n",
                 "발열 도시락({}명)\\n",
                 "보온 도시락({}명)\\n",
                 "오늘의 샐러드({}명)\\n"]


def apply_cntn_capsule(string: str) -> str:
    return "{\"COMPS\":[{\"COMP_TYPE\":\"TEXT\",\"COMP_DETAIL\":{\"HASHTAGS\":[],\"MENTIONS\":[],\"CONTENTS\":\"" + string + "\"}}]}"


def get_cntn_template(strings: list) -> str:
    cntn = cntn_preface
    total_len = len(strings[0]) + len(strings[1]) + len(strings[2])
    cntn += template[0].format(total_len)
    for i in range(3):
        cntn += "\\n"
        name_list = strings[i]
        cntn += cntn_template[i + 1].format(len(name_list))
        for name in name_list:
            cntn += "{}\\n".format(name)
    return apply_cntn_capsule(cntn)


if __name__ == "__main__":
    print(get_html_template([['기선주 사원'], ['김준영 대리'], ['김진욱 사원']]))
    print(get_cntn_template([['기선주 사원'], ['김준영 대리'], ['김진욱 사원']]))
