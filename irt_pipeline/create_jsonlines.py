import json
from log_data import setup_logging

logger = setup_logging()

def save_data_to_jsonlines(df5):
    try:
        user_quiz_dict = {}
        for index, row in df5.iterrows():
            user_id = row['userid']
            quiz_code = f'quiz{row["quizcode"]}'
            correct = row['correct']

            if user_id not in user_quiz_dict:
                user_quiz_dict[user_id] = {}
            user_quiz_dict[user_id][quiz_code] = correct

        with open('test1.jsonlines', 'w') as outfile:
            for user, quiz in user_quiz_dict.items():
                json.dump({"subject_id": user, "responses": quiz}, outfile)
                outfile.write('\n')

        logger.info("Data saved to JSONLines file successfully")
    except Exception as e:
        logger.error(f"Failed to save data to JSONLines: {str(e)}")
        raise e
