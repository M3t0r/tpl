# builder
FROM python:3-alpine AS zipper

RUN apk update && apk add make git

COPY ./ /app
RUN make -C /app dist/tpl

# final image
FROM python:3-alpine

LABEL maintainer="Simon Brüggen <tpl@m3t0r.de>"

COPY --from=zipper /app/dist/tpl /usr/bin/tpl

ENTRYPOINT ["tpl"]

CMD ["--environment", "-","-"]
