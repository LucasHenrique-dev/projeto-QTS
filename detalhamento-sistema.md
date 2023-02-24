- Plano de Aulas:
  - Descritvo de todas as aulas de uma disciplina para uma turma;
  - Aulas numeradas pelo ID;
  - Quantitativo de professores para a aula;
  - Recursos materiais necessários para ministrar a aula;
  - Horas de aula: não é um valor fixo;
  - Observações e Pré-requisitos: onde será, perído (manhã, tarde, noite e madrugada), entrada (aulas conjugadas: aulas contínuas), apoio (equipe de suporte), observações;
</br>

- Corpo Docente:
  - Divisão em equipes;
  - Cada equipe possui x instrutores (varia para cada equipe);
  - Cada equipe é responsável por algumas turmas;
  - Equipe pode se dividir para dar aulas simultâneas;
  - Calendário de permanência: data de início e término das atividades;
  - Quantitativo de horas lecionadas por dia;
</br>

- Informações Gerais:
  - Vários cursos simultâneos; Curso possui disciplinas e cada disciplina possui aulas.
  - Vários Campus disponíveis;
  - Campus possuem vários locais;
  - Aulas EAD podem ser cogitadas; EAD são aulas assíncronas, possuem data limite e podem servir como pré-requisito.
  - Recursos limitados;
  - Certas aulas necessitam de intervalos (não podem ter aulas após);
  - Imprevistos ocorrem é torna-se necessário elaborar novos QTS durnate o curso;
</br>

- Sistema Atual:
  - Visão do instrutor: cronograma de segunda a domingo contendo os horários de aula de cada equipe;
  - Visão do aluno: cronograma de segunda a domingo contendo os horários de aula de cada turma;
  - Cronogramas de aulas montados por Google Sheets;
  - Transição dos dados para um banco de dados (Laravel);
  - Tabelas de relacionamentos: equipes-turmas, informações contidas no plano de aulas, etc;
</br>

- Objetivos:
  - [ ] Impelmentar QTS flexível para atendar a todas os requisitos descritos (obrigatório);
  - [ ] Implementar a visão do aluno (prioritário);
  - [ ] Diminuir o tempo de ociosidade dos instrutores (pioritário);
  - [ ] Diminuir a permanência do instrutor na PRF (prioritário);
  - [ ] Implementar um QTS para o curso todo (preferível);

 <!--
Visão do professor e aluno 
divisão em equipes: 12 equipes com instrutores variáveis
aulas simultâneas e é preciso reduzir o tempo de ociosidade (algumas vezes é necessário aumentar o espaço)
Disciplina possui x aulas e algumas delas tem condições especiais (precisam de ser a noite, tarde..)
imprevistos podem acontecer e é necessário refazer o QTS.
Professores tem "prazo": dar aula de dia tanto até tanto
O ideal:
é fazer um QTS para o curso todo (varia)
são vários cursos simultâneos
Sistema em Laravel: é basicamente o banco de dados
requisitos essenciais:
diminuir a ociosidade do professor
diminuir a permanência do instrutor na PRF
Visões do sistema:
visão do aluno (ver o quador de aulas)
visão do instrutor (ver quais aulas precisar dar)
Plano de ensino:
mostra as informações de cada disciplina
existe uma tabela contendo informações do plano de aulas
- visão do aluno é mais emergente
turmas simultâneas:
um grupo de professores pode se dividir e dar aulas smultâneas
professores são responsáveis por turmas
algumas aulas precisam de mais de um professor (na mesma sala)
equipes de professores: dão aulas para turmas específicas
tabela relacionando equipes e turmas
plano de atividades é para a turma
-->
