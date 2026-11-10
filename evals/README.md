# Avaliações

Os [cenários](casos.json) são sintéticos e ficam fora da pasta instalável.
As [saídas registradas](RESULTADOS.md) permitem revisar o comportamento observado;
não representam promessa de eficácia.

## Executar

1. Fixar a versão e os hashes dos arquivos da skill.
2. Abrir um contexto novo por execução, sem histórico ou respostas anteriores.
3. Fornecer apenas a solicitação do cenário e, quando houver, seus arquivos iniciais
   em uma pasta exclusiva. Não fornecer `criterios_de_revisao`.
4. Para a condição com skill, permitir leitura da pasta instalável; para o controle,
   fornecer a mesma tarefa sem a skill. Manter modelo e restrições equivalentes.
5. Guardar a resposta integral e os artefatos efetivamente modificados.
6. Avaliar fidelidade, utilidade da ação, limites, autorização e proporcionalidade.
   Para edição, comparar arquivos e conferir a preservação dos originais.
7. Registrar versão, modelo/configuração solicitados, acesso permitido, duração
   quando disponível e estado da execução.

Dar ao executor uma resposta esperada invalida a independência dessa avaliação.
Uma falha de infraestrutura não é um resultado de comportamento.

## Interpretar

Distinguir resultado concluído, interrupção e cenário ainda não executado.
Registrar falhas e respostas desfavoráveis; nunca substituir uma saída real por
uma resposta ideal. Antes de atribuir ganho à skill, comparar com o modelo sem
as instruções. Um único par de respostas não demonstra efeito causal ou
superioridade geral.

Esta versão contém uma comparação observacional. Os critérios publicados
organizam a revisão posterior; não houve avaliação cega, pré-registro nem
repetições estatísticas. O ambiente também fornece instruções gerais aos modelos,
e o controle não representa um modelo sem instruções de sistema.

Os testes Python em `tests/` verificam o validador e o empacotador. Eles não
executam o modelo nem demonstram que a skill se ativa automaticamente.

