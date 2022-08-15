FROM python:3.9.5

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r  requirements.txt

EXPOSE 8080

WORKDIR /app
COPY app.py .
COPY column_metadata.csv .
CMD streamlit run app.py\
    --browser.serverAddress="0.0.0.0" \
    --server.port="8080"