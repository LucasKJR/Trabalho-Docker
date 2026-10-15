# WordPress com múltiplas instâncias, Nginx e Docker Compose

Aluno e turma: preencher antes da entrega.

Data dos testes: 14 de outubro de 2026.

## Objetivo

Executar três instâncias WordPress conectadas ao mesmo MySQL, utilizando Nginx como balanceador de carga. Verificar a distribuição das requisições por meio do cabeçalho HTTP X-Upstream.

## Arquitetura

Navegador → 127.0.0.1:8080 → Nginx → WordPress 1, 2 ou 3 → MySQL.

O Compose define cinco serviços. Nginx utiliza round-robin padrão e o DNS do Docker. Os três WordPress compartilham o banco wordpress e o diretório html em /var/www/html. Nginx monta o mesmo diretório em /usr/share/nginx/html, somente para leitura. O banco persiste em dados/mysql. Esses dados e o perfil dedicado ficam no SSD externo.

## Atendimento ao enunciado

| Requisito | Implementação |
|---|---|
| Cinco contêineres | mysql, wordpress1, wordpress2, wordpress3 e nginx |
| Imagens exigidas | mysql:5.7, wordpress:5.4.2-php7.2-apache, nginx:1.19.0 |
| Banco comum | Mesmo host mysql:3306, banco e usuário nos três WordPress |
| Host acessa somente Nginx | Apenas Nginx publica 127.0.0.1:8080 |
| Compartilhamento | html comum aos três WordPress e Nginx |
| Balanceamento verificável | upstream com três serviços e cabeçalho X-Upstream |

## Ambiente e adaptações

Mac Apple Silicon ARM64 com macOS 26.6.2; Docker CLI 29.6.2, Engine 29.5.2, Compose independente 5.3.1 e Colima 0.10.3. SSD APFS de 1 TB. O perfil dedicado t utiliza 2 CPUs e 3 GiB de RAM e compartilha somente a pasta do trabalho. O perfil anterior continua ativo e selecionado globalmente.

MySQL 5.7 executa em AMD64 emulado; WordPress e Nginx utilizam ARM64. A imagem antiga utiliza sed 4.7, que falhou ao criar temporários no VirtioFS/APFS. Um script curto incluído na entrega executa o entrypoint oficial primeiro no filesystem Linux do contêiner e copia os arquivos prontos ao SSD. Isso preserva as imagens exigidas e evita alterar permissões do Mac. O script externo do repositório não foi executado.

## Procedimento

Foram lidos o Google Docs e os arquivos relevantes do GitHub. Após inspeção do SSD, Docker e portas, foi criado o perfil separado autorizado com discos no SSD. As imagens oficiais foram baixadas, o Compose validado e os serviços iniciados em sequência. O WordPress foi instalado localmente com dados fictícios, senha exclusiva e envio de email desativado. Sua URL foi definida como http://127.0.0.1:8080.

## Resultados observados

- Cinco contêineres ativos; MySQL e três WordPress saudáveis.
- nginx -t: configuração válida.
- Página inicial do site instalado: HTTP 200.
- Seis requisições GET produziram o mesmo SHA-256 do HTML entre os três servidores, confirmando conteúdo idêntico.
- Nove requisições HEAD apresentaram X-Upstream 172.18.0.2:80, 172.18.0.3:80 e 172.18.0.4:80, correspondentes aos WordPress na rede web.
- MySQL: banco wordpress com as 12 tabelas da instalação.
- Somente Nginx publica porta; escuta real do Mac conferida em 127.0.0.1:8080.
- Inspeção dos cinco serviços: privileged=false; montagens restritas aos arquivos e dados deste trabalho.
- Parar e retomar foi submetido a teste; o registro completo está em evidencias/parar-retomar.txt.

Os testes podem ser repetidos com source ./ambiente.sh e python3 verificar.py. IPs são internos e podem mudar ao recriar redes; compare com a inspeção dos contêineres da execução atual.

## Evidências e limitações

Acompanham a entrega: listagem de contêineres, configuração validada, cabeçalhos HTTP, consulta ao banco, inspeção de portas/montagens/redes, logs e HTML recebido do site. Foram incluídas screenshots reais de desktop (1440 × 1405) e viewport mobile (390 × 1324), obtidas com Chromium headless em perfil novo e conferidas visualmente. A captura de rede do navegador registrou nove respostas HTTP 200 e os três X-Upstream. Nenhum login foi usado; cookies, tokens e cabeçalhos de autenticação não foram exportados. O teste mobile utiliza viewport emulado, não um iPhone físico.

Executáveis Docker/Compose/Colima, caches, contextos e temporários de sistema continuam no Mac. Arquivos do projeto, dados persistentes e discos do perfil dedicado ficam no SSD. As tags antigas foram preservadas por exigência do enunciado; o ambiente foi limitado a acesso local para uso acadêmico.

## Capturas reais

Figura 1: página inicial no Chromium headless, largura de desktop de 1440 pixels.

Figura 2: a mesma página no viewport mobile de 390 pixels.

Ambas mostram o conteúdo padrão do WordPress instalado no laboratório. Os arquivos originais PNG estão na pasta evidencias.

## Conclusão

Os testes demonstraram três instâncias WordPress por trás do Nginx, conectadas ao mesmo MySQL. Os três valores de X-Upstream comprovaram a distribuição das requisições. Configuração, evidências verificadas e screenshots reais acompanham a entrega.

## Referências

Enunciado: https://docs.google.com/document/d/1QbbGhd3xa76m16SvdwppHIxoj3QuCgFfIuFDh97gY8A/edit

Repositório: https://github.com/AmiltonRocha/Trabalho-Docker/tree/main — revisão c50b772279962485fd8faecec776472f8468e7fc.
