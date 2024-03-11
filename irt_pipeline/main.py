from conn_athena import connect_to_athena
from query_athena import query_athena_data
from filter_data import filter_data
from create_jsonlines import save_data_to_jsonlines


conn = connect_to_athena()
df5 = query_athena_data(conn)
df5_filtered = filter_data(df5)
save_data_to_jsonlines(df5_filtered)


