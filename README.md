# Implementacao TCP/IP HTTP
Repositório para a a pilha de protocolos TCP/IP
Disciplina de Redes / Engenharia de Computação

Prof. Sandro Renato Dias

CEFET-MG / 2019-2
<br>
O Documento relata o processo de Implementação da Pilha de Comunicação entre as camadas no modelo TCP/IP.
O trabalho foi divdido em 4 camadas ,são elas: <br>
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

# Camada de Transporte
## Escolhas de projeto
A camada TCP criada implementa os métodos básicos de transmissão TCP, que incluem segmentação, estabelecimento de conexão e retransmissão além de técnicas de Retransmissão rápida, controle de fluxo. A camada TCP criada não implementa técnicas de temporização, checksum, controle de congestionamento completo, ou uma comunicação Peer-to-peer (Apesar de idealmente simular uma utilizando pares cliente/servidor).

A camada UDP criada apenas segmenta e envia dados, que são recebidos por uma aplicação chamada de udp_server (que apenas escuta e integra os segmentos, esta não realiza qualquer resposta ao cliente)

## Comunicação para envio de pacotes
O envio de pacotes para camadas abaixo se dá por meio de arquivos de formato txt, colocados em uma pasta específica e configurável (TCP Apenas, é necessário editar variáveis globais no código fonte de udp_cliente.py e udp_server.py para alterar um caminho) para uso pela implementação da camada abaixo. Uma vez excluído, a implementação das camadas TCP e UDP considera que o arquivo foi enviado para camada abaixo.

O conteúdo do arquivo é precedido de um Header, utilizado para indicar a porta de origem e destino do pacote

## Comunicação para recebimento de pacotes
O recebimento de pacotes ocorre por meio de um arquivo txt. É necessário que o conteúdo do arquivo contenha um Header, e que a porta de destino seja a mesma especificada para a implementação De outra forma, o pacote é descartado.

## Formato do cabeçalho

Os cabeçalhos TCP e UDP são sepadados do payload por meio de duas barras verticais (' || ') antes e depois do cabeçalho. Dentre estas barras, cada campo do cabeçalho é separado por uma única barra vertical (' | ').

Um cabeçalho TCP contém porta de origem, porta de destino, nº de sequência, nº de acknowledgement, tamanho de janela e flags (uma flag ativa tem valor 1, uma flag inativa tem valor 0. As flags implementadas foram ACK (2º bit), SYN (5º bit), e FIN (6º bit))

ex.:
||12345|80|70|0|5|000010||

Um cabeçalho UDP contém apenas porta de origem, porta de destino e tamanho do segmento.

ex.:
||12345|80|256||

## Técnicas utilizadas
### Retransmissão rápida
Dentro de transp_server.py, a função listener() lida com os pacotes sendo recebidos, e ao encontrar pacotes cujo nº de sequência seja diferente do nº de acknowledgement, ao invés de confirmar, envia o último acknowledgement em sequência realizado  

### Controle de fluxo
O tamanho da janela é determinado pelo campo w_size do Header TCP (Penúltimo Campo). O receptor receberá até aquele número de segmentos não confirmados

O cliente dentro da função transfer() tem controle dos segmentos que sofrem timeout e dos segmentos que são retornados por transp_server. Desta forma, pode reenviar segmentos caso um segmento enviado sofra timeout, ou um mesmo ACK seja recebido três vezes.

## Execução
### TCP
Configure o local desejado para envio/recebimento dos arquivos em config.txt, em ordem:
<li>Endereço para recebimento de mensagens da camada de aplicação<br>
<li>Endereço para envio de mensagens para camada de aplicação<br>
<li>Endereço para envio de mensagens para camada de rede<br>
<li>Endereço para recebimento de mensagens da camada de rede<br>

Depois basta executar transp_cliente para enviar requisições da camada de aplicação, ou transp_server para receber conexões de outras aplicações.

ex.: 

python3 transp_cliente.py <porta_local> <porta_destino>
python3 transp_server.py <porta_local>

