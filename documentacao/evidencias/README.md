# Evidências da execução

Esta pasta recebe provas produzidas exclusivamente com o código desta revisão. Logs e JSON ajudam a conferir os testes, mas **não substituem prints reais do terminal e da aplicação**.

## Situação atual

- Código e scripts disponíveis no repositório.
- Verificações estáticas disponíveis em validacao-estatica.json e checagem-estatica.json.
- Execução pendente: o perfil Colima dedicado t está Broken e a porta 8086 não responde.
- Não há capturas atuais de cinco contêineres ativos nem da aplicação funcionando nesta revisão.
- Não foram copiadas imagens, scripts ou resultados de outro trabalho, nem reaproveitadas provas de outra configuração como se fossem atuais.

## Produzir o registro

No Terminal configurado para o Docker deste projeto:

```sh
python3 scripts/preparar.py
python3 scripts/verificar.py --estatico
docker-compose up -d
docker-compose ps
python3 scripts/verificar.py
```

O verificador não inicia, para ou remove contêineres e não instala ferramentas. Faz nove requisições locais, confere os destinos e o conteúdo e salva checagem-runtime.json. Código de saída 2 significa bloqueio ou reprovação; somente APROVADO_RUNTIME indica que os checks descritos foram concluídos. O preparador e o verificador não são testes de carga.

## Prints reais que precisam ser entregues

Salve capturas reais, sem dados pessoais ou segredos, em capturas/:

| Nome sugerido | O que deve aparecer |
|---|---|
| 01-terminal-containers.png | Comando docker-compose ps e cinco serviços ativos; WordPress/banco saudáveis |
| 02-terminal-balanceamento.png | Requisições curl e três valores X-Upstream |
| 03-terminal-validacao.png | nginx -t, verificador aprovado e consulta ao banco sem senha visível |
| 04-aplicacao.png | Página inicial do WordPress instalado na URL local desta revisão |
| 05-navegador-cabecalhos.png | Cabeçalhos da requisição da aplicação, incluindo X-Upstream |

Comandos úteis para o print do balanceamento:

```sh
for i in 1 2 3 4 5 6 7 8 9; do curl -sSI http://127.0.0.1:8086/; done
```

Capture a janela real usada para executar os comandos. Não converta texto de log em uma imagem apresentada como print. Não fotografe senhas, .env, arquivos em segredos, cookies ou telas pessoais. No navegador, abra somente a aplicação local; não é necessário entrar no painel administrativo para comprovar a página inicial.

## Conferência antes de publicar

Confirme que os IPs dos prints coincidem com o registro da execução, que a aplicação utiliza a URL/porta documentada e que não são capturas da tela de instalação apresentadas como site pronto. Registre o estado com honestidade se algum teste falhar.

Nenhuma imagem placeholder foi criada. A ausência dos PNGs indicados significa que as capturas ainda estão pendentes.
