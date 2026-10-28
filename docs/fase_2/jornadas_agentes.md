# Jornadas de funcionamento — Fase 2

Três fluxos simples. Em cada um: **gatilho**, **entrada**, **decisão**, **ação**, **humano**, **saída**. Pessoa no loop em toda execução que fale com cliente ou mexa em dinheiro.

Figuras usadas no relatório: [figuras/jornada_experiencia_entrega.png](figuras/jornada_experiencia_entrega.png), [figuras/jornada_avaliacoes.png](figuras/jornada_avaliacoes.png), [figuras/jornada_recompra.png](figuras/jornada_recompra.png).

## 1. Experiência da Entrega

Gatilho: pedido muda de status, o prazo se aproxima, ou CX encaminha review de atraso/cancelamento.

```mermaid
flowchart TD
  gatilho[Gatilho: status do pedido ou prazo]
  dados[Entrada: pedido datas UF status valor]
  agente[Agente classifica a trilha]
  prazo{Trilha prazo ou excecao?}
  risco[Decide risco: baixo medio alto]
  acaoPrazo{Uma acao}
  mon[Monitorar]
  avis[Avisar o cliente]
  cobr[Cobrar seller ou transportadora]
  tipo[Nomeia a excecao e a prioridade]
  passo[Um proximo passo humano]
  humano[Pessoa confirma e executa]
  saida[Saida: ficha de prazo ou de fila]
  rec[Handoff para Recompra so se boa entrega]

  gatilho --> dados --> agente --> prazo
  prazo -->|prazo| risco --> acaoPrazo
  acaoPrazo --> mon --> humano
  acaoPrazo --> avis --> humano
  acaoPrazo --> cobr --> humano
  prazo -->|excecao| tipo --> passo --> humano
  humano --> saida
  saida --> rec
```

Humano: logística/ops autoriza o aviso e qualquer movimento financeiro. O agente **nunca** estorna.

## 2. Inteligência de Avaliações

Gatilho: cliente publica avaliação (nota, com ou sem texto).

```mermaid
flowchart TD
  gatilho[Gatilho: review publicado]
  dados[Entrada: pedido nota texto atraso categoria]
  agente[Agente le nota e comentario]
  tema[Classifica um tema]
  urg[Define urgencia]
  critico{Caso critico?}
  rascunho[Rascunha resposta]
  humano[CX revisa e publica ou escala]
  handoff[Se tema prazo: chama Experiencia da Entrega]
  saida[Saida: resumo tema urgencia rascunho]

  gatilho --> dados --> agente --> tema --> urg --> critico
  critico -->|dano fraude ofensa nota 1| humano
  critico -->|demais| rascunho --> humano
  humano --> saida
  saida --> handoff
```

Humano: CX publica a resposta. Caso crítico não sai rascunho automático para o cliente.

## 3. Relacionamento e Recompra

Gatilho: pedido entregue no prazo **e** última nota 4 ou 5 (filtro alimentado pelos outros dois agentes).

```mermaid
flowchart TD
  gatilho[Gatilho: boa entrega e nota 4 ou 5]
  dados[Entrada: historico nota atraso categoria opt-out]
  bloqueio{Nota baixa atraso ou nao quer contato?}
  nao[Nao contactar]
  prio[Prioridade alta ou media]
  msg[Rascunha mensagem sem codigo interno]
  humano[CRM autoriza o disparo]
  saida[Saida: lista e texto ou bloqueio]

  gatilho --> dados --> bloqueio
  bloqueio -->|sim| nao --> saida
  bloqueio -->|nao| prio --> msg --> humano --> saida
```

Humano: CRM decide se envia. Má experiência **nunca** entra na lista.
