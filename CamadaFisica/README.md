# Implementar a camada Física da pilha TCP

O objetivo dessa parte do trabalho, é implementar a camada física da pilha TCP respeitando as diretrizes estabelecidas no enunciado do trabalho, conforme cópia no final desse README:

## Escolhas de projeto

A ideia dessa parte da documentação é exclarecer algumas lógicas que foram utilizadas devido a escolhas que o grupo adotou, conforme citado expecificamente abaixo:

### Comunicação com a camada fisica

Para a comunicação de alguma outra camada, com a camada física, utilizou-se um arquivo .txt. No exemplo, chamamos esse arquivo de PduRedeFisica.txt, para deixar claro que seria uma PDU que está sendo passada da camada de rede (ainda não implementada) para a camada física. 

O formato desse arquivo é bem simples, sendo a primeira linha o IP de destino e a segunda linha o payload que deverá ser enviado.

### Conversão de dados para binário

Para manter uma melhor representação da mensagem no texto binário, atitude que simplifica e minimiza erros na hora de converter para *string* novamente, utilizou-se formas diferentes conforme o que queria-se enviar, sendo:

#### MAC Address

Para as conversões do MAC Address, utilizou-se uma função desenvolvida pelo grupo, que procura cada caracter hexadecimal e substitui por sua representação em 4 bits. Fez-se dessa forma para manter o padrão da PDU que será enviada, conforme definido no enunciado. 

Não utilizou-se conversão pela calculadora ou de outras formas, pois precisávamos dessa precisão na quantidade de bits, para que a maquina de destino conseguisse traduzir essa mensagem de maneira correta.

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

