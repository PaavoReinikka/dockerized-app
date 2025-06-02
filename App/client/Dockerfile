FROM denoland/deno:alpine-2.0.2

WORKDIR /app

COPY package.json .

RUN DENO_FUTURE=1 deno install

COPY . .

CMD [ "run", "dev", "--host" ]
