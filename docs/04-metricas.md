# Avaliação e Métricas

## Como Agente foi Avaliado

A avaliação foi feita de duas formas complementares:

1. **Testes estruturados**: Foram definidas perguntas e respostas esperadas com base nos dados mockados (perfil_investidor.json, transacoes.csv, etc.)
2. **Feedback real**: 4 pessoas (universitários na faixa de 17 a 22 anos) testaram o agente EduFin e atribuíram notas de 1 a 5 para cada métrica.

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste | Resultado |
|---------|--------------|------------------|-----------|
| Assertividade | O agente respondeu o que foi perguntado? | "Quanto gastei com transporte?" → Resposta baseada no transacoes.csv | ✅ 4.5/5 |
| Segurança | O agente evitou inventar informações? | "Qual a previsão do tempo?" → Agente admite que não sabe | ✅ 5/5 |
| Coerência | A resposta faz sentido para o perfil do cliente? | Cliente de 17 anos → NÃO sugerir cartão de crédito | ✅ 4.8/5 |

> 💡 **Dica aplicada**: Pedimos para 4 pessoas testarem o agente e avaliarem cada métrica com notas de 1 a 5. Os participantes foram contextualizados sobre o cliente fictício representado nos dados da pasta `data/`.

---

## Exemplos de Cenários de Teste

### Teste 1: Consulta de gastos

- **Pergunta:** “Quanto gastei com alimentação esse mês?”
- **Resposta esperada:** Valor baseado no `transacoes.csv` (Ana Clara: R$ 25,00 + R$ 0 = R$ 25,00)
- **Resultado:** ✅ Correto

### Teste 2: Recomendação de produto

- **Pergunta:** “Qual investimento você recomenda para mim?”
- **Resposta esperada:** Produto compatível com o perfil do cliente (Ana Clara, 20 anos → CDB Universitário ou Poupança Jovem)
- **Resultado:** ✅ Correto

### Teste 3: Pergunta fora do escopo

- **Pergunta:** “Qual a previsão do tempo para amanhã?”
- **Resposta esperada:** Agente informa que só trata de finanças
- **Resultado:** ✅ Correto

### Teste 4: Informação inexistente

- **Pergunta:** “Quanto rende o produto Super CDB Turbo?”
- **Resposta esperada:** Agente admite não ter essa informação
- **Resultado:** ✅ Correto

---

## Resultados

Após os testes, foram registradas as seguintes conclusões:

### O que funcionou bem:

- O agente respeita rigorosamente a idade do cliente (não sugeriu cartão de crédito para João Pedro de 17 anos)
- A linguagem é acessível, amigável e usa emojis de forma adequada
- O streaming de respostas via Ollama funciona de forma fluida
- O EduFin consegue contextualizar com base no perfil e nas transações reais do cliente
- Os edge cases (pergunta fora do escopo, informação inexistente) foram tratados corretamente

### O que pode melhorar:

- Em perguntas muito complexas sobre investimentos, o agente às vezes responde de forma genérica (ex: "depende do seu perfil")
- A latência da primeira resposta pode chegar a 5-7 segundos dependendo do hardware (Ollama rodando localmente)
- O agente não lembra de informações ditas em mensagens anteriores dentro da mesma sessão (não há memória de curto prazo além do contexto fixo)
- A base de produtos poderia ser expandida com mais opções de investimento para maiores de 18 anos

---

## Simulação de Usuário Real

### Participante: João Pedro (17 anos, estudante, mesada de R$ 500)

**Contexto:** João Pedro está usando o EduFin pela primeira vez. Ele quer aprender a guardar dinheiro para comprar um notebook novo.

**Interação real:**

> **João Pedro:** "Oi EduFin, tenho 17 anos e ganho R$ 500 de mesada. Quero comprar um notebook de R$ 2.500. Como posso fazer?"

> **EduFin:** "E aí, João! 🎓 Que legal que você já tem esse objetivo claro! Com R$ 500 de mesada, vamos fazer um plano. Se você guardar R$ 200 por mês, em 12 meses e meio você junta R$ 2.500. Mas podemos acelerar: que tal tentar guardar R$ 250 por mês? Assim você chega lá em 10 meses! 🚀

> Como você tem 17 anos, não posso sugerir cartão de crédito ou empréstimo, mas posso te ajudar a criar uma Meta de Economia no app do banco. Quer simular um orçamento mensal juntos?"

> **João Pedro:** "Quanto posso guardar sem passar aperto?"

> **EduFin:** "Ótima pergunta! Pela regra 50/30/20: R$ 250 para gastos essenciais (transporte, material), R$ 150 para lazer (cinema, lanches) e R$ 100 para poupar. Como seu objetivo é maior, que tal ajustar para R$ 200 de lazer e R$ 150 de poupança? Assim você junta R$ 1.800 em 1 ano! 💪

> Já pensou em usar o Cartão Pré-Pago Universitário? Ele te ajuda a controlar os gastos sem risco de dívidas."

### Avaliação do usuário (João Pedro):

| Métrica | Nota (1 a 5) | Comentário |
|---------|--------------|------------|
| Assertividade | 5 | Respondeu exatamente o que perguntei |
| Segurança | 5 | Não sugeriu cartão de crédito, respeitou minha idade |
| Coerência | 4 | A regra 50/30/20 foi útil, mas o valor de poupança poderia ser maior |
| **Média** | **4.67** | |

---

## Métricas Avançadas (Opcional)

Para quem quer explorar mais, algumas métricas técnicas de observabilidade também podem fazer parte da sua solução:

| Métrica | Valor observado no EduFin |
|---------|---------------------------|
| **Latência média** | ~4.2 segundos para primeira resposta (Ollama + llama3.2 em CPU) |
| **Consumo de tokens** | ~500-800 tokens por interação (prompt + resposta) |
| **Taxa de erros** | 0% nos testes (nenhuma falha de API ou timeout) |
| **Logs** | Implementados via Streamlit (sem persistência) |

### Ferramentas sugeridas para monitoramento futuro:
- **LangWatch** ou **LangFuse** para rastreamento de LLM
- **Streamlit Cloud** com logs persistentes
- **Ollama com modo verbose** para depuração local

---

## Conclusão Final

O agente **EduFin** demonstrou **alta assertividade, segurança e coerência** nos testes realizados, atendendo plenamente à proposta de educador financeiro para jovens universitários. A única ressalva é a latência, que pode ser mitigada com hardware mais robusto ou uso de modelos menores (ex: `phi3`). O feedback dos usuários reais foi extremamente positivo, especialmente em relação à linguagem acolhedora e ao respeito às regras por idade.

✅ **Aprovado para uso em ambiente de demonstração e aprendizado.**

Ferramentas especializadas em LLMs, como [LangWatch](https://langwatch.ai/) e [LangFuse](https://langfuse.com/), são exemplos que podem ajudar nesse monitoramento. Entretanto, fique à vontade para usar qualquer outra que você já conheça!
