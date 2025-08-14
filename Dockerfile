FROM python:3.13.5-alpine3.22 AS backend
WORKDIR /app
COPY ./backend /app
EXPOSE 8000
RUN pip install --no-cache-dir pandas django django-cors-headers xlsxwriter matplotlib numpy Pillow

RUN adduser -S django && addgroup -S django
RUN chown -R django:django /app && chmod 755 -R /app
USER django
CMD ["python","manage.py","runserver","0.0.0.0:8000"] 
#sinon écoute uniquement sur la loopback
FROM nginx:1.29.0-alpine AS server

WORKDIR /app/nginx
COPY default.conf /etc/nginx/conf.d/default.conf
#donner les permissions à l'utilisateur du conteneur (sinon erreur de permissions au démarrage et pour le fonctionnement)
RUN chown -R nginx:nginx /app/nginx && \
    chown -R nginx:nginx /etc/nginx && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /var/run && \
    chmod 777 /var/run
CMD ["nginx", "-g", "daemon off;"]


FROM node:23-alpine3.20 AS react
WORKDIR /app
COPY ./frontend /app

EXPOSE 3000
RUN adduser -S react && addgroup -S react
RUN chown -R react /app && chmod -R 755 /app
RUN chown -R react:react /home/react
USER react


RUN npm install

RUN npm run build
CMD ["npx", "serve", "build", "-p", "3000"] 