FROM python:alpine AS BUILD 

RUN apk add --no-cache  python3-dev g++ musl-dev linux-headers
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt


FROM python:alpine AS DEPLOY 
COPY --from=BUILD /opt/venv /opt/venv

WORKDIR /app
COPY app.py entrypoint.sh /app/

EXPOSE 8000 

ENV PATH="/opt/venv/bin:$PATH"
#RUN chmod 755 /app/entrypoint.sh 

ENTRYPOINT [ "/app/entrypoint.sh" ]