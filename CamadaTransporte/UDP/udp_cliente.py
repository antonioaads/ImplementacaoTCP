#udpclient

import sys
import random as rd
import time
import os
import udpfunctions as up
import textwrap as tw

#ENDEREÇOS
appl_req = "AplClient/mensagem.txt"
phys_dump = "TranspServer/Segment.txt"
phys_loc = "TranspClient/Segment.txt"

#VARIAVEIS DE CONTROLE
seg_size = 256
lcl_port = rd.randint(1024,49151)
dst_port = 80

while True:
    try:
        data = 0
        with open(appl_req, 'r') as g:
            data = g.read()
        #os.remove(appl_req)
        print("Starting with port", lcl_port)
        time.sleep(1)
        segments = tw.wrap(data, seg_size, replace_whitespace=False,drop_whitespace=False)
        for s in segments:
            time.sleep(1)
            a = up.Segment(up.Header(lcl_port, dst_port, len(s)), s)
            up.safe_send(phys_dump, a)
        print("Termino de envio")
        break
    except FileNotFoundError:
        print("waiting", end='\r')