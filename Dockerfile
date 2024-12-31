# dockerfile_backend
FROM python:3.12.6-slim

# 작업 디렉토리 설정
WORKDIR /app

# 소스 코드 복사
COPY . /app

# requirements.txt가 존재하면 pip install 수행
RUN if [ -f "requirements.txt" ]; then pip install -r requirements.txt; fi

# Lambda 기본 엔트리포인트 설정
CMD ["main_lambda.handler"]
