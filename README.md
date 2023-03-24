# Orion-project
É uma plataforma online que permite aos clientes solicitar a abertura de uma ordem de serviço e acompanhar seu status em tempo real.
O sistema é construído em cima do framework Django, o que significa que é altamente personalizável e escalável. Além disso, o sistema possui uma interface de usuário amigável e responsiva, o que o torna fácil de usar em qualquer dispositivo.

Com o Sistema de Gerenciamento de Ordens de Serviço, empresas de diferentes segmentos podem melhorar a qualidade do seu suporte técnico e garantir a satisfação de seus clientes.
> Status: Em desenvolvimento..

![capturas_de_tela](https://user-images.githubusercontent.com/20466094/226771158-f5074ef3-85b3-4aaa-abb6-97afbfc6816b.gif)

## Instalação
1. Clone o repositório do projeto.
2. Instale as dependências com o seguinte comando:

```sh
pip install -r requirements.txt
```

3. Execute as migrações com o seguinte comando:

```sh
python manage.py migrate
```

4. Crie um superusuário com o seguinte comando:

```
python manage.py createsuperuser
```

5. Inicie o servidor com o seguinte comando:
```
python manage.py runserver
```

6. Acesse o projeto no seu navegador em http://localhost:8000.

## Funcionalidades
**Cadastro de Clientes**: O sistema permite o cadastro de novos clientes, com informações como nome, e-mail, telefone e endereço. Esses dados podem ser acessados pelos técnicos para facilitar o atendimento e garantir uma comunicação mais ágil e eficiente.

**Cadastro de Técnicos**: O sistema permite o cadastro de técnicos, com informações como nome, e-mail e área de atuação. Esses dados podem ser acessados pelos clientes para verificar quem é o técnico responsável pelo seu chamado e pelos administradores do sistema para gerenciar o desempenho dos técnicos.

**Autenticação e Segurança**: O sistema utiliza protocolos de autenticação e segurança avançados para garantir que apenas usuários autorizados possam acessar a plataforma e que as informações dos clientes sejam mantidas em sigilo.

**Solicitação de abertura de ordem de serviço**: O cliente pode acessar a plataforma e abrir uma nova ordem de serviço, descrevendo o problema que precisa ser resolvido.

**Acompanhamento de status de chamados**: O cliente pode acessar a plataforma e visualizar o status atual de todos os seus chamados em tempo real, como "Em andamento", "Aguardando resposta" e "Concluído".

**Atualização de status de chamados**: O técnico responsável pelo chamado pode acessar a plataforma e atualizar o status do chamado à medida que trabalha nele, mantendo o cliente informado sobre o progresso da resolução do problema.

**Histórico de chamados**: O cliente pode acessar o histórico de todos os seus chamados anteriores e verificar o status de cada um deles.

**Gerenciamento de usuários e permissões**: O sistema permite que a empresa gerencie os usuários que têm acesso à plataforma e defina suas permissões de acesso às funcionalidades.

**Geração de relatórios**: O sistema pode gerar relatórios detalhados sobre o desempenho do suporte técnico, incluindo o tempo médio de resolução de problemas, o número de chamados por técnico e outras métricas relevantes.

## Tecnologias utilizadas
**Django**: O Django é um framework de desenvolvimento web em Python, utilizado como base para o desenvolvimento deste projeto. O Django oferece diversas funcionalidades para desenvolver aplicações web, incluindo suporte para bancos de dados, autenticação de usuários, templates, formulários e muito mais.

**Widget Tweaks**: O Widget Tweaks é um aplicativo de terceiros do Django, que permite personalizar e estender os widgets de formulário do Django com facilidade. Com o Widget Tweaks, é possível adicionar classes CSS, modificar rótulos, adicionar placeholders e muito mais.

**JSignature**: O JSignature é outro aplicativo de terceiros do Django, utilizado para criar e armazenar assinaturas digitais em ordens de serviço. Com o JSignature, é possível adicionar um campo de assinatura em um formulário, permitindo que o cliente ou técnico assine digitalmente a ordem de serviço.

**Notifications**: O Notifications é um aplicativo de terceiros do Django, utilizado para enviar notificações para os usuários do sistema. Com o Notifications, é possível enviar notificações por e-mail, SMS ou outros meios, informando os usuários sobre atualizações em suas ordens de serviço.

**JavaScript**: O JavaScript é uma linguagem de programação utilizada no desenvolvimento web, principalmente para criar interações dinâmicas na interface do usuário. No projeto de gerenciamento de ordens de serviço, o JavaScript foi utilizado para criar funcionalidades como validação de formulários, animações e outras interações.

**jQuery**: O jQuery é uma biblioteca de JavaScript que simplifica a manipulação do DOM e a criação de animações e interações em páginas web. No projeto de gerenciamento de ordens de serviço, o jQuery foi utilizado para criar funcionalidades como pop-ups, seleção de elementos HTML e outras interações.

**Bootstrap**: O Bootstrap é um framework front-end de código aberto, desenvolvido pelo Twitter, que oferece diversos componentes e estilos CSS pré-definidos para construção de páginas web responsivas e amigáveis ao usuário. No projeto de gerenciamento de ordens de serviço, o Bootstrap foi utilizado para construir a interface do usuário, garantindo uma experiência consistente e de alta qualidade.

