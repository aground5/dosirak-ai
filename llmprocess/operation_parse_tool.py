from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

from constants import LLM_MODEL, OLLAMA_ENDPOINT

if __name__ != "__main__":
    from .parser import followup_question_parser
if __name__ == "__main__":
    from llmprocess.parser import followup_question_parser

examples = [
    {"input": "김영주 대리, 문형진 차장 발열도시락 신청 부탁드립니다!",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: Does the given sentence indicate a desire to order a lunchbox or to place an additional order?
Intermediate answer: Yes.
So the final answer is: create
"""},
    {"input": "정서원 사원 오늘의 샐러드 취소 부탁드립니다.",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: Does the given sentence indicate a desire to order a lunchbox or to place an additional order?
Intermediate answer: No.
Follow up: Does the given sentence indicate a desire to cancel a lunchbox order, delete a lunchbox order, or express an intention not to eat the lunchbox?
Intermediate answer: Yes.
So the final answer is: cancel
"""},
    {"input": "박성현 오늘의 샐러드로 변경 부탁드립니다.",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: Does the given sentence indicate a desire to order a lunchbox or to place an additional order?
Intermediate answer: No.
Follow up: Does the given sentence indicate a desire to cancel a lunchbox order, delete a lunchbox order, or express an intention not to eat the lunchbox?
Intermediate answer: No.
Follow up: Does the given sentence indicate a desire to change the type of lunchbox or to change the quantity of lunchboxes?
Intermediate answer: Yes.
So the final answer is: change
"""},
    {"input": "발열 도시락 주문을 오늘의 샐러드로 바꿔주세요!",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: Does the given sentence indicate a desire to order a lunchbox or to place an additional order?
Intermediate answer: No.
Follow up: Does the given sentence indicate a desire to cancel a lunchbox order, delete a lunchbox order, or express an intention not to eat the lunchbox?
Intermediate answer: No.
Follow up: Does the given sentence indicate a desire to change the type of lunchbox or to change the quantity of lunchboxes?
Intermediate answer: Yes.
So the final answer is: change
"""},
#     {"input": "저 취소여",
#      "output": """
# Are follow up questions needed here: No.
# Reason why don't need questions: Because the answer is directly stated in the sentence.
# So the final answer is: cancel
# """},
]
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "sentence: {input}\n"
                  "question: According to sentence, which operation should be used?"),
        ("ai", "{output}")
    ]
)
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples
)
final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are very helpful ai. You have available operations to process user's request.\n"
                   "operation list: \n"
                   "create //Create new order\n"
                   "change //Change order\n"
                   "cancel //Cancel order\n"
                   "launchbox type list: \n"
                   "발열 //Also said: 발열도시락, 발열 도시락\n"
                   "보온 //Also said: 보온도시락, 보온 도시락\n"
                   "샐러드 //Also said: 오늘의 샐러드, 오늘의샐러드\n"),
        few_shot_prompt,
        ("human", "sentence: {input}\n"
                  "question: According to sentence, which operation should be used?"),
    ]
)

model = ChatOllama(base_url=OLLAMA_ENDPOINT, model=LLM_MODEL)

chain = final_prompt | model | followup_question_parser

if __name__ == "__main__":
    humanInput="김효성 대리 샐러드로 바꿀게요."
    print(final_prompt.format(
        input=humanInput
    ))
    ai_answer = chain.invoke({
        "input": humanInput
    })
    print(ai_answer)
