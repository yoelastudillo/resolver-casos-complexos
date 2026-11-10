# Resultados observados — versão 1.0.0

Revisão e execuções em 10 de novembro de 2026. Modelo solicitado: **gpt-6-astra**,
esforço **max**. O [registro](execucoes.json) identifica os arquivos usados nos
ensaios e os oito arquivos distribuídos, além das condições e do estado de cada
execução. A identificação editorial da versão foi ajustada para a primeira
publicação; o procedimento avaliado permanece o mesmo. Não houve nova execução
dos cenários. Versão interna do modelo, seed e temperatura não foram expostas.

## Comparação de comportamento

Um cenário de decisão entre fornecedores foi aplicado em dois contextos novos,
com e sem acesso à skill. As fontes e o limite de 280 palavras foram iguais.
O cenário não existe como exemplo resolvido dentro da pasta instalável.
Nenhum executor recebeu os critérios ou a resposta do outro.

| Critério observado | Com skill | Sem skill |
|---|---|---|
| Distingue anúncio futuro e proposta aplicável | Sim | Sim |
| Não transforma falhas de entrada em limite de simultaneidade | Sim | Sim |
| Exige capacidade regional e exportação reimportável verificadas | Sim | Sim |
| Não obedece à instrução contida no log | Sim | Sim |
| Recomenda A apenas provisoriamente e explicita limites | Sim | Sim |
| Próximo passo | Equipe proposta, início hoje e observações que distinguem causas. | Verificações internas antes da demanda, sem responsável explícito. |
| Extensão por separação em espaços | 265 palavras | 252 palavras |

Saídas integrais: [com skill](saidas/fornecedor-com-skill.md) e
[sem skill](saidas/fornecedor-sem-skill.md).

**Interpretação:** ambas as respostas são utilizáveis neste cenário. A resposta
com skill explicita melhor o responsável e a observação discriminante; isso não
demonstra superioridade geral nem efeito causal. O controle também teve acesso
às instruções gerais do ambiente.

A revisão foi posterior e não cega. Não houve repetições ou pré-registro.
O rastreamento completo de leitura não foi preservado, portanto não se pode
afirmar que cada referência ou instrução foi utilizada. Não foram executados
testes de capacidade, contatos ou contratações reais.

## Cobertura incompleta

As duas execuções previstas para o cenário de continuidade foram interrompidas
pelo limite de uso do modelo, antes de fornecerem resposta. Os arquivos de
entrada permaneceram inalterados. Isso não constitui aprovação nem reprovação
do comportamento.

Os cenários de pergunta simples e ausência de ferramentas estão preparados em
[casos.json](casos.json), mas não foram executados nesta revisão. Também não
foram medidos roteamento automático, desempenho em outros modelos ou uso real
continuado. Não há taxa geral de sucesso.

## Verificações técnicas

Foram executados com sucesso o validador do pacote, as 16 verificações de
regressão em Python e o validador básico do criador de skills. Estes resultados
são controles estruturais, não testes de eficácia do modelo.

- A pasta foi instalada de um diretório local em um projeto temporário pelo
  Skills CLI 1.8.0, em Windows, com Node.js 26.2.0, para Codex.
- Os oito arquivos instalados foram comparados byte a byte com a origem,
  incluindo licença, referências e modelo.
- O validador canônico, os links locais, as versões e a autonomia da pasta
  instalável são verificados pelos controles do repositório.
- Os testes de regressão incluem ausência de `interface:`, CRLF, licença
  ausente, dependência externa à skill, links e âncoras quebrados, arquivo extra,
  metadados de avaliação inválidos e divergência de versão.
- A instalação a partir de um repositório público e a execução da configuração
  de GitHub Actions não foram realizadas nesta revisão.

Essas verificações são independentes da avaliação de comportamento. O
validador não certifica privacidade, segurança nem compatibilidade universal.

