# WordPress com balanceamento de carga

Experimento de cinco contêineres: um Nginx distribui requisições entre três instâncias WordPress, conectadas a um único MySQL. Código e diretórios persistentes podem ser mantidos em uma pasta dedicada no SSD.

**Estado desta revisão:** a configuração Compose e a preparação dos arquivos passaram nas verificações estáticas. Os testes de execução, Nginx e PHP ainda estão pendentes: o perfil Docker dedicado apresentou falha de comunicação. Não se apresenta a revisão como funcionalmente aprovada.

## Arquitetura

Navegador → 127.0.0.1:8086 → Nginx → wordpress1 / wordpress2 / wordpress3 → database.

As imagens são mysql:5.7, wordpress:5.4.2-php7.2-apache e nginx:1.19.0. Somente Nginx publica porta no host, restrita a loopback. Os três WordPress usam a mesma pasta html em /var/www/html; Nginx monta essa pasta em /usr/share/nginx/html, somente para leitura. O MySQL persiste em data/mysql.

## Organização

| Caminho | Uso |
|---|---|
| docker-compose.yml | Cinco serviços e suas conexões |
| config/balanceamento.conf | Pool HTTP, proxy e identificação do destino |
| config/wordpress.php | Configuração de banco e sessões, sem senhas embutidas |
| scripts/abrir-wordpress.sh | Copia os arquivos da imagem e inicia Apache |
| scripts/preparar.py | Cria diretórios e segredos locais, preservando os existentes |
| scripts/verificar.py | Registra os checks sem iniciar/parar containers; nao gera imagens |
| segredos/ | Senhas e semente de sessão; excluídos do Git |
| html/ e data/mysql/ | Dados de execução; excluídos do Git |
| documentacao/ | Relatório e evidências específicas desta revisão |

## Preparação

Use uma pasta compartilhada com o Docker. No SSD, preserve uma cópia do projeto e seus dados antes de mudanças. Este projeto não instala Docker, não altera permissões do Mac e não reconfigura o Colima.

```sh
python3 scripts/preparar.py
docker-compose config --quiet
```

O preparador cria três arquivos privados em segredos e uma configuração .env com UID/GID do usuário e URL local. Não mostra nem publica as senhas. A reexecução não troca os segredos existentes. Os arquivos privados precisam continuar disponíveis enquanto os contêineres estiverem em uso.

## Execução prevista — ainda requer validação desta revisão

Com o Docker acessível e 8086 livre:

```sh
docker-compose up -d
docker-compose ps
```

Em instalações com plugin integrado, use docker compose. Aguarde MySQL e os três WordPress saudáveis; abra http://127.0.0.1:8086 e conclua a instalação local. Não execute este projeto com o nome de outro projeto existente. A porta 8086 e o nome wordpress-experimento distinguem o experimento de outras aplicações.

```sh
docker-compose exec -T nginx nginx -t
for i in 1 2 3 4 5 6 7 8 9; do curl -sSI http://127.0.0.1:8086/; done
curl -sSL -o /dev/null -w 'HTTP %{http_code}\n' http://127.0.0.1:8086/
```

O resultado esperado é HTTP 200 após a instalação, com três valores de X-Upstream correspondentes aos WordPress. /saude-proxy confirma apenas que Nginx responde; não substitui o teste da aplicação. Compare também o conteúdo recebido dos três destinos e verifique que banco/WordPress não publicam portas.

## Parar, retomar e persistir

```sh
docker-compose stop
docker-compose up -d
```

Os diretórios html, data/mysql e segredos devem ser preservados. Antes de ejetar o SSD, pare este projeto e a VM dedicada que o utiliza. Nunca remova dados ou segredos para apenas parar. Mudanças de HTTP_PORT exigem atualizar SITE_URL no .env e reiniciar a configuração correspondente.

## Decisões do experimento

MySQL 5.7 usa linux/amd64 no Apple Silicon. A configuração WordPress é fornecida como arquivo somente leitura, e suas senhas são lidas de Compose secrets. A inicialização não edita PHP com sed no compartilhamento APFS. O Apache recebe UID/GID local. O arquivo padrão de Nginx da imagem é mantido; apenas um arquivo em conf.d define o experimento. Não há serviços adicionais ou contêineres privilegiados.

As versões foram fixadas para a atividade. Atualizações automáticas e cron do WordPress ficam desabilitados somente nesta instância local para preservar o experimento. O banco tem limites de conexão e buffer apropriados a um laboratório pequeno. As licenças e os avisos das imagens permanecem intactos; o repositório não distribui o código dessas dependências.

Referências técnicas oficiais em documentacao/ADAPTACOES.md. As evidências registram os limites atuais, sem reaproveitar resultados de outra configuração como prova desta revisão.

## Entrega: codigo, scripts e prints

O roteiro de evidencias esta em [documentacao/evidencias/README.md](documentacao/evidencias/README.md). Ele lista os prints reais do terminal, aplicacao e cabecalhos necessarios para completar a entrega. A pasta capturas ainda nao contem esses prints: a execucao da revisao esta bloqueada. Nenhum resultado alheio ou imagem gerada a partir de texto sera apresentado como prova de funcionamento.
