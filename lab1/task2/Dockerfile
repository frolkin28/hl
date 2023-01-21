FROM node:18

WORKDIR /work

COPY index.html /work/

COPY package*.json /work/

RUN npm install

ENTRYPOINT [ "npm", "run", "dev" ]
