FROM node:16.17-slim

WORKDIR /app
# add `/app/node_modules/.bin` to $PATH

ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies

COPY package.json ./


COPY package-lock.json ./

RUN npm install

# add app

COPY . ./

EXPOSE 3000

CMD ["npm", "start"]