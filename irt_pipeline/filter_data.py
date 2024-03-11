import pandas as pd
from log_data import setup_logging

logger = setup_logging()

def filter_data(df5):
    try:
        df5['correct'] = df5['correct'].replace({'O': 1, 'X': 0})
        quiz_filter = df5.groupby(['quizcode'])['userid'].nunique().reset_index()
        quiz_filter = quiz_filter[quiz_filter['userid'] >= 500]['quizcode']

        user_filter = df5.groupby(['userid'])['quizcode'].nunique().reset_index()
        user_filter = user_filter[user_filter['quizcode'] >= 20]['userid']

        filtered_df = df5[df5['quizcode'].isin(quiz_filter) & df5['userid'].isin(user_filter)]
        
        logger.info("Data filtering successful")
        return filtered_df

    except Exception as e:
        logger.error(f"Failed to filter data: {str(e)}")
        raise e
