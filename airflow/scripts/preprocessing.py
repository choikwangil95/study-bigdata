import requests
import pandas as pd
import boto3
import ast
import os
from datetime import datetime

# 1. API 호출 - 아바타 캐릭터 데이터
url = "https://api.sampleapis.com/avatar/characters"
response = requests.get(url)
data = response.json()

# 2. DataFrame 변환
df = pd.DataFrame(data)

# 3. physicalDescription 컬럼 딕셔너리로 정보들 개별 칼럼으로 분리
df["physicalDescription"] = df["physicalDescription"].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else x
)
desc_df = df["physicalDescription"].apply(pd.Series)
df = pd.concat([df.drop(columns=["physicalDescription"]), desc_df], axis=1)

# 4. 선택: 저장
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# 기본 저장 경로 설정
default_path = os.path.abspath(os.path.join(os.getcwd(), "datas"))  # 로컬 기본값

# 도커 환경이라면 /opt/airflow 경로가 존재함
if os.path.exists("/opt/airflow/datas"):
    default_path = "/opt/airflow/datas"

# 디렉토리 없으면 생성
os.makedirs(default_path, exist_ok=True)

# 최종 저장 경로
file_path = os.path.join(default_path, f"avatar_characters_{timestamp}.csv")

df.to_csv(file_path, index=False)

print(f"✅ CSV 저장 완료: {file_path}")


# 5. S3 업로드
# S3 스토리지 이름 정의
bucket_name = "hk-mlops-storage-1"

# AWS S3 클라이언트 생성
s3 = boto3.client("s3", region_name="ap-northeast-2")

# 현재 날짜와 시간으로 파일 이름 생성
file_name =  f"test/data_{timestamp}.csv"

# S3에 파일 업로드
try:
    s3.upload_file(file_path, bucket_name, file_name) # 저장할 파일명, S3 버킷명, 저장할 폴더 경로
    print(f"✅ S3 업로드 완료: s3://{bucket_name}/{file_name}")
except Exception as e:
    print(f"❌ S3 업로드 실패: {e}")
    