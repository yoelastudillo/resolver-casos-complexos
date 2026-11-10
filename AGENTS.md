# Manutenção

- Manter a skill instalável em `skills/resolver-casos-complexos/`, sem dependências da raiz.
- Preservar o nome público; manter fontes de domínio fora do procedimento genérico.
- Manter exemplos, testes e instruções de contribuição fora da pasta instalável.
- Usar somente dados sintéticos em testes, issues, registros e exemplos públicos.
- Não apresentar validação estrutural como prova de eficácia.
- Ao alterar comportamento, executar cenários pertinentes em contextos novos, sem respostas esperadas; registrar execuções incompletas como incompletas.
- Manter versão, licença e caminhos consistentes.
- Executar `python tools/validar_distribuicao.py .` e `python -m unittest discover -s tests -v`.
- Não interpretar estas instruções como autorização para publicação ou ações externas.

