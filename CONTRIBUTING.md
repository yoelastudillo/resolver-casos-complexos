# Contribuir

Abra uma issue ou pull request com um cenário sintético, o comportamento observado
e o resultado útil esperado. Prefira mudanças pequenas que melhorem uma decisão
ou evitem um erro identificável.

## Alterar instruções

Mantenha o núcleo breve e carregue referências somente quando necessárias.
Não adicione explicações sobre como a skill foi criada nem repita o mesmo
procedimento em vários arquivos. Preserve o nome público.

Para mudanças de comportamento, aplique o [protocolo de avaliação](evals/README.md).
Guarde a resposta real, a configuração e as limitações; não edite uma saída
antiga para parecer melhor. Um cenário escrito ou uma busca textual não equivale
a uma avaliação executada.

## Verificar

Com Python 3.10 ou superior, sem dependências adicionais:

```bash
python tools/validar_distribuicao.py .
python -m unittest discover -s tests -v
```

O validador verifica o formato canônico deste repositório. Não é um parser YAML
geral nem uma certificação de compatibilidade de todos os assistentes.

Para futuras versões, atualize `VERSION`, a versão textual de `SKILL.md`, README,
changelog e os resultados pertinentes. Mantenha as duas cópias de LICENSE iguais.
Registre arquivos novos em `PUBLIC_FILES` no validador.

## Proteger dados

Envie somente exemplos sintéticos, sem nomes reais, credenciais, arquivos
privados ou combinações de detalhes identificadoras. Revise também comentários,
metadados e histórico. `.gitignore` não remove conteúdo já versionado.

Não publique um valor sensível para comunicar sua descoberta: descreva o tipo e
a localização. A revisão automática de padrões ajuda, mas não certifica
anonimato. As contribuições seguem a licença MIT.

