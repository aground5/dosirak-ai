from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

from constants import LLM_MODEL, OLLAMA_ENDPOINT

if __name__ != "__main__":
    from .parser import followup_question_parser
if __name__ == "__main__":
    from llmprocess.parser import followup_question_parser

examples = [
    {"input": "오늘의 샐러드 2개 변경 요청 드립니다.",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: What type of lunch box are you changing from?
Intermediate answer: Not provided
Follow up: What type of lunch box would you like to change it to?
Intermediate answer: 샐러드
Follow up: How many of these lunch boxes are you looking to change? If not specified, default is 1.
Intermediate answer: 2 for 샐러드
So the final answer is: Nothing to (샐러드, 2)
"""},
    {"input": "발열 도시락에서 보온 도시락으로 바꿔주세요.",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: What type of lunch box are you changing from?
Intermediate answer: 발열
Follow up: What type of lunch box would you like to change it to?
Intermediate answer: 보온
Follow up: How many of these lunch boxes are you looking to change? If not specified, default is 1.
Intermediate answer: 1 for 보온
So the final answer is: 발열 to (보온, 1)
"""},
    {"input": "발열도시락으로 변경부탁드려요~",
     "output": """
You should use follow up questions for more accuracy: Okay, I will.
Follow up: What type of lunch box are you changing from?
Intermediate answer: Not provided
Follow up: What type of lunch box would you like to change it to?
Intermediate answer: 발열
Follow up: How many of these lunch boxes are you looking to change? If not specified, default is 1.
Intermediate answer: 1 for 발열
So the final answer is: Nothing to (발열, 1)
"""},
]
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "sentence: {input}\n"
                  "question: The given sentence is a request to modify a lunchbox order.\n"
                  "Please determine what lunchbox needs to be changed to what."),
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
                  "question: The given sentence is a request to modify a lunchbox order.\n"
                  "Please determine what lunchbox needs to be changed to what."),
    ]
)

humanInput="바꿔주세요."

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
