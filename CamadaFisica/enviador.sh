#!/bin/bash

#Setar o IP que irá enviar
ipEnvio=172.16.127.51

#Setar a porta que irá enviar
portaEnvio=7000

#Setar o nome que terá o arquivo recebido
nomeArquivo=arquivoParaEnvio.txt

#Chama o NetCat passando os parâmetros através 
#das variáveis de ambiente criadas
echo "Enviando para " $ipEnvio " na porta " $portaEnvio " ..." 
nc $ipEnvio $portaEnvio < $nomeArquivo

#Imprime mensagem (ainda não fazendo tratamento)
echo "Arquivo enviado com sucesso"

