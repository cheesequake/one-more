FROM node:21.7.3-alpine3.20

WORKDIR /app

ARG VITE_BACKEND_URL

ENV VITE_BACKEND_URL=$VITE_BACKEND_URL

COPY package*.json .

RUN npm install

RUN npm i -g serve

COPY . .

RUN npm run build

EXPOSE 3000

CMD ["serve", "-s", "dist"]