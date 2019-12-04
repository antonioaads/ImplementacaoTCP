#udpclient

import sys
import random as rd
import time
import os
import udpfunctions as up
import textwrap as tw

#ENDEREÇOS
appl_req = "AplServer/mensagem.txt"
phys_dump = "TranspClient/Segment.txt"
phys_loc = "TranspServer/Segment.txt"

#VARIAVEIS DE CONTROLE
seg_size = 16
lcl_port = 80
dst_port = 0
timeout = 5

while True:
    data = 0
    a = up.safe_get(phys_loc)
    if(a != 0): print(a.head.dst_port)
    if(a != 0 and a.head.dst_port == lcl_port):
        dst_port = a.head.dst_port
        print("Incoming")
        data = a.data
        counter = 0
        start_time = time.time()
        while counter-start_time < timeout:
            a = up.safe_get(phys_loc)
            if a == 0:
                counter = time.time()
            else:
                data+=a.data
                start_time = time.time()
        with open(appl_req, "w") as f:
            print(data)
            f.write(data)
        print("Dava saved")
    else:
        print('waiting', end='\r')