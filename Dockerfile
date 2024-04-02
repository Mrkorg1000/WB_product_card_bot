FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTONUNBUFFERED=1
WORKDIR /app
COPY . ./
# RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python3", "app.py"]