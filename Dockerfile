FROM python:3-alpine

COPY dist/tpl /usr/bin/tpl
RUN ln -s /usr/bin/tpl /entrypoint

CMD ["tpl", "--environment", "-","-"]
