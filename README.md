# UMId-BackEnd
<a href="https://gitmoji.carloscuesta.me">
  <img src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=flat-square" alt="Gitmoji">
</a>

## Padronização de Desenvolvimento
<p align="center">
  <img width="100" height="100" src="https://avatars2.githubusercontent.com/u/58614957?s=400&u=d133ba2f65c51ecb72cdf6753ab378b77fef46a4&v=4">
</p>

No intuito de proporcionar uma organização aos repositórios e haver uma uniformidade na forma do trabalho nestes. A equipa The Order of Code (TOC) optou adotar padronização na gestão dos fluxo de desenvolvimento :

1. [Documentação]()
2. [Branchs](#branchs);
3. [Commits](#commits);
4. [Issue](#issue).

## Documentação:
Deve-se documentar a configuração do ambiente e possíveis problemas e suas respectivas soluções. Para facilitar a configuração do ambiente de desenvolvimento para outros da equipa e otimizar para solucionar um possível problema apareça mais de uma vez.

## Branchs:

Iremos adotar o fluxo de branchs baseado no Workflow Design: Git Flow o qual foi publicado e popularizado por Vincent Driessen na nvie. O fluxo de trabalho Gitflow define um modelo de ramificação estrito projetado em torno da publicações de versões do projeto. Isso nos proporciona um maior gerenciamento do projeto. 


<p align="center">
  <img width="450" height="200" src="https://iamchuka.com/content/images/2018/05/gitflowimage.png">
</p>

### Descrição das Branchs
| Só existe duas branchs que são fixas a branch master aonde é rotulado a versão do projeto e branch develop a branch a qual é feita todo desenvolvimento.


- [x] **Master:** 
  
1.  Branch de produção o codigo que está aqui é correspondente da versão do produto até então desenvolvida.
   
    1.  O versionamento deve seguir a seguinte logica **v[x].[y].[w]** = v0.1.0;
  
     2.  O **v** de versão o **y** correspondente cada vez que o código for dado merge a master incrementa-se mais um. Quando este valor atingir 9 valores o **x**  incrementa-se mais um. O **w** representa a quantidade de vezes que se utilizou a branch Hotfix.
  

- [ ] **Hotfix:** 
     - Branch criada quando ocorre um erro no código que está em produção e esse não pode ser esperar uma nova release. Deve-se uma Hotfix criar para corrigir o erro e ao termino deste dar merge na Master e na Devolop
  
    
  
- [x] **Develop:** 
  - branch da qual irá ser base para desenvolvimento do projeto.
  
- [ ] **Feature:**  

 1.  São criadas apartir da Develop seguindo a seguinte nomeclatura feature/[ nome da funcionalide];

1.  Para desenvolver uma nova funcionalidade;
   
2.  Ao finalizar essa funcionalide deve-se testar;
   
3.  Tudo ok na etapa anterior dar-se merge a Develop;
     
4. Deleta-se a branch feature.
   
  
- [ ]  **Realease:**
  
1.  É criada apartir da develop quando se tem um junto de features as quais desejam testar;
  
2. Colaca-se no nome dessa branch da seguinte forma **release/v[X.Y.W]** . Sendo o segundo parametro referente a versão que será tageada na branch master;

3. Uma vez testada todas as features, deve-se fazer merge com a master finalizando seu ciclo de vida.
    

## Commits:

<img align="left" src="https://cloud.githubusercontent.com/assets/7629661/20073135/4e3db2c2-a52b-11e6-85e1-661a8212045a.gif" width="150" height="100" /> 

Para haver uma uniformidade nos commits e entendermos o que se passa em cada commit feito ao projeto iremos utilizar o Gitmoji.

Depois de clonar os repositórios os quais irão trabalhar. Para usar o gitmojis na linha de comando, instale gitmoji-cli.

```bash
 npm i -g gitmoji-cli
```

Logo após a instalação sete o comando, para criar um hook sempre quando chamar opção git commit 

```bash
 gitmoji init -i
```


**Quando for fazer commit:**

Agora quando for fazer commit basta digitar git commit e apertar enter e aprecerá as seguintes telas:

1. Escolhe a mensagem que representa aquele commit e aperta enter.
   
<p align="center">
  <img width="500" height="150" src="https://miro.medium.com/max/996/1*xk6ZOkjbi6S4jExb_ivY9A.png">
</p>

1. Deve-se escrever um titulo iniciado por um verbo que expresse uma ação. Logo em seguida será solicitado uma mensagem que descreverá melhor aquele commit.
   
<p align="center">
  <img width="500" height="150" src="https://miro.medium.com/max/1006/1*HuyRn2Ivr6PShE6wHt8d3w.png">
</p>


## Issue

Toda issue encontrada no projeto deve ser regista no repositório e quando resolvida deve ser fechada  atráves de um commit. Tutorial para utilizar palavras chaves para tal finalidade [aqui](https://docs.github.com/en/enterprise/2.16/user/github/managing-your-work-on-github/closing-issues-using-keywords).



