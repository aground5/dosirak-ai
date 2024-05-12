from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

from constants import LLM_MODEL, OLLAMA_ENDPOINT
from .parser import followup_question_parser

known_people_list = ['강성수', '강양기', '강용문', '강태형', '기선주', '김경태', '김기호', '김범선', '김수연', '김영주', '김원민', '김원정', '김종민', '김준영', '김지호', '김진욱', '김창우', '김태균', '김한조', '김행수', '김현수', '김효성', '류광춘', '류혜영', '문형진', '박성현', '배만수', '배윤서', '백석영', '변화영', '상담 운영 종료', '손옥재', '신세화', '신지인', '안기도', '양태순', '오미소', '윤동균', '윤여표', '이민정', '이선순', '이선우', '이승훈', '이은채', '이화진', '임차희', '임형규', '장진수', '정서원', '정시안', '정일', '정종윤', '정창환', '조정은', '최민수', '플로우 운영자']

examples = [
    {"input": "김영주 대리, 문형진 차장 발열도시락 신청 부탁드립니다!",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: Is there a word in the sentence above that is supposed to be a person's name?
Intermediate answer: Yes.
Follow up: What is the word that is a person's name?
Intermediate answer: 
1. 김영주
2. 문형진
So the final answer is: 2
"""},
    {"input": "정서원 사원 오늘의 샐러드 취소 부탁드립니다.",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: Is there a word in the sentence above that is supposed to be a person's name?
Intermediate answer: Yes.
Follow up: What is the word that is a person's name?
Intermediate answer: 
1. 정서원
So the final answer is: 1
"""},
    {"input": "김진경 오늘의 샐러드 신청 부탁드립니다.",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: Is there a word in the sentence above that is supposed to be a person's name?
Intermediate answer: Yes.
Follow up: What is the word that is a person's name?
Intermediate answer: 
1. 김진경
So the final answer is: 1
"""},
    {"input": "발열 도시락, 오늘의 샐러드 주문합니다!",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: Is there a word in the sentence above that is supposed to be a person's name?
Intermediate answer: No.
So the final answer is: 0
"""},
]
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "sentence: {input}\n"
                  "question: How many people showed up in this sentence?"),
        ("ai", "{output}")
    ]
)
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples
)
final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are very helpful ai. You have known people list. Known people list: {people_list}\n"),
        few_shot_prompt,
        ("human", "sentence: {input}\n"
                  "question: How many people showed up in this sentence?"),
    ]
)

humanInput="김태균 사원, 김진경 대리 보온도시락 추가요!"

model = ChatOllama(base_url=OLLAMA_ENDPOINT, model=LLM_MODEL)

chain = final_prompt | model | followup_question_parser

if __name__ == "__main__":
    print(final_prompt.format(
        people_list=known_people_list,
        input=humanInput
    ))
    ai_answer = chain.invoke({
        "people_list": known_people_list,
        "input": humanInput
    })
    print(ai_answer)
