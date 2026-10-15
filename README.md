# Trabalho Docker — WordPress, Nginx e MySQL

Projeto configurado, executado e testado localmente em Mac Apple Silicon com código, dados e VM dedicada no SSD externo. Esta publicação é um repositório independente, com histórico novo, a partir dos arquivos do projeto funcional. Não é um fork.

A arquitetura segue o [enunciado acadêmico](https://docs.google.com/document/d/1QbbGhd3xa76m16SvdwppHIxoj3QuCgFfIuFDh97gY8A/edit) e utiliza como referência [AmiltonRocha/Trabalho-Docker](https://github.com/AmiltonRocha/Trabalho-Docker), revisão c50b772279962485fd8faecec776472f8468e7fc. A configuração foi adaptada para o ambiente Mac/SSD; não se reivindica autoria exclusiva das ideias ou configurações de referência.

## Arquitetura e requisitos

Navegador → Nginx → wordpress1, wordpress2 ou wordpress3 → MySQL.

São exatamente cinco serviços, com as imagens exigidas:

- mysql:5.7
- wordpress:5.4.2-php7.2-apache, em três serviços
- nginx:1.19.0

Os três WordPress usam o mesmo banco e compartilham `html/` em `/var/www/html`. Nginx monta a mesma pasta em `/usr/share/nginx/html`, somente para leitura. MySQL persiste em `dados/mysql/`. Apenas Nginx publica `127.0.0.1:8080`; WordPress e MySQL não possuem portas publicadas no host. A alternância de `X-Upstream` demonstra o balanceamento.

## Arquivos

| Arquivo | Função |
|---|---|
| docker-compose.yml | Cinco serviços, persistência, redes e healthchecks |
| nginx.conf | Round-robin entre os três WordPress e cabeçalho X-Upstream |
| iniciar-wordpress.sh | Inicialização adaptada ao VirtioFS/APFS, usando o entrypoint oficial |
| .env.example | Modelo sem credenciais reais |
| documentacao/RELATORIO.pdf | Relatório com screenshots reais incorporadas |
| documentacao/evidencias/ | Resultados observados e imagens desktop/mobile |
| documentacao/ADAPTACOES.md | Diferenças justificadas em relação à referência |

Nome e turma devem ser preenchidos pelo aluno no relatório.

## Preparar e iniciar uma cópia nova

Requisitos: Docker ativo, Compose disponível e esta pasta compartilhada com o Docker. No Mac, escolha uma pasta no SSD antes de clonar. O repositório não instala nem reconfigura o Docker ou o Colima.

```sh
mkdir -p html dados/mysql
cp .env.example .env
```

Edite `.env`: substitua os dois valores de senha por senhas exclusivas do laboratório; ajuste `LOCAL_UID` e `LOCAL_GID` para os resultados de `id -u` e `id -g` do host. No Mac testado foram usados 501:20. Nunca publique `.env`.

```sh
docker-compose config --quiet
docker-compose pull
docker-compose up -d
docker-compose ps
```

Se sua instalação utiliza o plugin integrado, use `docker compose` no lugar de `docker-compose`. Aguarde MySQL e os três WordPress saudáveis e Nginx ativo. Abra **http://127.0.0.1:8080/** e conclua a instalação local do WordPress. Uma cópia nova não contém o banco, as contas ou o site já instalado no SSD.

O projeto se chama `trabalho-docker-academico` e usa 8080. Não inicie simultaneamente duas cópias com o mesmo nome de projeto no mesmo Docker. Se a porta estiver ocupada, não pare processos alheios. Caso escolha outra porta, ajuste também a URL de um WordPress já instalado.

## Testar

```sh
docker-compose ps
docker-compose exec -T nginx nginx -t
for i in 1 2 3 4 5 6 7 8 9; do curl -sSI http://127.0.0.1:8080/; done
curl -sSL -o /dev/null -w 'HTTP %{http_code}\n' http://127.0.0.1:8080/
```

O cabeçalho `X-Upstream` deve assumir três endereços. Compare com os IPs internos dos três serviços WordPress; esses IPs podem mudar ao recriar redes. Em uma instalação nova, HTTP 200 na tela de instalação não significa que o assistente já foi concluído. As evidências incluídas correspondem ao site instalado e testado em 14/10/2026, com revalidação em 15/10/2026.

## Parar e retomar

```sh
docker-compose stop
docker-compose up -d
```

`docker-compose down` remove contêineres e redes deste projeto e preserva os diretórios de dados. Não apague `html/` ou `dados/mysql/` para apenas parar. Antes de ejetar o SSD, pare também o perfil/VM Docker dedicado que o utiliza. O ambiente local preparado possui instruções próprias de seleção e parada do perfil Colima `t`, preservadas no SSD.

## O que foi verificado

Cinco contêineres ativos; MySQL e os três WordPress saudáveis; `nginx -t` válido; HTTP 200; três `X-Upstream` correspondentes às três instâncias; mesmo hash HTML nos três servidores; banco comum com 12 tabelas; parada/retomada aprovadas; escuta apenas em loopback; nenhum dos cinco contêineres privilegiado. As imagens são capturas reais de desktop e viewport mobile emulado, não um teste em iPhone físico.

## Privacidade e referências

Credenciais reais, .env, wp-config.php, WordPress instalado, banco, dumps, backups, caches, cookies, tokens, perfis de navegador e discos de VM ficam fora do Git. Os dados e o backup do laboratório permanecem somente no SSD. Nenhum script do repositório de referência foi publicado como implementação deste projeto.

As tags antigas foram mantidas por exigência acadêmica. O acesso do laboratório é local. Executáveis Docker/Compose/Colima, alguns caches, contextos e temporários continuam no Mac; código, dados persistentes e discos do perfil dedicado ficam no SSD.
