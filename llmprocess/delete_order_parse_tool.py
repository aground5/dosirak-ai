from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

from constants import LLM_MODEL, OLLAMA_ENDPOINT

if __name__ != "__main__":
    from .parser import followup_question_parser
if __name__ == "__main__":
    from llmprocess.parser import followup_question_parser

examples = [
    {"input": "오늘의 샐러드 취소 부탁드립니다.",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: Does the sentence above mention any specific lunchbox type?
Intermediate answer: Yes. (샐러드)
So the final answer is: 샐러드
"""},
    {"input": "취소할게요.",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: Does the sentence above mention any specific lunchbox type?
Intermediate answer: No.
Follow up: Can I consider this sentence as an entire order cancellation because the sentence don't have a specific type of lunchbox?
Intermediate answer: Yes.
So the final answer is: entire order
"""},
    {"input": "샐러드, 발열 취소 부탁드립니다.",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: Does the sentence above mention any specific lunchbox type?
Intermediate answer: Yes. (샐러드, 발열)
So the final answer is: 샐러드, 발열
"""},
#     {"input": "샐러드 취소 부탁해요~",
#      "output": """
# Are follow up questions needed here: No.
# Reason why don't need questions: Because the answer is directly stated in the sentence.
# So the final answer is: 샐러드
# """},
]
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "sentence: {input}\n"
                  "question: According to sentence, which type of launchbox was canceled? or is it an entire order cancellation?"),
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
                  "question: According to sentence, which type of launchbox was canceled? or is it an entire order cancellation?"),
    ]
)

humanInput="주문 취소 요청 드립니다."

model = ChatOllama(base_url=OLLAMA_ENDPOINT, model=LLM_MODEL)

chain = final_prompt | model | followup_question_parser

if __name__ == "__main__":
    print(final_prompt.format(
        input=humanInput
    ))
    for i in range(0, 10):
        print("Attempt: {} of 10".format(i + 1))
        ai_answer = chain.invoke({
            "input": humanInput
        })
        print(ai_answer)
