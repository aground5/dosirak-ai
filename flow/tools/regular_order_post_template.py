# 문단 사이를 nbsp로 표현하는 듯
preface = ("<p>3월 동안 일주일 중 몇요일에 신청을 원하는지 댓글로 남겨주세요.<br>"
           "\"월화수목금\" 이렇게 댓글 남겨주시면 해당 요일에 기본적으로 신청해놓겠습니다.<br>"
           "도시락 종류 언급 없을 시 보온 도시락으로 신청됩니다</p>"
           "<p>&nbsp;</p>"
           "<p>도시락 변동 가격</p>"
           "<p>발열도시락(+ 발열팩) : 7,000원<br>"
           "보온도시락 : 6,500원<br>"
           "오늘의 샐러드 : 6,500원</p>"
           "<p>(보온 도시락은 발열팩 옵션이 없습니다!)</p>")

template = ["<p>발열 도시락</p>",
            "<p>보온 도시락</p>",
            "<p>오늘의 샐러드</p>"]


def get_html_template(strings: list) -> str:
    html = preface
    for i in range(3):
        html += "<p>&nbsp;</p>"
        name_list = strings[i]
        html += template[i]
        for name in name_list:
            html += "<p>{}</p>".format(name)
    return html


cntn_preface = ("3월 동안 일주일 중 몇요일에 신청을 원하는지 댓글로 남겨주세요.\\n"
                '"월화수목금" 이렇게 댓글 남겨주시면 해당 요일에 기본적으로 신청해놓겠습니다.\\n'
                "도시락 종류 언급 없을 시 보온 도시락으로 신청됩니다.\\n"
                "\\n"
                "도시락 변동 가격\\n"
                "발열도시락(+ 발열팩) : 7,000원\\n보온도시락 : 6,500원\\n"
                "오늘의 샐러드 : 6,500원\\n"
                "(보온 도시락은 발열팩 옵션이 없습니다!)\\n")

cntn_template = ["발열 도시락\\n",
                 "보온 도시락\\n",
                 "오늘의 샐러드\\n"]


def apply_cntn_capsule(string: str) -> str:
    return "{\"COMPS\":[{\"COMP_TYPE\":\"TEXT\",\"COMP_DETAIL\":{\"HASHTAGS\":[],\"MENTIONS\":[],\"CONTENTS\":\"" + string + "\"}}]}"


def get_cntn_template(strings: list) -> str:
    cntn = cntn_preface
    for i in range(3):
        cntn += "\\n"
        name_list = strings[i]
        cntn += cntn_template[i]
        for name in name_list:
            cntn += "{}\\n".format(name)
    return apply_cntn_capsule(cntn)


if __name__ == "__main__":
    print(get_html_template([['기선주 사원(월)'], ['김준영 대리(월화수목)'], ['김진욱 사원(월화수목)']]))
    print(get_cntn_template([['기선주 사원(월)'], ['김준영 대리(월화수목)'], ['김진욱 사원(월화수목)']]))
