FROM python:3.9-slim
EXPOSE 8501
WORKDIR /app
RUN apt-get update && apt-get install -y\
    build-essential \
    sofware-properties-commom \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone  .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "home.py", "--server.port=88501:88501"]