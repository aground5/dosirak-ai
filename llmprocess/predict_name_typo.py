from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

from constants import LLM_MODEL, OLLAMA_ENDPOINT
from llmprocess.parser import followup_question_parser

known_people_list = ['강성수', '강양기', '강용문', '강태형', '기선주', '김경태', '김기호', '김범선', '김수연', '김영주', '김원민', '김원정', '김종민', '김준영', '김지호', '김진욱', '김창우', '김태균', '김한조', '김행수', '김현수', '김효성', '류광춘', '류혜영', '문형진', '박성현', '배만수', '배윤서', '백석영', '변화영', '상담 운영 종료', '손옥재', '신세화', '신지인', '안기도', '양태순', '오미소', '윤동균', '윤여표', '이민정', '이선순', '이선우', '이승훈', '이은채', '이화진', '임차희', '임형규', '장진수', '정서원', '정시안', '정일', '정종윤', '정창환', '조정은', '최민수', '플로우 운영자']

examples = [
    {"input": "기선주",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: Does the given name match exactly one of the list of known people?
Intermediate answer: Yes.
So the final answer is: Yes.
"""},
    {"input": "문형딘",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: Does the given name match exactly one of the list of known people?
Intermediate answer: No.
Follow up: So what is one of the most similar known names to a given name?
Intermediate answer: 문형진
Follow up: Can be acceptable 문형딘 as typos of 문형진?
Intermediate answer: Yes.
So the final answer is: Yes.
"""},
    {"input": "김진경",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: Does the given name match exactly one of the list of known people?
Intermediate answer: No.
Follow up: So what is one of the most similar known names to a given name?
Intermediate answer: 김진욱
Follow up: Can be acceptable 김진경 as typos of 김진욱?
Intermediate answer: No.
So the final answer is: No.
"""},
    {"input": "김범수",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: Does the given name match exactly one of the list of known people?
Intermediate answer: No.
Follow up: So what is one of the most similar known names to a given name?
Intermediate answer: 김범선
Follow up: Can be acceptable 김범수 as typos of 김범선?
Intermediate answer: No.
So the final answer is: No.
"""},
    {"input": "한문철",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: Does the given name match exactly one of the list of known people?
Intermediate answer: No.
Follow up: So what is one of the most similar known names to a given name?
Intermediate answer: 최민수
Follow up: Can be acceptable 한문철 as typos of 최민수?
Intermediate answer: No.
So the final answer is: No.
"""},
]
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "name: {input}\n"
                  "question: Is the given name on the known people list? You can accept some little typo."),
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
        ("human", "name: {input}\n"
                  "question: Is the given name on the known people list? You can accept some little typo."),
    ]
)

humanInput="박진수, 김진수"

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
