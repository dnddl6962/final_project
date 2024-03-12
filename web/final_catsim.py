'''
pip install py-irt
pip install -U catsim
pip install #seaborn
'''
from catsim.cat import rmse, mse
from catsim.simulation import *
from catsim.initialization import *
from catsim.selection import *
from catsim.estimation import *
from catsim.stopping import *
from catsim.irt import icc
from catsim import plot
from catsim.irt import normalize_item_bank, validate_item_bank, reliability
import catsim.plot as catplot
import pandas as pd
import numpy as np
import seaborn as sns
import catsim
import math
import random
import os
import re
import json
import matplotlib.pyplot as plt



with open('/content/drive/MyDrive/Colab Notebooks/천재교육 프로젝트/최종 프로젝트/kdt_5th_data/Remove_Duplicates/best_parameters_5grade.json', 'r') as json_file:
    json_data = json.load(json_file)

result_array = []

for i in range(len(json_data['disc'])):
    new_array = [json_data['disc'][i], json_data['diff'][i], 0, 1]
    result_array.append(new_array)

np.array(result_array)
## ---------------------------------------- 여기까지 json 열고 result_array 댓고오는거임 ----------------------------------------------------

class Simulator:
    def __init__(self, result_array, max_items, initializer, selector, estimator, stopper):
        #simulator로 돌려야 되니까 self 로 그냥 다 받았습니다. 
        self.result_array = result_array
        self.max_items = max_items
        self.initializer = initializer
        self.selector = selector
        self.estimator = estimator
        self.stopper = stopper

    def simulate(self, verbose=False):
        administered_items = []
        responses = []

        # 초기 4문제의 문제 ID
        initial_item_ids = ['quiz30049372', 'quiz30064607', 'quiz30048859', 'quiz30062323']

        # 초기 4문제의 인덱스를 찾아서 administered_items에 추가하고 응답 벡터에 대응하는 응답을 추가
        for item_id in initial_item_ids:
            item_index = list(json_data['item_ids'].values()).index(item_id)
            administered_items.append(item_index)

            # 초기 문제에 대한 응답 추가
            correct = input(f"Did the user answer the item {item_id} correctly? (True/False): ").lower()
            if correct not in ['true', 'false']:
                print("Invalid input. Please enter either 'True' or 'False'.")
                continue
            responses.append(correct == 'true')

        # 초기화 단계
        est_theta = self.initializer.initialize()

        est_theta = self.estimator.estimate(
        items=np.array(self.result_array),
        administered_items=administered_items,
        response_vector=responses,
        est_theta=est_theta
    )
        # 여기까지가, 이제 해당 4문제들을 난이도가 중간값에 근사한 걸로 넣어가지고 진행했구요
        # 여기서 이제 사용자가 입력받아 True or False로 알겠지

    # 초기 4문제 후의 능력치 출력
        if verbose:
            print("Initial 4 items answered. Estimated proficiency:", est_theta)
            ## 여기까지 이제 4문제를 풀고 난후의 theta 값 즉, 사용자의 능력치를 추정

        while True:
            # 추천 단계
            if len(administered_items) >= len(initial_item_ids):
                item_index = self.selector.select(items=np.array(self.result_array), administered_items=administered_items, est_theta=est_theta)
            else:
                # 초기 문제를 추천하지 않도록 건너뛰기
                item_index = administered_items[len(administered_items)]

            next_item_id = json_data['item_ids'][str(item_index)]
            ## 여기까지 이제 문제를 select해서 퀴즈코드 추천  -> 문제 추천해줘

            # 평가 단계
            true_theta = 0.0
            a, b, c, d = np.array(self.result_array)[item_index]
            prob = icc(true_theta, a, b, c, d)
            correct = input(f"Did the user answer the item {next_item_id} correctly? (True/False): ").lower()
            if correct not in ['true', 'false']:
                print("Invalid input. Please enter either 'True' or 'False'.")
                continue
            correct = (correct == 'true')

            # 여기까지가 그 문제를 맞추고, 틀렸는지 이제 estimation 해줘요

            # 중단 단계
            if len(administered_items) >= self.max_items or self.stopper.stop(administered_items=np.array(self.result_array)[administered_items], theta=est_theta):
                break
            #max_item 은 필요없긴 한데, self stopper에서 종단기준이 만족하면 stop

            # 결과 기록
            administered_items.append(item_index)
            responses.append(correct)

            if verbose:
                print('Estimated proficiency, given answered items:', est_theta)
                print('Next item to be administered:', next_item_id)
                print('Probability to correctly answer item:', prob)
                print('Did the user answer the selected item correctly?', correct)
                print("responses: ", responses)

            # 능력치 업데이트
            est_theta = self.estimator.estimate(
                items=np.array(self.result_array),
                administered_items=administered_items,
                response_vector=responses,
                est_theta=est_theta
            )

        if verbose:
            print("responses: ", responses)
        print("사용자의 최종 능력치 (Estimated Proficiency):", est_theta)
        # 사용자의 최종 능력치를 추정해줌.


## --------------------- 여기까지가 클래스 정의고 밑에 클래스 돌리는거 ---------------------------------
initializer = FixedPointInitializer(0)
selector = UrrySelector()
estimator = NumericalSearchEstimator()
stopper = MinErrorStopper(.6)

s = Simulator(np.array(result_array), 20, initializer, selector, estimator, stopper)
s.simulate(verbose=True)


# ----- 분기 처리 해드리고 싶은데 그냥 알아서 해주세요 ㅅㄱ----------------------