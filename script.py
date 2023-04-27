import cv2 as cv

#Captuto o vídeo dentro da variavel vídeo
video = cv.VideoCapture("pedra-papel-tesoura.mp4")

#Criação de algumas variaveis para utilizar no código
contadorFrames = 0
maoEsquerda = ""
maoDireita = ""
movimentoAnteriorDireita = ""
movimentoAnteriorEsquerda = ""
placar = [0,0]

#Função para encontrar as mãos no código
def encontraMaos():
    #Utilização das variaveis globais
    global contadorFrames
    global maoEsquerda
    global maoDireita
    
    #Contando a quantidade de frames e transformandos os em GRAY para que o matchtemplete possa encontrar
    contadorFrames += 1
    frame_gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)

    #Logica para encontrarmos as mãos
    if (contadorFrames == 10):
        contadorFrames = 0
        maoDireita = encontraMaoDireita(frame_gray)
        maoEsquerda = encontraMaoEsquerda(frame_gray)

    #Pegando os resultados das mãos e encontrando quem venceu
    resultadoMaoDireita, resultadoMaoEsquerda = encontrandoVencedor(maoDireita, maoEsquerda)

    #Calculando o placar
    calculoPlacar(resultadoMaoDireita, resultadoMaoEsquerda)
    #Imprime o placar no vídeo
    cv.putText(frame, "Jogador 1 placar: " + str(placar[0]), (300, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv.LINE_AA)
    cv.putText(frame, "Jogador 2 placar: " + str(placar[1]), (800, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv.LINE_AA)

#Função para podermos encontrar as jogadas da mão direita
def encontraMaoDireita(frame_gray):
    #Encontrando tesoura
    tesoura = cv.imread('tesoura_mao_direita.png', 0)
    encontraTesoura = cv.matchTemplate(frame_gray, tesoura, cv.TM_SQDIFF_NORMED).max()
    #Encontrando pedra
    pedra = cv.imread('pedra_mao_direita.png', 0)
    encontraPedra = cv.matchTemplate(frame_gray, pedra, cv.TM_SQDIFF_NORMED).max()
    #Fazendo a logica para reconhecer se for pedra, tesoura ou papel.
    if(encontraPedra > 0.2 and encontraPedra < 0.21):
        return "Pedra"
    if (encontraTesoura > 0.2194):
        return "Tesoura"
    else:
        return "Papel"

#Função para podermos encontrar as jogadas da mão esquerda
def encontraMaoEsquerda(frame_gray):
    #Encontrando tesoura
    tesoura = cv.imread('tesoura_mao_esquerda.png', 0)
    encontraTesoura = cv.matchTemplate(frame_gray, tesoura, cv.TM_SQDIFF_NORMED).max()
    #Encontrando pedra
    pedra = cv.imread('pedra_mao_esquerda.png', 0)
    encontraPedra = cv.matchTemplate(frame_gray, pedra, cv.TM_CCOEFF_NORMED).max()
    #Fazendo a logica para reconhecer se for pedra, tesoura ou papel.
    if(encontraPedra < 0.40):
        return "Pedra"
    elif(encontraTesoura > 0.21):
        return "Tesoura"
    else:
        return "Papel"

#Logica para encontrar o jogador que ganhou a rodada
def encontrandoVencedor(maoDireita, maoEsquerda):

    #Logica do empate
    if(maoDireita == maoEsquerda):
        cv.putText(frame, str("Empatou"), (800, 300), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2, cv.LINE_AA)
        cv.putText(frame, str(maoEsquerda), (350, 200), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv.LINE_AA)
        cv.putText(frame, str(maoDireita), (1100, 200), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv.LINE_AA)
        return "Empate", "Empate"
    
     #Logica jogador 2 ganhou
    elif(maoDireita == "Pedra" and maoEsquerda == "Tesoura"):
        cv.putText(frame, str("Jogador 2 ganhou"), (500, 300), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv.LINE_AA)
        cv.putText(frame, str("Tesoura"), (350, 200), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv.LINE_AA)
        cv.putText(frame, str("Pedra"), (1100, 200), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv.LINE_AA)
        return "Perdedor", "Ganhador"
    
    #Logica jogador 2 ganhou
    elif (maoDireita == "Papel" and maoEsquerda == "Pedra"):
        cv.putText(frame, str("Jogador 2 ganhou"), (500, 300), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv.LINE_AA)
        cv.putText(frame, str("Papel"), (350, 200), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv.LINE_AA)
        cv.putText(frame, str("Papel"), (1100, 200), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv.LINE_AA)
        return "Perdedor", "Ganhador"
    
    #Logica jogador 2 ganhou
    elif (maoDireita == "Tesoura" and maoEsquerda == "Papel"):
        cv.putText(frame, str("Jogador 2 ganhou"), (500, 300), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv.LINE_AA)
        cv.putText(frame, str("Papel"), (350, 200), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv.LINE_AA)
        cv.putText(frame, str("Tesoura"), (1100, 200), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv.LINE_AA)
        return "Perdedor", "Ganhador"
    
    #Logica jogador 1 ganhou
    elif (maoDireita == "Pedra" and maoEsquerda == "Papel"):
        cv.putText(frame, str("Jogador 1 ganhou"), (500, 300), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv.LINE_AA)
        cv.putText(frame, str("Papel"), (350, 200), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv.LINE_AA)
        cv.putText(frame, str("Pedra"), (1100, 200), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv.LINE_AA)
        return "Ganhador", "Perdedor"
    
    #Logica jogador 1 ganhou
    elif (maoDireita == "Papel" and maoEsquerda == "Tesoura"):
        cv.putText(frame, str("Jogador 1 ganhou"), (500, 300), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv.LINE_AA)
        cv.putText(frame, str("Tesoura"), (350, 200), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv.LINE_AA)
        cv.putText(frame, str("Papel"), (1100, 200), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv.LINE_AA)
        return "Ganhador", "Perdedor"
    
    #Logica jogador 1 ganhou
    elif (maoDireita == "Tesoura" and maoEsquerda == "Pedra"):
        cv.putText(frame, str("Jogador 1 ganhou"), (500, 300), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv.LINE_AA)
        cv.putText(frame, str("Pedra"), (350, 200), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv.LINE_AA)
        cv.putText(frame, str("Tesoura"), (1100, 200), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv.LINE_AA)
        return "Ganhador", "Perdedor"
    #Logica jogada não identificada

    else:
        cv.putText(frame, str("Jogada não identificada"), (500, 300), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv.LINE_AA)
        return "Não identificado", "Não identificado"

#Função para calcular o placar do jogo
def calculoPlacar(resultadoMaoDireita, resultadoMaoEsquerda):

    #Pegando as variaveis globais criadas no inicio
    global placar
    global maoDireita
    global maoEsquerda
    global movimentoAnteriorDireita
    global movimentoAnteriorEsquerda

    #Logica para a pontuação do placar
    if not maoDireita == movimentoAnteriorDireita or not maoEsquerda == movimentoAnteriorEsquerda:
        #Mão esquerda pontuou
        if resultadoMaoEsquerda == "Ganhador":
            placar[1] += 1
        #Mão direita pontuou
        elif resultadoMaoDireita == "Ganhador":
            placar[0] += 1
        movimentoAnteriorDireita = maoDireita
        movimentoAnteriorEsquerda = maoEsquerda

#Pegando os frames do vídeo
if video.isOpened():
    ret, frame = video.read()
else:
    ret = False

#While para rodar o vídeo e fechar ele com o Q
while ret:
    encontraMaos()
    cv.imshow("Scrpt", frame)

    ret, frame = video.read()
    if cv.waitKey(1) & 0xFF == ord('q'): break

video.release()
cv.destroyAllWindows()