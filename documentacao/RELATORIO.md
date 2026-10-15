# WordPress com balanceamento de carga em cinco contêineres

Aluno e turma: preencher.

Data da revisão: 15 de outubro de 2026.

## Objetivo

Preparar um experimento em que Nginx encaminha requisições a três instâncias WordPress que compartilham arquivos e um banco MySQL. A identificação do destino deve ser observável por X-Upstream.

## Requisitos

Exatamente cinco serviços, com mysql:5.7, wordpress:5.4.2-php7.2-apache e nginx:1.19.0. WordPress e MySQL não publicam portas no host. Os três WordPress compartilham /var/www/html e usam o mesmo banco. Nginx monta a mesma pasta em /usr/share/nginx/html.

## Arquitetura

Navegador → 127.0.0.1:8086 → Nginx → wordpress1, wordpress2 ou wordpress3 → database.

A rede de requisições conecta Nginx e WordPress. A rede interna de persistência conecta WordPress e MySQL. Os diretórios html e data/mysql são bind mounts que podem ficar no SSD. Senhas e semente de sessão são arquivos locais separados, entregues somente aos serviços que precisam deles.

## Implementação

O arquivo Compose declara cinco serviços explicitamente. Os WordPress iniciam em sequência após a prontidão das dependências. O script de inicialização copia a distribuição da imagem para a pasta de arquivos compartilhados. A configuração PHP é montada somente para leitura e lê segredos de arquivos em /run/secrets; não é necessário editar PHP com sed no SSD.

O Nginx utiliza um arquivo em conf.d, preservando a configuração principal da imagem oficial. O pool contém os três WordPress. São configurados conexões persistentes, tempos limite e o cabeçalho X-Upstream. O endpoint /saude-proxy verifica somente o proxy e não comprova comunicação com WordPress ou banco.

MySQL 5.7 utiliza linux/amd64 em Apple Silicon, com limites de memória e conexões para um laboratório pequeno. A URL de WordPress é definida por SITE_URL. Cron e atualizações automáticas ficam desabilitados nesta instância para manter as versões e o comportamento do experimento.

## Verificações realizadas

- Compose resolvido sem erro, com exatamente cinco serviços e as tags exigidas.
- Uma única publicação de porta: 127.0.0.1:8086, no Nginx.
- Ausência de publicação de portas no banco e nos WordPress.
- Rede de persistência interna e Nginx fora dessa rede.
- Senha root do MySQL não entregue aos serviços WordPress.
- Nenhum serviço configurado como privileged.
- Sintaxe shell aprovada; preparador reexecutado sem substituir segredos existentes.

Essas verificações são estáticas e de preparação. Não demonstram que os contêineres desta revisão funcionam em conjunto.

## Bloqueio e testes pendentes

O perfil Colima dedicado foi encontrado parado e a tentativa de retomada informou estado Broken, com processo existente e socket recusando conexão. Não foi forçada a parada do processo nem alterado o perfil padrão. Os dados e a implementação anterior permanecem preservados.

Ainda são necessários: php -l na versão PHP 7.2, nginx -t, início dos cinco serviços, instalação WordPress, HTTP 200, alternância de três X-Upstream, igualdade do conteúdo entre instâncias, consulta ao banco, teste de persistência após parar/retomar e screenshots reais desta revisão. Nenhuma evidência de outra configuração foi apresentada como prova do código atual.

## Conclusão provisória

A revisão passou nas verificações estruturais e de preparação. A aprovação funcional permanece pendente da recuperação do ambiente dedicado e da execução dos testes descritos. Esta conclusão registra o limite observado e não afirma funcionamento que ainda não foi comprovado.

## Referências técnicas oficiais

Docker Compose: https://docs.docker.com/reference/compose-file/services/

Secrets Compose: https://docs.docker.com/reference/compose-file/secrets/

WordPress: https://developer.wordpress.org/advanced-administration/wordpress/wp-config/

Nginx upstream: https://nginx.org/en/docs/http/ngx_http_upstream_module.html

Nginx proxy: https://nginx.org/en/docs/http/ngx_http_proxy_module.html

As imagens e distribuições mantêm seus avisos de licença e autoria. O projeto não reivindica autoria dessas dependências.
