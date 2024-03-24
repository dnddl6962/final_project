from Athena_Connection.conn_athena import connect_to_athena
from Data_Preprocessing.query_athena import query_athena_data
from Data_Preprocessing.filter_data import filter_data
from JSON_Creation.create_jsonlines import save_data_to_jsonlines


conn = connect_to_athena()
df5 = query_athena_data(conn)
df5_filtered = filter_data(df5)
save_data_to_jsonlines(df5_filtered)


