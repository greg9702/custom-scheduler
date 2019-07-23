FROM archlinux/base

WORKDIR /app
RUN pacman -Sy --noconfirm stress
COPY . /app

CMD /bin/sh init.sh
