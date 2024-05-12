import logging
import re

from nlp.word_distance import min_distance_in_list


def count_people_parse(parsed_followup_questions, known_people_list: list):
    order_people = []

    qa_list = parsed_followup_questions["qa_list"]
    final_answer = parsed_followup_questions["final_answer"]

    if final_answer != '0':
        people_strings = None
        for qa in qa_list:
            if qa[0] == "What is the word that is a person's name?":
                people_strings = qa[1]

        if people_strings is not None:
            people = people_strings.split('\n')
            for i in range(len(people)):
                name = people[i]
                numbering = re.search("^[0-9].*\.", name)
                people[i] = name[numbering.span()[1]:].strip()

            for person in people:
                possible_people, distance = min_distance_in_list(person, known_people_list)
                if distance > 0.5:
                    logging.warning(f"count_people_parse: 거리가 너무 멉니다. distance={distance} name={person} possible_people={possible_people}")
                elif len(possible_people) > 1:
                    logging.warning(f"count_people_parse: 가능한 이름이 두개 이상 입니다. distance={distance} name={person} possible_people={possible_people}")
                elif len(possible_people) == 1:
                    order_people.append(possible_people[0])
                else:
                    logging.error(f"count_people_parse: 가능한 이름이 없습니다. distance={distance} name={person} possible_people={possible_people}")
    return order_people
