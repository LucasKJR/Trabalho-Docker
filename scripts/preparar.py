#!/usr/bin/env python3
"""Prepara apenas a pasta do experimento; nao instala ou inicia software."""
import os
from pathlib import Path
import secrets

raiz = Path(__file__).resolve().parent.parent
for pasta in ['html', 'data/mysql', 'segredos']:
    (raiz / pasta).mkdir(parents=True, exist_ok=True)
for nome in ['senha_root', 'senha_aplicacao', 'semente_sessao']:
    destino = raiz / 'segredos' / nome
    if not destino.exists():
        # Cria com acesso restrito desde a abertura, sem alterar arquivos existentes.
        descriptor = os.open(destino, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, 'w') as arquivo:
            arquivo.write(secrets.token_hex(32) + '\n')
config = raiz / '.env'
if not config.exists():
    config.write_text('COMPOSE_PROJECT_NAME=wordpress-experimento\n'
                      'HTTP_PORT=8086\n'
                      'LOCAL_UID=' + str(os.getuid()) + '\n'
                      'LOCAL_GID=' + str(os.getgid()) + '\n'
                      'SITE_URL=http://127.0.0.1:8086\n')
# Permite o bind mount do arquivo de configuracao em uma pasta inicialmente vazia.
placeholder = raiz / 'html/wp-config.php'
if not placeholder.exists():
    placeholder.touch()
print('Pastas e segredos locais preparados; nenhum segredo foi exibido.')
