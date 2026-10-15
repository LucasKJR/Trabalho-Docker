# Adaptações do trabalho executado no Mac/SSD

A atividade e as tags seguem o Google Docs e a pasta trabalho2 de AmiltonRocha/Trabalho-Docker, revisão c50b772279962485fd8faecec776472f8468e7fc. Esta implementação foi configurada e testada no computador; não é uma cópia literal nem reivindica autoria exclusiva das referências. Não foi encontrada uma licença no repositório consultado, e nenhuma licença nova foi atribuída ao conteúdo de referência.

| Diferença | Justificativa |
|---|---|
| MySQL com platform linux/amd64 | A tag 5.7 não apresenta ARM64 no manifesto inspecionado; executa pela emulação do ambiente Docker |
| Inicialização WordPress em /tmp antes de copiar ao SSD | O sed 4.7 da imagem falhou no VirtioFS/APFS; o script usa o entrypoint oficial no filesystem Linux e copia os arquivos prontos |
| UID/GID local no WordPress | Compatibilidade de escrita no diretório compartilhado, sem alterar permissões do Mac |
| Porta 127.0.0.1:8080:80 | Isolamento local e conveniência; difere da porta 80 do host no exemplo. Nginx continua em 80 dentro do contêiner |
| Senhas via .env | Evita publicar senhas fixas ou reais; mantém banco e usuário comuns |
| MySQL em ./dados/mysql | Mantém os dados persistentes acessíveis no SSD em vez de volume nomeado dentro da VM |
| Redes web e banco, banco interna | Isolamento adicional; Nginx não participa da rede MySQL |
| Nomes gerados por projeto | Evita colisões com outros projetos; serviços mantêm nomes mysql/wordpress1/wordpress2/wordpress3/nginx |
| Healthchecks e início sequencial | Espera pelo banco e evita inicialização concorrente da pasta compartilhada |
| Sem restart automático | Evita iniciar ao boot com SSD desconectado |
| Nginx usa $http_host | Preserva a porta 8080 nos redirecionamentos |
| X-Upstream com always e X-Forwarded-Proto | Facilita diagnóstico e encaminhamento pelo proxy |
| Âncora YAML e name no Compose | Organização da configuração para o Compose atual |

As cinco imagens/serviços, o banco comum, os caminhos compartilhados, o balanceamento e a ausência de portas publicadas no WordPress/MySQL foram mantidos. Os exemplos opcionais da raiz do repositório de referência, incluindo extras com socket Docker, não integram este projeto.

O código publicado é o Compose/Nginx/script presente na pasta funcional do SSD. A pasta de publicação não inclui histórico ou arquivos .git do fork anterior. A publicação tem um commit inicial novo, sem pais. Relatórios e imagens registram os testes efetivamente realizados, sem executar novamente a instalação durante o upload.

Referências:

- https://docs.google.com/document/d/1QbbGhd3xa76m16SvdwppHIxoj3QuCgFfIuFDh97gY8A/edit
- https://github.com/AmiltonRocha/Trabalho-Docker/tree/main
