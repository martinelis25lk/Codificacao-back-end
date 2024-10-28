# Teste-de-Codifica-o-de-Desenvolvedor-Back-End
 Um pequeno projeto backend utilizando fastapi e postgres.


Lu Estilo API - FastAPI
Descrição do Problema
A Lu Estilo é uma empresa de confecção que busca novas oportunidades de negócio. Entretanto, o time comercial da empresa atualmente não possui uma ferramenta que facilite a criação de novos canais de vendas.

Solução
Para apoiar o time comercial, desenvolvemos uma API RESTful utilizando FastAPI. Esta API fornece dados e funcionalidades que facilitam a comunicação entre o time comercial, clientes e a empresa. A API será consumida por uma interface Front-End, desenvolvida por outro time.

Requisitos do Projeto
1. Linguagens e Estruturas
Python
FastAPI
Pytest (para testes)
2. Endpoints
a. Autenticação
POST /auth/login: Autenticação de usuário.
POST /auth/register: Registro de novo usuário.
POST /auth/refresh-token: Refresh de token JWT.
b. Clientes
GET /clients: Listar todos os clientes, com suporte a paginação e filtro por nome e email.
POST /clients: Criar um novo cliente, validando email e CPF únicos.
GET /clients/{id}: Obter informações de um cliente específico.
PUT /clients/{id}: Atualizar informações de um cliente específico.
DELETE /clients/{id}: Excluir um cliente.
c. Produtos
GET /products: Listar todos os produtos, com suporte a paginação e filtros por categoria, preço e disponibilidade.
POST /products: Criar um novo produto com atributos como descrição, valor de venda, código de barras, seção, estoque inicial, data de validade (quando aplicável), e imagens.
GET /products/{id}: Obter informações de um produto específico.
PUT /products/{id}: Atualizar informações de um produto específico.
DELETE /products/{id}: Excluir um produto.
d. Pedidos
GET /orders: Listar todos os pedidos, com filtros por período, seção dos produtos, id_pedido, status do pedido e cliente.
POST /orders: Criar um novo pedido contendo múltiplos produtos, validando estoque disponível.
GET /orders/{id}: Obter informações de um pedido específico.
PUT /orders/{id}: Atualizar informações de um pedido específico, incluindo status do pedido.
DELETE /orders/{id}: Excluir um pedido.
3. Autenticação e Autorização
JWT: Utilizado para autenticação.
Proteção de Rotas: Apenas usuários autenticados podem acessar as rotas de clientes, produtos e pedidos.
Níveis de Acesso: Admin e usuário regular, com restrições específicas para cada nível.
4. Validação e Tratamento de Erros
Validações: Implementadas em todos os endpoints.
Respostas de Erro: Informativas e em padrão consistente.
Monitoramento de Erros: Erros críticos registrados em um sistema de monitoramento (ex. Sentry).
5. Banco de Dados
PostgreSQL: Utilizado como banco de dados relacional.
Migrações: Facilitam a configuração do ambiente.
Índices: Otimizam a performance das consultas.
6. Documentação da API
Swagger: Documentação automática gerada pelo FastAPI.
Exemplos de Requisições e Respostas: Disponíveis para cada endpoint.
Descrição Detalhada: Inclui regras de negócio e casos de uso para cada endpoint.
7. Testes
Testes Unitários e de Integração: Implementados para garantir qualidade.
Pytest: Ferramenta utilizada para execução dos testes.
