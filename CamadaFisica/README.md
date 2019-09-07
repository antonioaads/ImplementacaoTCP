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

