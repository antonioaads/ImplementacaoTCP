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

`python3 transp_cliente.py <porta_local> <porta_destino>`

`python3 transp_server.py <porta_local>`

### UDP

Execute udp_cliente para enviar pacotes udp e udp_server para escutar pacotes udp. Os locais utilizados por estes são definidos por meio de variáveis globais:
<li>Endereço para recebimento de mensagens da camada de aplicação (udp_cliente.py): appl_req <br>
<li>Endereço para envio de mensagens para camada de aplicação (udp_servidor.py): appl_req  <br>
<li>Endereço para envio de mensagens para camada de rede: phys_dump <br>
<li>Endereço para recebimento de mensagens da camada de rede: phys_loc <br>
<li>Portas locais e de destino: lcl_port e dst_port

ex.:

`python3 udp_cliente.py`
`python3 udp_server.py`

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

#Camada Fisica 
A ideia dessa parte da documentação é exclarecer algumas lógicas que foram utilizadas devido a escolhas que o grupo adotou, conforme citado expecificamente abaixo:

### Comunicação com a camada fisica

Para a comunicação de alguma outra camada, com a camada física, utilizou-se um arquivo .txt. No exemplo, chamamos esse arquivo de PduRedeFisica.txt, para deixar claro que seria uma PDU que está sendo passada da camada de rede (ainda não implementada) para a camada física. 

O formato desse arquivo é bem simples, sendo a primeira linha o IP de destino e a segunda linha o payload que deverá ser enviado.

### Conversão de dados para binário

Para manter uma melhor representação da mensagem no texto binário, atitude que simplifica e minimiza erros na hora de converter para *string* novamente, utilizou-se formas diferentes conforme o que queria-se enviar, sendo:

#### MAC Address

Para as conversões do MAC Address, utilizou-se uma função desenvolvida pelo grupo, que procura cada caracter hexadecimal e substitui por sua representação em 4 bits. Fez-se dessa forma para manter o padrão da PDU que será enviada, conforme definido no enunciado. 

Não utilizou-se conversão pela calculadora ou de outras formas, pois precisávamos dessa precisão na quantidade de bits, para que a maquina de destino conseguisse traduzir essa mensagem de maneira correta.

#### Tamanho do payload

Para o tamanho do payload, também é necessário preocuparmos com a quantidade de bits, pois para essa informação, a PDU deverá ter exatamente 2 bytes, ou seja, 16 bits. Pelo mesmo motivo citado acima, não pode-se utilizar funções prontas disponíveis no SO, pois essas normalmente não fixam bits a esquerda, então, por exemplo, o inteiro na base 1 seria representado na base binaria também como 1, representação que por sua vez é errônea, pois, para o modelo de PDU utilizada, a representação correta seria 0000000000000001. 

Para solucionar esse problema, convertemos o tamanho do payload da base decimal para a base hexadecimal, fixando 4 digitos para esse representação, através da função printf("%04x", tamanhoPayload), que transforma, 1(base 10) em 0001(base hexadecimal).

#### Payload 

Para converter o payload, utilizou-se um comando em *perl*, que de maneira simples e clara converte caracteres ASCII em byte.

### Conversão de dados para hexadecimal e ASCII

#### MAC ADDRESS e tamanho do payload

Devido as peculiaridades adotadas anteriormente, temos um modelo binário muito bem definido, então, par voltar para qualquer outra representação, sendo ela decimal ou hexadecimal, foi só utilizar a função ("obase=BaseDestino; ibase=2; numeroParaConverter" | bc), substituindo onde esta BaseDestino para 10 (decimal) ou para 16 (hexadecimal).

#### Payload

Para o payload, utilizou a função inversa da utilizada na conversão, também em *perl*. Escolhemos por essa solução devido a facilidade e a clareza do código.

### Envio da PDU

Para envio da PDU, utilizou-se a ferramenta disponível no linux, NetCat, conforme foi utilizado e detalhadamente explicado na tarefa anterior, que era apenas enviar um arquivo de um PC para outro. Caso tenha alguma dúvida quanto a essa parte, basta consulta o [link](https://github.com/antonioaads/CEFET-MG/tree/master/EngenhariaComputacao/6_Semestre/Redes/EnviarArquivoUsandoShellScript).

## Enunciado

Deverá ser usado o TCP em sua implementação com um código cliente-servidor para fazer a transferência entre os dois hosts. O Quadro Ethernet a ser enviado deverá estar dentro de um arquivo txt, cujo conteúdo serão os bits que o formam seguindo a definição a seguir, baseada na RFC (https://tools.ietf.org/html/rfc895). 

Neste caso teremos duas PDUs a serem apresentadas por esta camada, a PDU original, proveniente dos dados da camada superior e a PDU convertida para bits, a qual deverá ser entregue ao host de destino. Camada física recebe da camada superior a mensagem a ser trocada e o endereço (IP) do destinatário. Assim, deverá descobrir o MAC Address para preencher o quadro com esta informação, para isso, fará uso do protocolo ARP (ou comando ARP na linha de comando). 

Deverá ser implementada a probabilidade de uma colisão, ou seja, a cada envio de PDU de um lado para outro, deverá ser gerado um número aleatório que, se dentro de uma faixa de valores, considera-se que houve colisão para se esperar um tempo aleatório e depois reenviar o quadro.

A camada física deverá funcionar

**Algoritmo:**
1. *Remetente:* verifica se há colisão (probabilidade). Se sim, aguarda tempo aleatório, senão envia.
2. *Remetente:* envia quadro (fragmentação, se necessária, será realizada posteriormente pela camada de rede)
3. *Destinatário:* recebe quadro, remove cabeçalho e encaminha payload para a camada superior

*Formato da PDU original:*

* 6 bytes       - MAC Destino         - 41:7f:33:0e:65:b2
* 6 bytes       - MAC Origem          - 41:7f:83:e8:5e:ff
* 2 bytes       - Tamanho do payload  - 8
* 0-1500 bytes  - Payload             - sandrord

*Formato da PDU em bits:*
01000001011111110011001100001110011001011011001000000000000010000111001101100001011011100110010001110010011011110111001001100100

*Padrão de conversão:*
Endereço MAC é separado por “:”, que é ignorado na conversão para binário
Endreeço MAC é convertido de hexa para binário por grupos de 1 byte
Valor em Tamanho do payload é convertido em campo de 2 bytes
Payload é convertido de ascii para binário
