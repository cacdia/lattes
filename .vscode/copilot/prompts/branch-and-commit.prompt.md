---
mode: 'agent'
description: 'Versionar o projeto usando Conventional Commits'
tools: ['changes', 'fetch', 'codebase', 'githubRepo', 'problems', 'runCommands', 'usages']
---

# Inicialização
1. Garantir: nunca usar modo interativo dos comandos.

# Verificar alterações
2. chamar ferramenta #changes para listar alterações pendentes no #codebase
3. if nenhuma alteração encontrada:
     - terminar (nada a commitar)

# Agrupar alterações (mínimo: um ciclo)
4. Para cada conjunto lógico de alterações (por arquivo ou grupo relacionado) faça:
     a. Determinar tipo_da_mudança <- avaliar se é:
        - "feat"  (nova funcionalidade)
        - "fix"   (correção de bug)
        - "chore" (tarefas de manutenção)
        - "docs"  (documentação)
        - "refactor" (refatoração)
     b. Escrever descrição_curta <- resumo em português, imperativo, poucas palavras (sem pontuação final)
     c. Definir escopo_opcional <- (ex: api, ui, build) ou vazio
     d. Determinar breaking_change_flag <- true se houver quebra de compatibilidade, senão false

# Criar e mudar para branch
5. branch_name <- tipo_da_mudança + "/" + slugify(descrição_curta)
   - slugify: minúsculas, espaços -> -, remover caracteres inválidos
6. Executar comando:
   git checkout -b <branch_name>

# Preparar staging
7. Selecionar arquivos afetados pelo conjunto
8. Executar:
   git add <lista-de-arquivos>    # ou git add -A se preferir

# Montar mensagem de commit (em português)
9. Cabeçalho:
   if escopo_opcional != vazio and breaking_change_flag == true:
       header <- "<tipo>[<escopo>]!: <descrição_curta>"
   else if escopo_opcional != vazio:
       header <- "<tipo>[<escopo>]: <descrição_curta>"
   else if breaking_change_flag == true:
       header <- "<tipo>!: <descrição_curta>"
   else:
       header <- "<tipo>: <descrição_curta>"

10. Corpo (opcional):
    - Se precisar de contexto, adicionar uma linha em branco e depois o corpo explicando "o que" e "por que"
    - Incluir referências (issue #123) se aplicável

# Commit
11. mensagem_completa <- header + ( "\n\n" + corpo se corpo existe )
12. Executar commit com a mensagem entre aspas simples:
    git commit -m '<mensagem_completa>'

# (Opcional) Push
13. Se desejar subir a branch:
    git push -u origin <branch_name>

# Fim do ciclo
14. Repetir para o próximo conjunto lógico de alterações, ou terminar.
