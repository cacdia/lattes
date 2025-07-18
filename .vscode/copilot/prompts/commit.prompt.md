---
mode: 'agent'
description: 'Versionar o projeto usando Conventional Commits'
tools: ['changes', 'fetch', 'codebase', 'githubRepo', 'problems', 'runCommands', 'usages']
---

# Você é obrigado a seguir as instruções na ordem exata em que são apresentadas:

{
  "attention": "Sempre siga o padrão Conventional Commits de modo profissional. Garanta que cada mensagem de commit seja clara, contextualizada e padronizada, facilitando o entendimento do histórico do projeto por qualquer pessoa.",
  "steps": [
    {
      "id": 1,
      "instruction": "Nunca utilize a versão interativa dos comandos."
    },
    {
      "id": 2,
      "instruction": "Verifique cada uma das alterações que você fez no `#codebase` através da tool `#changes`.",
      "tools": ["changes", "codebase"]
    },
    {
      "id": 3,
      "instruction": "Entenda o que cada alteração representa (nova funcionalidade, correção de bug, melhoria, etc.)"
    },
    {
      "id": 4,
      "instruction": "Crie e mude para uma nova branch que reflita o tipo e o escopo das alterações.",
      "command": "git checkout -b <tipo>/<descrição-curta>",
      "prefixes": ["feat/", "fix/", "chore/", "docs/", "refactor/"]
    },
    {
      "id": 5,
      "instruction": "Para todos os arquivos pendentes, em português, escreva o commit na forma `<tipo>[escopo][!]: <descrição>`."
    },
    {
      "id": 6,
      "instruction": "[Opcional] Após uma linha em branco, acrescente o corpo para adicionar contexto e detalhes."
    },
    {
      "id": 7,
      "instruction": "Com a mensagem entre aspas simples, submeta o commit.",
      "command": "git commit -m '<mensagem do commit>'"
    }
  ]
}
