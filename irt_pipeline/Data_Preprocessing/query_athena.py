from pyathena.pandas.cursor import PandasCursor
from Logs.log_data import setup_logging

logger = setup_logging()

def query_athena_data(conn):
    try:
        query = '''
            WITH
            -- problem(문제 코드) 테이블
            -- 최신 교육 과정의 초등 5학년 수학 문제 중 삭제되지 않은 문제 추출
            problem_base AS(
            SELECT f_problem_id, f_difficult_cd, f_subject_id
            FROM "shine_cat"."t_problem_analysis"
            WHERE f_emh_cd ='E0' AND f_area_cd = 'MA' AND f_deleteyn ='N' AND f_subject_id IN (1982, 1983)),
            
            -- testhisdtl(문제 풀이 이력) 테이블
            -- userid와 quizcode가 중복인 데이터 모두 제외
            tbl_base AS(
            SELECT userid, quizcode, TRIM(correct) AS correct
            FROM "shine_cat"."tbl_app_testhisdtl"
            WHERE (userid, quizcode)
            IN (
                SELECT userid, quizcode
                FROM "shine_cat"."tbl_app_testhisdtl"
                GROUP BY userid, quizcode
                HAVING COUNT(*) = 1
            )
            AND correct !=''),
            
            -- INNER JOIN을 사용하여 problem_base와 tbl_base 테이블 조인
            inner_joined AS (
            SELECT
                problem_base.*,
                tbl_base.userid,
                tbl_base.quizcode,
                tbl_base.correct
            FROM
                problem_base
            INNER JOIN
                tbl_base ON problem_base.f_problem_id = tbl_base.quizcode
            )
            
            -- 문제 풀이 이력 데이터 추출
            SELECT userid, quizcode, correct, f_subject_id, f_difficult_cd
            FROM inner_joined
            WHERE correct != '' AND (correct = 'X' OR correct ='O')
        '''
        
        cursor = conn.cursor()
        df = cursor.execute(query).as_pandas()
        logger.info("Query executed successfully and data fetched from Athena")
        return df
        
    except Exception as e:
        logger.error(f"Failed to execute query and fetch data: {str(e)}")
        raise e
