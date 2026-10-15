#!/bin/bash
set -euo pipefail

# O sed 4.7 desta imagem falha ao criar temporarios mode 000 no VirtioFS/APFS.
# Inicializa com o entrypoint oficial no filesystem Linux e copia para o SSD.
if [ ! -s /var/www/html/wp-config.php ]; then
    mkdir -p /tmp/wordpress-inicializacao
    cd /tmp/wordpress-inicializacao
    /usr/local/bin/docker-entrypoint.sh apache2ctl -t
    cp -R . /var/www/html/
fi
cd /var/www/html
exec apache2-foreground
