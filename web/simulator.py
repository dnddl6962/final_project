import numpy as np
from catsim.initialization import FixedPointInitializer
from catsim.selection import UrrySelector
from catsim.estimation import NumericalSearchEstimator
from catsim.stopping import MinErrorStopper
from load import load_data
from quiz import json_to_array, get_quiz

    
initializer = FixedPointInitializer(0)
selector = UrrySelector()
estimator = NumericalSearchEstimator(precision=8, dodd=True, method='ternary')
stopper = MinErrorStopper(0.6)

json_data = load_data('mathcat-bucket', 'irt_result/yyyy=2024/mm=03/dd=13/irt_result.json')
result_array = json_to_array(json_data)
initial_item_ids = get_quiz(json_data, result_array)


class SimulatorManager:
    def __init__(self):
        self.simulator = None
    
    def initialize_simulator(self):
        self.simulator = Simulator(np.array(result_array), 4, 12, initializer, selector, estimator, stopper)


class Simulator:
    def __init__(self, result_array, init_items, max_items, initializer, selector, estimator, stopper):
        self.result_array = result_array
        self.init_items = init_items
        self.max_items = max_items
        self.initializer = initializer
        self.selector = selector
        self.estimator = estimator
        self.stopper = stopper
        self.administered_items = []
        self.responses = []
        self.index = 0

    def recommend_next(self, user_answer=None, quiz=False):
        
        ## 다음 문제 추천
        # 초기 4문제는 리스트에서 반환
        if len(self.administered_items) < self.init_items:
            if quiz:
                return initial_item_ids[self.index]

            item_index = list(json_data['item_ids'].values()).index(initial_item_ids[self.index])
            self.administered_items.append(item_index)

            # 문제에 대한 응답 추가
            correct = user_answer
            self.responses.append(correct == True)
            print(f'Did the user answer the item {initial_item_ids[self.index]} correctly?: {self.responses[self.index]}')


        # 5번째 문제부터는 사용자의 학습 수준에 맞게 추천
        else:
            item_index = self.selector.select(items=self.result_array, administered_items=self.administered_items, est_theta=self.est_theta)
            if quiz:
                return json_data['item_ids'][str(item_index)]
            
            self.administered_items.append(item_index)

            # 문제에 대한 응답 추가
            correct = user_answer
            self.responses.append(correct == True)
            print(f"Did the user answer the item {json_data['item_ids'][str(item_index)]} correctly?: {self.responses[self.index]}")


        # 사용자의 학습 수준 추정
        if self.index == 3:
            self.est_theta = self.initializer.initialize()
            self.est_theta = self.estimator.estimate(
                items=np.array(self.result_array),
                administered_items=self.administered_items,
                response_vector=self.responses,
                est_theta=self.est_theta
            )
        elif self.index > 3:
            self.est_theta = self.estimator.estimate(
                items=np.array(self.result_array),
                administered_items=self.administered_items,
                response_vector=self.responses,
                est_theta=self.est_theta
            )
        else:
            self.est_theta = 0
            
        if len(self.administered_items) == self.max_items or self.stopper.stop(administered_items=np.array(self.result_array)[self.administered_items], theta=self.est_theta):
            # 사용자의 학습 수준 출력
            print("시험 종료")
            print("Final estimated proficiency:", self.est_theta)
            return self.est_theta, self.administered_items, self.responses, self.index + 1, True

        self.index += 1
        return self.est_theta, self.administered_items, self.responses, self.index + 1, False