### UDP

Execute udp_cliente para enviar pacotes udp e udp_server para escutar pacotes udp. Os locais utilizados por estes são definidos por meio de variáveis globais:
<li>Endereço para recebimento de mensagens da camada de aplicação (udp_cliente.py): appl_req <br>
<li>Endereço para envio de mensagens para camada de aplicação (udp_servidor.py): appl_req  <br>
<li>Endereço para envio de mensagens para camada de rede: phys_dump <br>
<li>Endereço para recebimento de mensagens da camada de rede: phys_loc <br>
<li>Portas locais e de destino: lcl_port e dst_port

ex.:

python3 udp_cliente.py
python3 udp_server.py

# Camada de Rede
O objetivo desta parte do trabalho diz respeito ao roteamento realizado pela camada de rede da pilha de protocolos TCP/IP.

## Escolhas de projeto
De forma esclarecer algumas padronizações estabelecidas no projeto do grupo, os tópicos abaixo abordam sobre a comunicação entre camadas, bem como a interface disponibilizada pelo código desta camada.


### Comunicação para envio de pacotes
No envio, a camada de transporte constrói um pacote, salvo como TXT e formatado em ASCII, em uma pasta comum a todos os pacotes gerados pela pilha e passa como parâmetro um ou mais caminhos de pacotes a serem enviados na linha de comando de execução do script de rede.

Como resultado, a camada de rede escreve um pacote (também TXT/ASCII) com seu header concatenado no início. O caminho desse 
arquivo é repassado ao chamar a camada física.

### Comunicação para recebimento de pacotes
No recebimento, a camada de física constrói um pacote, salvo como TXT e formatado em ASCII, em uma pasta comum a todos os pacotes gerados pela pilha e passa como parâmetro um o caminho para aquele pacote na linha de comando de execução do script de rede.

Como resultado, a camada de rede escreve um pacote (também TXT/ASCII) sem seu header concatenado no início (logo o primeiro header passa a ser o header de transporte). O caminho desse arquivo é repassado ao chamar a camada física.

### Formato do cabeçalho
O formato do cabeçalho segue n
o seguinte formato:
||ip_origem|ip_destino|checksum||
Com os IPs e checksum separados por barras únicas e o início e fim do pacote demarcados por barras duplas.

## Algoritmo
O algoritmo, tanto para o envio quanto para o recebimento, seguem um mesmo padrão, diferenciando apenas de onde são retirados alguns campos e uma condicional extra (no caso do de recebimento).

No envio, é checado se o endereço de origem (computador atual) e o endereço de destino (pacote HTTP) sob mesma máscara de origem (JSON de configuração) resultam em um mesmo valor. Caso sejam iguais (mesma rede), o nextHop, ou próximo salto, é na realidade o próprio destino (direto). Caso contrário, checa se, dentre a lista de rotas (JSON de configuração), existe uma rota que possua conhecimento daquele IP. Caso exista, o IP da rota que conhece o IP de destino passa a ser o nextHop. Caso não exista nenhum o nextHop é o IP default configurado (JSON de config.). Por fim, o pacote de rede é salvo (TXT/ASCII) com o IP de origem sendo a máquina, o IP de destino sendo o nextHop, a máscara de origem sendo o do arquivo JSON e o checksum sendo gerado a partir do conteúdo do pacote de transporte.

No recebimento, é checado se o endereço de origem (computador atual) e o endereço de destino (pacote físico) são iguais. Caso sejam iguais, o pacote de rede é escrito (sem o cabeçalho de rede) e a camada de transporte é chamada passando o caminho para o pacote salvo. Caso contrário, as mesmas regras de roteamento são seguidas, porém, durante a reescrita do header de rede para reenvio do pacote, o IP de origem permanece o mesmo mas o IP de destino passa a ser no nextHop a partir das configurações daquele PC (arquivo JSON).

## Execução
Para a execução do código basta:

`npm run-script send path [path,...]`
`npm run-script receive path`

