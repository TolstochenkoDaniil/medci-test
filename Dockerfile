FROM python:3.9
ENV PYTHONBUFFERED 1

WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt /app
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && rm -rf /root/.cache

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--timeout", "150", "--log-level", "debug", "wsgi:app"]