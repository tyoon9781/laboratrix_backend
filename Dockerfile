FROM python:3.12.6-slim

WORKDIR /app

COPY . /app

# requirements.txt가 존재하면 pip install 수행
RUN if [ -f "requirements.txt" ]; then pip install -r requirements.txt; fi

# Lambda 기본 엔트리포인트 설정
CMD ["main_lambda.handler"]
