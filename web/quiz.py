import numpy as np

def json_to_array(json_data):

    result_array = []

    for i in range(len(json_data['disc'])):
        new_array = [json_data['disc'][i], json_data['diff'][i], 0, 1]
        result_array.append(new_array)

    return result_array

def get_quiz(json_data, result_array):

    # 난이도 추출
    diff = np.array(result_array)[:, 1]

    # 중앙값 계산
    median_value = np.median(diff)

    # 중앙값과 가장 가까운 네 개의 행의 인덱스를 찾기 위해 argsort 사용
    # 두 번째 열의 값과 중앙값의 차이를 기준으로 오름차순 정렬 후 인덱스 반환
    sorted_indices = np.argsort(np.abs(diff - median_value))

    # 가장 작은 네 개의 인덱스 추출
    selected_indices = sorted_indices[:4]

    # 리스트 초기화
    initial_item_ids = []

    for index in selected_indices:
        item_id = json_data['item_ids'][str(index)]
        initial_item_ids.append(item_id)

    return initial_item_ids