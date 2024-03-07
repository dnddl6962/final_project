import pandas as pd

def filter_data(df5):
    quiz_filter = df5.groupby(['QuizCode'])['UserID'].nunique().reset_index()
    quiz_filter = quiz_filter[quiz_filter['UserID'] >= 500]['QuizCode']

    user_filter = df5.groupby(['UserID'])['QuizCode'].nunique().reset_index()
    user_filter = user_filter[user_filter['QuizCode'] >= 20]['UserID']

    df5_filter = df5[df5['QuizCode'].isin(quiz_filter) & df5['UserID'].isin(user_filter)]
    
    return df5_filter
