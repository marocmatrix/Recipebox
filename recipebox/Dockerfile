ARG BUILD_FROM
FROM ${BUILD_FROM}

ENV LANG=C.UTF-8 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

# System deps (Pillow needs jpeg/zlib; build tools for any wheels)
RUN apk add --no-cache \
    jpeg-dev zlib-dev libjpeg \
    && apk add --no-cache --virtual .build-deps gcc musl-dev python3-dev

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt \
    && apk del .build-deps

COPY app /app/app
RUN mkdir -p /app/app/static
COPY run.sh /run.sh
RUN chmod a+x /run.sh

EXPOSE 8099
CMD [ "/run.sh" ]
