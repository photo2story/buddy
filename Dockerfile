# 공식 Python 런타임 이미지를 부모 이미지로 사용
FROM python:3.9-slim

# 컨테이너에서 작업 디렉토리를 설정
WORKDIR /app

# 현재 디렉토리 내용을 컨테이너의 /app에 복사
COPY . /app

# requirements.txt에 명시된 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 8080 포트를 외부에 노출
EXPOSE 8080

# 환경 변수 정의
ENV NAME World

# 컨테이너 실행 시 실행할 명령어 설정
CMD ["python", "main.py"]
