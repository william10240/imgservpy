FROM python:3.5-alpine

LABEL maintainer="williamyan1024@gmail.com"

RUN pip install --no-cache-dir --upgrade --ignore-installed \
	aiohttp==3.5.1 \
    async-timeout==3.0.1 \
    attrs==18.2.0 \
    chardet==3.0.4 \
    idna==2.8 \
    multidict==4.5.2 \
    redis==3.0.1 \
    yarl==1.3.0

EXPOSE 80

CMD ["python3"]

