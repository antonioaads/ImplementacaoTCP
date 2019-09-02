#!/bin/bash

readonly PduRedeFisica=PduRedeFisica.txt    
readonly PduFisica=PduFisica.txt
readonly IpServidor=127.0.0.1
readonly PortaServidor=7000
readonly FileLog=cliente.log

enviaLog(){
    echo -n $(date) >> ${FileLog};
    echo ": CAMADA FISICA: $*" >> ${FileLog};
    echo "$*";
}

hex2Bin(){
    a=$*;   
    a=$(echo ${a//0/0000});
    a=$(echo ${a//1/0001});
    a=$(echo ${a//2/0010});
    a=$(echo ${a//3/0011});
    a=$(echo ${a//4/0100});
    a=$(echo ${a//5/0101});
    a=$(echo ${a//6/0110});
    a=$(echo ${a//7/0111});
    a=$(echo ${a//8/1000});
    a=$(echo ${a//9/1001});
    a=$(echo ${a//a/1010});
    a=$(echo ${a//b/1011});
    a=$(echo ${a//c/1100});
    a=$(echo ${a//d/1101});
    a=$(echo ${a//e/1110});
    a=$(echo ${a//f/1111});
    a=$(echo ${a//A/1010});
    a=$(echo ${a//B/1011});
    a=$(echo ${a//C/1100});
    a=$(echo ${a//D/1101});
    a=$(echo ${a//E/1110});
    a=$(echo ${a//F/1111});

    echo $a;
}

enviaLog "Lendo a PDU"

ipDestino=$(cat ${PduRedeFisica} | head -1 | tail -1);
payload=$(cat ${PduRedeFisica} | head -2 | tail -1);

enviaLog "Ip destino é: ${ipDestino}"; 
enviaLog "Mensagem de payload é: ${payload}";

macOrigem=$(cat /sys/class/net/$(ip route show default | awk '/default/ {print $5}')/address)

enviaLog "O MAC Address de origem é: ${macOrigem}"; 

if [ "$IpServidor" == "localhost" ] || [ "$IpServidor" == "127.0.0.1" ]; then
    macDestino=$macOrigem;
    enviaLog "A comunicação está sendo feita na mesma máquina"
else
    macDestino=$(arp ${IpServidor} -a | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}')
fi

enviaLog "O MAC Address destino é: ${macDestino}"

macDestinoEnviar=$(hex2Bin $(echo ${macDestino} | tr -d ':'))
macOrigemEnviar=$(hex2Bin $(echo ${macOrigem} | tr -d ':'))

tamanhoPayload=$(echo $payload | wc -c)
tamanhoPayload=$(echo $tamanhoPayload-1 | bc -l)
tamanhoPayload=$(printf "%04x" $tamanhoPayload)
tamanhoPayloadEnviar=$(hex2Bin $tamanhoPayload)
payloadEnviar=$(echo $payload | perl -lpe '$_=unpack"B*"')

enviaLog "Montando PDU para envio"

$(echo $macDestinoEnviar$macOrigemEnviar$tamanhoPayloadEnviar$payloadEnviar > $PduFisica)

pduGerado=$(cat $PduFisica)

enviaLog "O PDU gerado foi: $pduGerado"

enviaLog "Tentando enviar a pdu"

tentativa=$(( ( RANDOM % 10 )  + 1 ));
while [ $((${tentativa})) -le 5 ]; do
    tentativa=$(( ( RANDOM % 10 )  + 1 ));
    enviaLog "Erro ao enviar, nova tentativa em $tentativa segundos..."
    sleep $tentativa
done

enviaLog "Enviando a pdu"

nc $IpServidor $PortaServidor < $PduFisica

enviaLog "PDU Enviada"	