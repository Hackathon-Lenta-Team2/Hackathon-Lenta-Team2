FROM node:18.16-alpine as development

WORKDIR app

COPY package*.json .

RUN npm install

COPY . .

RUN npm run build

CMD sh -c "npm run dev"
