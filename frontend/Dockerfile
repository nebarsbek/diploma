FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173
# Запускаем dev-сервер с флагом --host, чтобы он был доступен снаружи контейнера
CMD ["npm", "run", "dev", "--", "--host"]
