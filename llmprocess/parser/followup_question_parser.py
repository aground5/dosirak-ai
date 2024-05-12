from langchain_core.messages import AIMessage


def followup_question_parser(ai_message: AIMessage) -> dict:
    followup_start = ai_message.content.find('You should use follow up questions for more accuracy:')
    followup_end = ai_message.content.find('\n', followup_start)
    followup = ai_message.content[followup_start + len("You should use follow up questions for more accuracy:")
                                  :followup_end].strip()
    qa_list = None
    if followup == "Okay, I will.":
        start_idx = followup_end
        question_start = ai_message.content.find("Follow up:", start_idx)
        qa_list = []
        while question_start != -1:
            question_end = ai_message.content.find("Intermediate answer:", question_start)
            question = ai_message.content[question_start + len("Follow up:")
                                          :question_end].strip()
            answer_start = question_end
            answer_end = ai_message.content.find("Follow up:", answer_start)
            if answer_end == -1:
                answer_end = ai_message.content.find("So the final answer is:", answer_start)
            answer = ai_message.content[answer_start + len("Intermediate answer:")
                                        : answer_end].strip()
            question_start = ai_message.content.find("Follow up:", answer_end)
            qa_list.append((question, answer))
    elif followup == "No.":
        qa_list = []
        reason_start = ai_message.content.find("Reason why don't need questions:", followup_end)
        reason_end = ai_message.content.find("So the final answer is:", reason_start)
        reason = ai_message.content[reason_start + len("Reason why don't need questions:")
                                   :reason_end].strip()
        qa_list.append(("Reason why don't need questions", reason))
    final_answer_start = ai_message.content.find("So the final answer is:")
    final_answer = ai_message.content[final_answer_start + len("So the final answer is:")
                                      :].strip()
    return {
        "followup": followup,
        "qa_list": qa_list,
        "final_answer": final_answer
    }