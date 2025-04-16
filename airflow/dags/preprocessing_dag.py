from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# 기본 설정 정의
default_args = {
    "owner": "airflow",  # DAG 소유자
    "start_date": datetime(2024, 4, 16),  # DAG 실행 시작 날짜
    "retries": 1,  # 실패 시 재시도 횟수
    "retry_delay": timedelta(minutes=5),  # 재시도 간격 (5분 후 재시도)
}

# DAG 정의 (with 블록 내부에서 task들을 정의함)
with DAG(
    dag_id="avatar_character_preprocessing",  # DAG 이름 (고유 식별자)
    default_args=default_args,  # 기본 인자 전달
    schedule_interval="* * * * *",  # 실행 주기: 매 1분마다 실행
    catchup=False,  # 과거 날짜의 미수행 DAG catch-up 실행 여부 (False면 안 함)
    tags=["preprocessing"],  # Airflow UI에서 DAG 구분용 태그
    is_paused_upon_creation=False,  # DAG이 생성되자마자 실행 가능 상태로 설정
) as dag:

    # BashOperator를 사용해 preprocessing.py 실행
    run_preprocessing = BashOperator(
        task_id="run_avatar_preprocessing",  # task의 이름 (UI에서 식별용)
        bash_command="python /opt/airflow/scripts/preprocessing.py",  # 실제 실행할 bash 명령어
        dag=dag,  # 명시적으로 DAG 연결 (with 블록 안에선 생략해도 됨)
    )

    # 태스크 실행 명시 (단일 태스크일 경우 이 라인 없어도 됨)
    run_preprocessing
