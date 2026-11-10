# Resolver casos complexos

Skill em português para transformar evidências conflitantes, causas incertas e
dependências em **uma decisão rastreável e uma próxima ação verificável**.

*An evidence-based decision workflow for ambiguous problems.*

## Quando usar

- Investigar um incidente com mais de uma explicação plausível.
- Comparar alternativas quando disponibilidade, requisitos ou prazos são incertos.
- Revisar um plano quando uma nova fonte contradiz uma conclusão anterior.

O procedimento serve a diferentes áreas; critérios técnicos e regras específicas
precisam vir das fontes do problema. Para definições, traduções ou tarefas simples,
uma resposta direta é suficiente.

## Instalar

A pasta instalável é [skills/resolver-casos-complexos](skills/resolver-casos-complexos/SKILL.md).

Com Node.js 22.20 ou superior e o [CLI Skills](https://github.com/vercel-labs/skills),
baixe e extraia este repositório, abra um terminal na pasta deste README e execute:

```bash
npx skills add . --skill resolver-casos-complexos --global
```

Escolha o assistente no instalador. A opção `--global` disponibiliza a skill para
o usuário, entre projetos. Para instalar somente em um projeto, abra o terminal
**nesse projeto**, use o caminho absoluto da pasta extraída no lugar de `.` e
retire `--global`. Para instalar diretamente do GitHub, use a URL deste
repositório no lugar de `.`.

Sem o CLI, copie a pasta instalável completa para o diretório de skills aceito
pelo seu assistente. Preserve referências, modelo e licença.

## Usar

Em ambientes com invocação por nome:

> Use $resolver-casos-complexos para analisar estas fontes. Preciso decidir
> [decisão], preservando [restrições]. Entregue [resultado esperado].

Forneça os documentos, registros ou trechos pertinentes e informe o que já está
autorizado. A sintaxe de invocação e o acesso a ferramentas dependem do assistente.

**Exemplo fictício:** um contrato exige exportação CSV e teste de integração;
uma demonstração mostra apenas o painel. A saída útil identifica quais requisitos
ainda não foram verificados, prepara o teste necessário e condiciona o aceite
a seu resultado. A falta de demonstração não prova, sozinha, que a funcionalidade
não existe.

O resultado normalmente contém a decisão, evidências e limites, a próxima ação,
seu responsável proposto e a condição que mudaria o plano. A skill conclui ações
autorizadas quando há ferramentas e acesso; caso contrário, entrega uma proposta
utilizável e explicita a etapa pendente.

Em um chat sem instalação nativa, anexe `SKILL.md` e os arquivos Markdown de
`references/` e `assets/`, e peça a aplicação do procedimento. Confirme que o
assistente consegue ler os anexos. Isso fornece contexto à conversa, não
instalação permanente.

## Dados e permissões

Esta skill contém instruções e um modelo; não fornece um serviço próprio de
armazenamento, telemetria ou envio de dados. Os scripts em `tools/` são controles
locais de manutenção, sem chamadas de rede. O instalador e o assistente usado
têm suas próprias políticas e configurações.

Compartilhe apenas dados necessários e guarde registros preenchidos fora da
pasta instalada. As instruções operacionais sobre minimização e fontes não
confiáveis estão em [dados e fontes](skills/resolver-casos-complexos/references/dados-e-fontes.md).
A skill não concede acesso, permissão, habilitação profissional nem monitoramento
automático.

## Estrutura e qualidade

| Caminho | Uso |
|---|---|
| `skills/resolver-casos-complexos/` | Skill independente: núcleo, quatro referências, um modelo, metadados e licença. |
| [evals/README.md](evals/README.md) | Cenários, protocolo e limites da avaliação. |
| [evals/RESULTADOS.md](evals/RESULTADOS.md) | Execuções registradas, incluindo comparação sem a skill. |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Como propor e verificar mudanças. |
| [CHANGELOG.md](CHANGELOG.md) | Histórico de versões e notas de publicação. |

O pacote usa o formato [Agent Skills](https://agentskills.io/specification).
Conformidade de formato não demonstra eficácia. Os ensaios registrados são
limitados; não estabelecem superioridade geral sobre o modelo sem a skill.

Para manutenção, com Python 3.10 ou superior:

```bash
python tools/validar_distribuicao.py .
python -m unittest discover -s tests -v
```

Versão: 1.0.0. Licença: [MIT](LICENSE).

