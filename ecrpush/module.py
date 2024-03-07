import pandas as pd
import numpy as np

class TitanicProcessor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.df = None

    def load_data(self):
        self.df = pd.read_csv(self.input_file)

    def drop_columns(self):
        self.df.drop(['Sex', 'Cabin'], axis=1, inplace=True)

    def extract_titles(self):
        list1 = []
        for i in range(self.df['Name'].count()):
            list1.append(self.df['Name'][i].split(', ')[1].split('. ')[0])
        self.df['Sex'] = list1

    def map_sex(self):
        sex_mapping = {
            'Mr': 'Male',
            'Master': 'Male',
            'Col': 'Male',
            'Rev': 'Male',
            'Dr': 'Male',  
            'Mrs': 'Female',
            'Miss': 'Female',
            'Ms': 'Female',
            'Dona': 'Female'
        }
        self.df['Sex'] = self.df['Sex'].map(sex_mapping)

    def fill_age(self):
        # self.df['Age'].fillna(self.df['Age'].median(), inplace=True)
        self.df['Age'].fillna(self.df['Age'].mode(), inplace=True)

    def add_check_column(self):
        self.df['Check'] = np.where((self.df['Sex']=='Male') & (self.df['Age']>=10) & (self.df['Age']<20), 'O', 'X')

    def save_result(self):
        self.df.to_csv(self.output_file)

    def process(self):
        self.load_data()
        self.drop_columns()
        self.extract_titles()
        self.map_sex()
        self.fill_age()
        self.add_check_column()
        self.save_result()

