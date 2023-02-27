import db

db = db.DataBase()


def _parse_message(message):
    parsed_message = message.strip().lower()
    return parsed_message


def is_answer_correct(user, message):
    parsed_message = _parse_message(message.text)

    question = db.get_question(user["question_index"])


    if question["correct"] == parsed_message:
        if user["is_tip"]:
            user["points"]+=1


        user["question_index"] += 1
        db.set_user(message.chat.id, {"question_index": user["question_index"], "points" : user["points"], "is_tip": True})

        return True


    return


def get_question_message(user):
    text = _check_end(user)

    if text is not None:
        return text

    text = []
    question = db.get_question(user["question_index"])
    for message in question['text']:
        text.append(message)

    return text


def _check_end(user):
    if user["question_index"] == db.questions_count:
        text = ["Вы прошли викторину!"]
        db.set_user(user["chat_id"], {"is_passed": True, "is_passing": False})
        return text
    return
