# This needs to be run from the root directory as you want to call files from src/static
# to do so use this build command: 
# lea

FROM nginx:1.19.0-alpine

COPY Infrastructure/nginx/default.conf ./etc/nginx/conf.d/default.conf
RUN mkdir /tmp/nginx


EXPOSE 80