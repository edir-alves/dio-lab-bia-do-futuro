# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Utilização no Agente |
|---------|---------|----------------------|
| `produtos_conta_universitaria.json` | JSON | Sugerir produtos adequados à idade e renda (ex: cartão controlado, poupança, meta de economia) |
| `perfil_universitario.json` | JSON | Personalizar orientações com base no perfil do jovem (ex: mesada fixa, renda própria, startup) |
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores para não repetir orientações e dar continuidade ao aprendizado |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente (categorias, valores, frequência) e sugerir ajustes |

## Adaptações nos Dados

Os dados mockados foram **expandidos** para incluir:
- Faixas etárias específicas (17 a 25 anos)
- Exemplos de renda compatível com universitários (R$ 100 a R$ 3.000/mês)
- Produtos bancários com limites reduzidos e educativos
- Cenários de gastos típicos (transporte, alimentação, lazer, material)
- Regras legais adaptadas (ex: menor de 18 não pode ter cheque especial)
- Histórico de conversas simuladas para o agente lembrar de orientações já dadas
- Transações realistas de universitários (mesada, estágio, startup, gastos do dia a dia)

## Estratégia de Integração

### Como os dados são carregados?

Os arquivos JSON/CSV são carregados no início da sessão do chatbot e incluídos no **contexto do prompt do LLM**. O agente não acessa banco de dados em tempo real, apenas os arquivos estáticos versionados no repositório.

### Como os dados são usados no prompt?

Os dados vão no **system prompt** como um bloco estruturado de conhecimento base. O agente consulta esses dados dinamicamente antes de responder, priorizando:
- O histórico de atendimento para dar continuidade
- As transações para identificar padrões de gasto
- As regras e produtos definidos nos JSONs

### Exemplo de formatação dos dados para o agente
Dados do Cliente:
- Nome: Ana Clara
- Idade: 19 anos
- Perfil: Renda própria (estágio + startup)
- Renda mensal: R$ 1.800
- Saldo atual: R$ 450

Histórico de Atendimento:
- 01/04: Cliente perguntou como investir R$ 200
- 05/04: Agente sugeriu Poupança Jovem
- 10/04: Cliente disse que vai começar a guardar

Últimas transações:
- 10/04: Transporte - R$ 120
- 12/04: Lanchonete - R$ 35
- 15/04: Material faculdade - R$ 90

Regras aplicáveis:
- Menor de 18? Não
- Pode ter cartão com limite? Sim, até R$ 500
- Pode investir? Sim, apenas renda fixa básica
