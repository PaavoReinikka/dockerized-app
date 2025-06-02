FROM mcr.microsoft.com/playwright:v1.48.1-jammy

WORKDIR /app

COPY package*.json .
COPY *config.js .

RUN npm install
RUN npx playwright install chromium

COPY . .

CMD [ "npc", "playwright", "test" ]
