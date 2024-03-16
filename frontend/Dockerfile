FROM node:21-slim AS builder
WORKDIR /app
COPY package*.json .
RUN npm clean-install
COPY . .
COPY svelte.config.prod.js svelte.config.js
RUN npm run build

FROM node:21-slim
WORKDIR /app
COPY --from=builder /app/build build
COPY --from=builder /app/node_modules node_modules
COPY package.json .
EXPOSE 3000
ENV NODE_ENV=production
CMD [ "node", "build" ]
