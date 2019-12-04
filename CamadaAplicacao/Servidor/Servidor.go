package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

func EscreveMensagem(filename string) {

	Mensagem, err := os.Create("../../CamadaAplicacao/Servidor/Mensagem-Enviar.txt") //Irei colocar o conteudo do arquivo a ser enviado aki
	if err != nil {

		fmt.Println(err)
	}

	http := "HTTP/1.0 200 OK"
	Content_Type := "text/file"
	Content_Length := len(filename)
	Expires := "Thu, 01 Dec 2022 16:00:00 GMT"
	Last_Modified := "Wed, 1 May 2019 12:45:26 GMT"
	Server := " Apache 0.84"
	Mensagem.WriteString(http + "\n" + Content_Type + "\n" + strconv.Itoa(Content_Length) + "\n" + Expires + "\n" + Last_Modified + "\n" + Server + "\n")

	file, erro := os.OpenFile(filename, os.O_RDWR, 0755)
	if erro != nil {
		log.Fatalf("\n Falha ao abrir o arquivo em esrever")
	}
	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)
	var txtlines []string

	for scanner.Scan() {
		txtlines = append(txtlines, scanner.Text())
	}
	file.Close()

	for _, eachline := range txtlines {
		l, err := Mensagem.WriteString(eachline)
		if err != nil {
			fmt.Println(err)
			fmt.Println(l)
			Mensagem.Close()
		}
	}
}
func BytesDoArquivo(fileName string) {
	//Le todo arquvio que contem o nome do arquivo solicitado
	f, _ := os.Open(fileName)
	scanner := bufio.NewScanner(f)
	scanner.Split(bufio.ScanBytes)
	resultado := ""
	var linha = 0
	for scanner.Scan() {

		b := scanner.Bytes()
		if string(b) == "\n" {
			linha++
		}
		if linha == 3 {
			if string(b) != "\n" {

				resultado = fmt.Sprintf("%s%s", resultado, string(b))
			}
		}
	}

	EscreveMensagem(resultado)
}
func main() {

	BytesDoArquivo("Mensagem.txt")

}
