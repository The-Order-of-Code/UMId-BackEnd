## Introdução

#### Nesta secção iremos explicar a estrutura do CA e da PKI do projecto, onde criamos o nosso CA, gerimos-lo para assinar certificados e propriedades dos utilizadores de modo a garantir o uso seguro da nsosa aplicação.

## Estrutura
Nós optamos por estruturar em duas secções diferentes, o [CA](./CA/) e o [PKI](./PKI/), pois o CA, pode estar numa máquina idependente do PKI.

### CA
O CA é independente do pki, na pasta do [CA](./CA/Readme.md) podemos ver os comandos necessários para inicializá-lo e estará encarregue por assinar os certificados fidedignos, e garantir a autenticidade das propriedades dos utilizadores.

### PKI
O PKI estará encarregue por tratar dos pedidos da aplicação e fazer a ligação com o CA que irá autenticar-los ou não, na pasta [PKI](./PKI/) encontram-se os ficheiros de configuração para garantir a comunicação entre o backend e o ca.

