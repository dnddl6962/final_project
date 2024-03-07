import json

def create_jsonlines(df5):
    user_quiz_dict = {}
    for index, row in df5.iterrows():
        user_id = row['UserID']
        quiz_code = f'quiz{row["QuizCode"]}'
        correct = row['Correct']

        if user_id not in user_quiz_dict:
            user_quiz_dict[user_id] = {}
        user_quiz_dict[user_id][quiz_code] = correct

    with open('test1.jsonlines', 'w') as outfile:
        for user, quiz in user_quiz_dict.items():
            json.dump({"subject_id": user, "responses": quiz}, outfile)
            outfile.write('\n')
