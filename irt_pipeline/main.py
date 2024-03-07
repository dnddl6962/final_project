
from load import load_and_preprocess_data
from filter import filter_data
from create_json import create_jsonlines
from json_load import load_json_config

# 데이터 로딩 및 전처리
df5 = load_and_preprocess_data('mathcat-bucket', 'DATA_preprocessing/Unsaved/2024/03/06/baba44b9-9567-4da7-872e-35cde599f185.csv')

# 데이터 필터링
df5_filtered = filter_data(df5)

# 데이터 변환 및 JSONLines 파일 생성
create_jsonlines(df5_filtered)

# JSON 파일 로딩
json_config = load_json_config('best_parameters_filter.json')
