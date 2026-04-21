📄 Documento de Requisitos do Produto (PRD)
Produto: SaaS Gestão (ERP de Gestão Comercial)
Estágio Atual: MVP (Minimum Viable Product) Concluído

1. Visão Geral do Produto
O SaaS Gestão é um sistema web integrado (ERP) desenhado para pequenas e médias empresas (PMEs). O objetivo principal é unificar a operação comercial — desde a intenção de compra até a venda no balcão — garantindo controle rigoroso de estoque, rastreabilidade financeira (auditoria) e agilidade no atendimento ao cliente.

2. Problemas a Resolver
Falta de Auditoria: Evitar compras não autorizadas e desvios de estoque.

Lentidão no Caixa: Eliminar telas complexas no momento da venda (resolvido com PDV em tela única via HTMX).

Furo de Estoque: Garantir que o custo da mercadoria vendida (CMV) e o saldo reflitam a realidade física (resolvido com motor FIFO).

Controle de Acessos: Evitar que operadores de caixa vejam informações sensíveis de custo ou modifiquem relatórios (resolvido via RBAC).

3. Perfis de Usuário (Personas) e Permissões (RBAC)
O sistema adere estritamente à Segregação de Funções (SoD).

👑 Dono / Admin: Acesso irrestrito. Único com permissão para importar/exportar dados sensíveis (CSV) e deletar registros definitivos.

⚖️ Gerente / Supervisor: Aprova ou rejeita Solicitações de Compra. Visualiza o desempenho da loja.

📦 Estoquista: Realiza Solicitações de Compra internas. Faz o Recebimento físico das notas. Analisa o extrato de movimentações.

🤝 Comprador: Transforma solicitações aprovadas em Pedidos de Compra oficiais, definindo valores e fornecedores.

🛒 Operador de Caixa: Foco total na tela de PDV. Visualiza catálogo de produtos e clientes, mas não acessa custos, suprimentos ou gestão.

4. Escopo Funcional (Módulos)
4.1. Core & Segurança
Soft Delete: Registros nunca são apagados do banco, apenas inativados (is_active=False), mantendo a integridade do histórico.

Menu Dinâmico: A interface (Sidebar) se adapta automaticamente às permissões do usuário logado.

4.2. Módulo de Cadastros (MDM - Master Data Management)
Produtos: Gestão de SKUs, Categorias, Custos (Médio e Última Compra) e travas de Estoque Mínimo.

Clientes & Fornecedores: Cadastros validados (impedindo CPF/CNPJ duplicados, mesmo de registros inativos).

4.3. Módulo de Suprimentos (Workflow Auditável)
1. Solicitação: Estoque pede quantidade (sem preço).

2. Aprovação: Gerência autoriza a despesa.

3. Pedido (PO): Compras negocia com fornecedor e gera o pedido anexado à solicitação original (Fio Condutor).

4. Recebimento: Estoque dá entrada na mercadoria.

Motor FIFO: O sistema controla os lotes por data de entrada, consumindo sempre o produto mais antigo primeiro.

4.4. Módulo de Vendas (Frente de Caixa - PDV)
Experiência SPA (Single Page Application): Tela reativa sem recarregamentos (powered by HTMX).

Validação de Saldo: Bloqueio automático de vendas de produtos sem estoque.

Automação Contábil: Ao finalizar a venda, o sistema abate o estoque (FIFO) e fotografa o CMV exato do momento para cálculo preciso de Lucro Bruto.

5. Requisitos Não Funcionais (Tecnologia)
Backend: Python 3 + Django 5+ (Padrão MTV - Model, Template, View).

Frontend: HTML5, Bootstrap 5 (UI Responsiva), JavaScript / HTMX (Reatividade).

Banco de Dados: SQLite (Desenvolvimento). Pronto para migração para PostgreSQL em Produção.

Segurança: Proteção CSRF em todos os formulários, autenticação baseada em sessão, decoradores @login_required e @permission_required blindando todas as rotas.

6. Roadmap (Próximos Passos Imediatos)
Dashboard Executivo: Implementação de gráficos de Faturamento e Alertas de Estoque (Chart.js).

Impressão de PDV: Geração de Cupom Não-Fiscal formato bobina (80mm) após a conclusão da venda.

Relatórios Básicos: Exportação de PDF para fechamento de caixa diário.