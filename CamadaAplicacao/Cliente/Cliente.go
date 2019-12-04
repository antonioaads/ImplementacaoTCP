package main

import (
	"bufio"
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"
)

var caminho = "Mensagem-Recebida.txt"
var Script = "/media/rodrigo/MULTIBOOT/Transporte-20191202T115133Z-001/Transporte/TCP/transp_cliente.py"

func deletararquivo() {
	// delete file
	var err = os.Remove(caminho)
	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println("Arquivo deletado com sucesso")
}
func main() {

	f, erro := os.OpenFile("Cliente.log", os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0600)
	if erro != nil {
		log.Println(erro)
	}
	defer f.Close()

	logger := log.New(f, "Camada de Aplicacao : Data/Hora : ", log.LstdFlags)

	logger.Println("Iniciando  a Camada de Aplicacao")

	log.Println("Aplicacao  Rodando na porta 8080")

	log.Println("Cliente.log criado")
	http.HandleFunc("/", index)

	err := http.ListenAndServe(":8081", nil)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
		logger.Println("Erro ao iniciar a aplicacao erro : %s", err)
	}
}

func index(w http.ResponseWriter, r *http.Request) {

	switch r.Method {
	case "GET":
		if r.URL.Path != `/favicon.ico` {
			requisicao := r.URL.Path
			requisicao = strings.TrimPrefix(requisicao, "/")

			f, err := os.Create("../../CamadaAplicacao/Cliente/Mensagem.txt")
			if err != nil {
				fmt.Println(err)
			}
			url_nao_pode := `/favicon.ico`

			method := "GET " + requisicao + " HTTP/1.0"
			//fmt.Println(method)
			host := strings.TrimSuffix(r.Host, ":")
			//fmt.Println(host)
			User_Agent := r.Header.Get("User-Agent")
			//fmt.Println(User_Agent)

			cabecalho := method + "\n" + host + "\n" + User_Agent + "\n"
			fmt.Println("Imprimindo o cabecalho da PDU\n", cabecalho, "\n")
			f.WriteString(cabecalho)
			if len(requisicao) > 1 {
				if requisicao != url_nao_pode {
					l, err := f.WriteString(requisicao)
					if err != nil {
						fmt.Println(err)
						fmt.Println(l)
						f.Close()

					}
					f.Close()
					/*
						cmd := exec.Command(Script)
						cmd.Stdin = strings.NewReader("")
						var out bytes.Buffer
						cmd.Stdout = &out
						errt := cmd.Run()
						fmt.Println("Rodando a camada de Transporte")
						if errt != nil {
							fmt.Println("Erro ao abrir o A Camada de Transporte")
							log.Fatal(errt)

						}
					fmt.Printf(" \n", out.String())*/
				}
			}
		}
	}
	for {
		if _, err := os.Stat("Mensagem-Recebida.txt"); err == nil {
			Arquiv_Mostrar, err := os.Create("Mensagem-Mostrar.txt")
			if err != nil {
				fmt.Println(err)
			}

			f, _ := os.Open("Mensagem-Recebida.txt")
			scanner := bufio.NewScanner(f)
			scanner.Split(bufio.ScanBytes)
			resultado := ""
			var linha = 0
			for scanner.Scan() {

				b := scanner.Bytes()
				if string(b) == "\n" {
					linha++
				}
				if linha == 6 {
					if string(b) != "\n" {

						resultado = fmt.Sprintf("%s%s", resultado, string(b))
					}
				}
			}
			l, err := Arquiv_Mostrar.WriteString(resultado)
			if err != nil {
				fmt.Println(err)
				fmt.Println(l)
				f.Close()

			}
			Arquiv_Mostrar.Close()

			http.ServeFile(w, r, "Mensagem-Mostrar.txt")

			deletararquivo()
			break
		}
	}
}
