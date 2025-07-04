FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

# 使用阿里云镜像源加速pip安装
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip config set global.trusted-host mirrors.aliyun.com

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./scripts /app/scripts
COPY ./pyproject.toml ./alembic.ini /app/
COPY ./app /app/app

ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
