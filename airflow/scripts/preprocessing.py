import requests
import pandas as pd
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
