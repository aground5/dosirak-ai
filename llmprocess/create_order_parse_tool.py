from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

from constants import LLM_MODEL, OLLAMA_ENDPOINT
from .parser import followup_question_parser

examples = [
    {"input": ",  발열도시락 신청 부탁드립니다!",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: Which type of launchbox was ordered?
Intermediate answer: 발열
Follow up: Is there any information about the order quantity in the given sentence?
Intermediate answer: No. I'll consider the order quantity is 1.
So the final answer is: (발열, 1)
"""},
    {"input": "오늘의 샐러드 추가 부탁드립니다.",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: Which type of launchbox was ordered?
Intermediate answer: 샐러드
Follow up: Is there any information about the order quantity in the given sentence?
Intermediate answer: No. I'll consider the order quantity is 1.
So the final answer is: (샐러드, 1)
"""},
    {"input": "샐러드 2개, 보온도시락 1개 신청합니다.",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: Which type of launchbox was ordered?
Intermediate answer: 샐러드, 보온
Follow up: Is there any information about the order quantity in the given sentence?
Intermediate answer: Yes.
Follow up: Then, how much is the order quantity?
Intermediate answer: 2 for 샐러드, 1 for 보온
So the final answer is: (샐러드, 2), (보온, 1)
"""},
    {"input": "샐러드 2개 신청합니다!",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: Which type of launchbox was ordered?
Intermediate answer: 샐러드
Follow up: Is there any information about the order quantity in the given sentence?
Intermediate answer: Yes.
Follow up: Then, how much is the order quantity?
Intermediate answer: 2
So the final answer is: (샐러드, 2)
"""},
    {"input": "보온 도시락하고 샐러드 주문합니다",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: Which type of launchbox was ordered?
Intermediate answer: 보온, 샐러드
Follow up: Is there any information about the order quantity in the given sentence?
Intermediate answer: No. I'll consider the order quantity is 1.
So the final answer is: (보온, 1), (샐러드, 1)
"""},
]
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "sentence: {input}\n"
                  "question: According to sentence, which lunchbox type was ordered and how many?"),
        ("ai", "{output}")
    ]
)
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples
)
final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are very helpful ai. You have available lunchbox type list.\n"
                   "lunchbox type list: \n"
                   "발열 //Also said: 발열도시락, 발열 도시락\n"
                   "보온 //Also said: 보온도시락, 보온 도시락\n"
                   "샐러드 //Also said: 오늘의 샐러드, 오늘의샐러드\n"),
        few_shot_prompt,
        ("human", "sentence: {input}\n"
                  "question: According to sentence, which lunchbox type was ordered and how many?"),
    ]
)

humanInput="기선주 사원 샐러드, 보온 주문할게요."

model = ChatOllama(base_url=OLLAMA_ENDPOINT, model=LLM_MODEL)

chain = final_prompt | model | followup_question_parser

if __name__ == "__main__":
    print(final_prompt.format(
        input=humanInput
    ))
    ai_answer = chain.invoke({
        "input": humanInput
    })
    print(ai_answer)
