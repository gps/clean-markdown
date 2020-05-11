FROM nikolaik/python-nodejs

WORKDIR /opt/clean_markdown

COPY entrypoint.sh /entrypoint.sh
COPY requirements.txt /opt/clean_markdown/requirements.txt
COPY clean_markdown.py /opt/clean_markdown/clean_markdown.py
COPY package.json /opt/clean_markdown/package.json
COPY package-lock.json /opt/clean_markdown/package-lock.json

# NPM needs this
ENV CI=true

RUN chmod +x /entrypoint.sh && \
    pip3 install -r requirements.txt && \
    npm install

ENTRYPOINT ["/entrypoint.sh"]
