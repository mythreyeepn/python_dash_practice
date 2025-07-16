# Expose app port
EXPOSE 3002

RUN useradd -u 5000 -m iamuser

# Use entrypoint to fix permissions + build + run
USER 5000
ENTRYPOINT [ "sh", "-c", "mkdir -p /usr/app/build && chown -R 5000 /usr/app && echo \"Building React app with theme=$REACT_APP_THEME\" && cd /usr/app && npm run build && node server" ]
