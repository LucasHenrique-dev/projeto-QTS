# UC_01 - Gerar QTS

## Descrição:
Este caso de uso permite a criação de um quadro de trabalho semanal.
## Atores:
Funcionário da PRF.
## Pré-condição:
Estar na página inicial da aplicação.
## Pós-condição:
Usuário visualiza quadro de trabalho semanal e a opção de "Imprimir" é habilitada.
## Fluxo Principal:
1. Usuário deseja gerar QTS;
1. Usuário clica no botão "Gerar Novo Quadro";
1. Sistema realiza cálculos de otimização para geração do quadro de trabalho;
1. Sistema exibe o novo quadro de trabalho semanal;
## Fluxo de Exceção:
* FE1 - Dados Não Informados
  * FE1.1 - Na etapa 2 do fluxo principal, sistema verifica que usuário não forneceu todas as informações necessárias para o bom funcionamento do sistema;
  * FE1.2 - Sistema desabilita o clique no botão "Gerar Novo Quadro";
  * FE1.3 - Sistema exibe uma notificação "Cadastre todos os dados referentes às aulas, vá até a sessão de cadastro";
## Nota Auxiliar:
"O bom funcionamento do sistema" se refere aos dados mínimos para que um QTS possa ser gerado e, para isso, é necessário se certificar de que as informações de aulas, instrutores, materiais, salas e critérios de prioridade foram corretamente preenchidas.
