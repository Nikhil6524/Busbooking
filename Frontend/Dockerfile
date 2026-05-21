FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

ARG VITE_BUSINESS_BASE=http://127.0.0.1:8000
ARG VITE_AUTH_BASE=http://127.0.0.1:8001
ENV VITE_BUSINESS_BASE=${VITE_BUSINESS_BASE}
ENV VITE_AUTH_BASE=${VITE_AUTH_BASE}

RUN npm run build

FROM nginx:1.27-alpine AS runtime

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]