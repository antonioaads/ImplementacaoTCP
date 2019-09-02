#!/bin/bash
   
readonly PduFisica=PduFisicaRecebida.txt
readonly PduFisicaRede=PduFisicaRede.txt
readonly PortaServico=7000
readonly FileLog=servidor.log

enviaLog(){
    echo -n $(date) >> ${FileLog};
    echo ": CAMADA FISICA: $*" >> ${FileLog};
    echo "$*";
}

enviaLog "Esperando conexão..."
nc -l -p $PortaServico -w 5 > $PduFisica

pdu=$(cat ${PduFisica});
enviaLog "PDU Recebida $pdu"

enviaLog "Decodificando a PDU..."

macDestinoLido=${pdu:0:48}
macOrigemLido=${pdu:48:48}
macOrigem=$(echo "obase=16; ibase=2; $macOrigemLido" | bc)
macOrigem=$(echo ${macOrigem:0:2}":"${macOrigem:2:2}":"${macOrigem:4:2}":"${macOrigem:6:2}":"${macOrigem:8:2}":"${macOrigem:10:2})
macDestino=$(echo "obase=16; ibase=2; $macDestinoLido" | bc)
macDestino=$(echo ${macDestino:0:2}":"${macDestino:2:2}":"${macDestino:4:2}":"${macDestino:6:2}":"${macDestino:8:2}":"${macDestino:10:2})

enviaLog "MAC Address Origem: $macOrigem"
enviaLog "MAC Address Destino: $macDestino"

tamanhoPayloadLido=${pdu:96:16}
tamanhoPayload=$(echo "obase=10; ibase=2; $tamanhoPayloadLido" | bc)
tamanhoPayloadBits=$(echo $tamanhoPayload*8 | bc)

enviaLog "Tamanho do Payload: $tamanhoPayload" 

payloadLido=${pdu:112:$tamanhoPayloadBits}
payload=$(echo $payloadLido | perl -lpe '$_=pack"B*",$_')

enviaLog "Payload: $payload"

enviaLog "Criado PDU para camada de rede..."

$(echo $payload > $PduFisicaRede)

enviaLog "PDU Criada, fim do serviço."
	