FROM node:14

WORKDIR /app
COPY public/ public/
COPY src/ src/
COPY package.json package.json
COPY package-lock.json package-lock.json
RUN npm install
EXPOSE 3000
CMD ["npm", "start"]