---
mode: 'agent'
description: 'Versionar o projeto usando Conventional Commits'
tools: ['changes', 'fetch', 'codebase', 'githubRepo', 'problems', 'runCommands', 'usages']
---

# Inicialização

1. Garantir: evitar modo interativo dos comandos

2. Verificar alterações:
   - chamar ferramenta #changes para listar alterações pendentes
   - se nenhuma alteração: terminar

3. Agrupar alterações (um conjunto lógico por commit):
   a. Avaliar tipo_da_mudança:
      - "feat", "fix", "chore", "docs", "refactor", etc.
   b. Escrever descrição_curta em português, imperativo, sem pontuação final
   c. Definir escopo_opcional (ex: api, ui) ou vazio
   d. Definir breaking_change_flag se houver quebra de compatibilidade

4. Preparar staging:
   - Selecionar arquivos afetados pelo conjunto
   - Executar: git add <lista-de-arquivos>  (ou git add -A)

5. Montar mensagem de commit (Conventional Commits, português):
   - Cabeçalho:
     if escopo_opcional != vazio and breaking_change_flag:
         header <- "<tipo>[<escopo>]!: <descrição_curta>"
     else if escopo_opcional != vazio:
         header <- "<tipo>[<escopo>]: <descrição_curta>"
     else if breaking_change_flag:
         header <- "<tipo>!: <descrição_curta>"
     else:
         header <- "<tipo>: <descrição_curta>"
   - Corpo (opcional):
     - linha em branco + explicação do "o que" e "por que"
     - referências (ex: closes #123) se aplicável

6. Commit:
   - mensagem_completa <- header + ( "\n\n" + corpo se existir )
   - Executar: git commit -m '<mensagem_completa>'

7. (Opcional) Push da branch atual:
   - git push origin HEAD

8. Repetir para o próximo conjunto lógico de alterações ou terminar
