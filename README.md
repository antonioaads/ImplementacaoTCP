# ImplementacaoTCP
Repositório para a implementação do protocolo TCP
Disciplina de Redes / Engenharia de Computação

Prof. Sandro Renato Dias

CEFET-MG / 2019-2
<br>
O Documento relata o processo de Implementação da Pilha de Comunicação entre as camada no modelo TCP.
O trabalho foi diivdido em 4 camadas ,são elas: <br>
<li>Camada de Aplicação : Desenvolvida pelo aluno Marcos Junio, utilizando a Linguagem Go.<br>
<li>Camada de Transporte : Desenvolvida pelo aluno Gabriel , utilizando a Linguagem Python.<br>
<li>Camada de Rede : Desenvolvida pelo aluno Rodrigo ,utilizando a linguagem JavaScript.<br>
<li>Camada Física : Desenvolvida pelo aluno Antonio Dias , utilizando a linguagem ShellScript.<br>

Ao final do trabalho, todas as camadas deveriam estar sem comunicando e integralizando a pilha.
A Comunicação entre as camadas foi determinada pela leitura de um arquivo,denominado PDU referente a cada camada.
# Camada de Aplicação
<h2>Escolhas do Projeto</h2>
Foi decidido implementar que a camada de Aplicação inicializa um Servidor Local para que o Cliente possa navegar pelo Browser (parte gráfica)e visualizar a pagina requerida.

<h2>Comunicação para envio de pacotes no Cliente</h2>
Quando o Cliente esta sendo executado, ao digitar no navegador o endereco do servidor e o arquivo solicitado, como por exemplo :192.168.14.19:8080/Servidor.go , significa que o Cliente quer fazer uma requisição para o endereço : 192.168.14.19 (endereço do servidor) que na aplicação Cliente está rodando na porta 8080 e Servidor.go é o nome do arquivo ao qual deseja visualizar no navegador. Para isso é criado um arquivo no formato TXT contendo o Cabeçalho da requisição e o no campo Dado da PDu da Aplicação está inserido o nome do arquivo solicitado.E então esse arquivo TXT é salvo e será utilizado pela camada debaixo(Transporte) para que seja continuado a sequencia da pilha.

<h2>Comunicação para Recebimento de pacotes no Servidor</h2>
Após todo processo da requisição, o pacote chega no Servidor, e então deve-se abrir o arquivo, que contem o nome do arquivo que deve ser enviado para o Cliente,selecionamos o arquivo, e criamos uma nova mensagem com o conteudo do arquivo solicitado, após esse processo, a camada de Transporte no Servidor se encarrega de dar proseguimento a sequencia da Pilha.


<h2>Recebimento de Pacotes no Cliente</h2>
Após o Servidor enviar o arquivo, temos o arquivo solciitado pelo Cliente contendo o Cabeçalho e o conteudo do arquivo.
Foi decidido mostrar apenas o conteudo do arquivo sem o cabeçalho no navegador.
<h2>Formato do cabeçalho</h2>
Para o Cabeçalho na Aplicação foi utilizado o HTTP na versão 1.0.Com as seguintes informações : Metodo (Get ou Post),Endereço de requisição do Servidor , User_Agente (Determinado pelo navegador,Browser, utilizado pelo Cliente) .
<h2>Execução</h2>
<li>Execução no Cliente
Para executar a Camada de Aplicação, deve ser verificado se está instalado o pacote GoLang.
Após isso, ir na pasta CamadaAplicacao/Cliente e executar o arquivo Cliente.go pelo comando :
<br> go build Cliente.go    <br> go run Cliente.go <br>
E Assim poderá ser verificado pelos Logs no terminal que o Servidor Local está rodando em uma determinada porta. E Com isso é so ir ate o navegador e digitar o Endereo Ip do servidor e o arquivo solicitado.
<li>Execução no Servidor
De Maneira analoga ao Cliente, no servidor vamos rodar o arquivo Servidor.go<br>
go build Servidor.go <br>
go run Servidor.go<br>

