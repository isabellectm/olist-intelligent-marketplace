# Priorização de problemas

Critério simples para priorização: **evidência nos dados** × **impacto no negócio** × **viabilidade de um agente de IA** (instrução + pessoa na ponta).

Os percentuais abaixo são leitura de negócio (quanto dói, para quem, o que fazer), não resultado de modelo.

Escala 1 (baixo) a 5 (alto).

## Ranking

1. **Atraso na entrega tem grande impacto na satisfação** — evidência 5, impacto 5, viabilidade 5  
   Só 6,8% dos pedidos entregues chegam depois da data prometida, mas a nota média cai de **4,29 para 2,57**. Entre os atrasados, **54%** dão nota 1 ou 2 (no prazo, isso é 9%). O atraso é maior no Nordeste e no RJ (CE 15%, BA 14%, RJ 13%) do que em SP (6%).  
   **Vira agente:** Acompanhamento de Prazo.

2. **Reviews ruins não viram ação** — evidência 5, impacto 4, viabilidade 5  
   14,7% das avaliações são nota 1 ou 2. 41% têm texto. Cancelados saem com nota média 1,81. Hoje isso é leitura humana, lenta e desigual.  
   **Vira agente:** Inteligência de Avaliações.

3. **A Olist quase não tem segunda compra** — evidência 5, impacto 5, viabilidade 4  
   96,9% dos clientes únicos fizeram **um único pedido**. O máximo observado é 17. Parte disso é compra pontual, mas o mix inclui categorias de reposição (ex.: beleza). Marketplace com ~3% de recompra é problema de relacionamento e de critério de contato.  
   **Vira agente:** Relacionamento e Recompra.

4. **Exceções operacionais (cancelado, indisponível, travado)** — evidência 4, impacto 3, viabilidade 4  
   Volume pequeno (~1,2% cancelado + indisponível; há ainda shipped/processing), mas a experiência é péssima e gera ruído no atendimento. Bom como quarto agente, de apoio.  
   **Vira agente:** Exceções Operacionais.

5. **Frete alto no ticket baixo** — evidência 4, impacto 3, viabilidade 3  
   Frete equivale a 16,5% do GMV. Ticket mediano ~R$ 87. Frete alto sozinho não impacta tanto a nota quanto o atraso; como insumo e não como agente.

6. **Concentração de categorias e cauda de vendedores** — evidência 3, impacto 3, viabilidade 2  
   Top 10 categorias = 63% do GMV; top 50 vendedores = 33%. Útil para estratégia comercial, mas com poucos insumos para agente.

## Decisão desta fase

Seguem **quatro agentes**, nesta ordem de prioridade: Prazo, Avaliações, Recompra e Exceções. Frete e mix de oferta entram como contexto do marketplace.
