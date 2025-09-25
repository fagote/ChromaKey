import cv2
import numpy as np

def create_mask(hsv_frame, color="green"):
    if color == "green":
        # Faixa do verde (matiz ~100° no HSV, mas no OpenCV vai de 0 a 179)
        lower = np.array([35, 40, 40])   # limite inferior (H, S, V)
        upper = np.array([85, 255, 255]) # limite superior
    elif color == "blue":
        # Faixa do azul marinho (mais escuro que o azul padrão)
        lower = np.array([90, 50, 20])
        upper = np.array([130, 255, 150])
    else:
        raise ValueError("Cor inválida: use 'green' ou 'blue'")

    # Cria a máscara
    mask = cv2.inRange(hsv_frame, lower, upper)
    return mask

def main():
    # Carregar a imagem local (a pessoa com fundo verde ou azul)
    frame = cv2.imread("imagem.jfif")
    if frame is None:
        print("Erro: não consegui carregar a imagem. Verifique o caminho.")
        return

    # Pré-carregar imagens de fundo
    backgrounds = [
        cv2.imread("fundo1.jfif"),
        cv2.imread("fundo2.jfif"),
        cv2.imread("fundo3.jfif"),
    ]
    current_bg = 0  # índice do fundo atual

    # Define cor inicial (verde)
    chroma_color = "green"

    while True:
        # Converte para HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Cria máscara da cor escolhida
        mask = create_mask(hsv, color=chroma_color)

        # Inverte a máscara para pegar a pessoa/objeto
        mask_inv = cv2.bitwise_not(mask)

        # Redimensiona o fundo para o tamanho da imagem principal
        bg_resized = cv2.resize(backgrounds[current_bg], (frame.shape[1], frame.shape[0]))

        # Separa a parte da pessoa (sem o fundo verde/azul)
        fg = cv2.bitwise_and(frame, frame, mask=mask_inv)

        # Separa a parte do fundo (somente onde tinha verde/azul)
        bg = cv2.bitwise_and(bg_resized, bg_resized, mask=mask)

        # Junta pessoa + fundo
        result = cv2.add(fg, bg)

        # Mostra os frames
        cv2.imshow("Original", frame)
        cv2.imshow("Mascara", mask)
        cv2.imshow("Chroma Key", result)

        # Controles do teclado
        key = cv2.waitKey(0) & 0xFF
        if key == 27:  # tecla ESC -> sair
            break
        elif key in [ord("1"), ord("2"), ord("3")]:
            current_bg = int(chr(key)) - 1  # troca fundo
        elif key == ord("g"):
            chroma_color = "green"  # trocar para verde
        elif key == ord("b"):
            chroma_color = "blue"   # trocar para azul

    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()