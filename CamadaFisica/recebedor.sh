#!/bin/bash

#Setar a porta que irá escutar
portaEscuta=7000

#Setar o nome que terá o arquivo recebido
nomeArquivo=arquivoParaReceber.txt

#Chama o NetCat passando os parâmetros através 
#das variáveis de ambiente criadas
echo "Escutando na porta " $portaEscuta " ..." 
nc -l -p $portaEscuta -w 5 > $nomeArquivo

#Imprime mensagem (ainda não fazendo tratamento)
echo "Arquivo recebido e nomeado como" $nomeArquivo
echo "Como pode ser viato abaixo:"

ls -l $nomeArquivo

