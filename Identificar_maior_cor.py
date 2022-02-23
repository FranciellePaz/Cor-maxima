from sys import builtin_module_names
import cv2
import numpy as np 

#lower = {'red': (166, 84,141), 'blue':(97, 100, 117), 'yellow': (23, 59, 119)}
#upper = {'red': (186, 255, 255), 'blue': (117, 255, 255),'yellow': (54, 255, 255) }


#Função para redimensionar a imagem 
def redim(img, largura):
    alt = int(img.shape[0]/img.shape[1]*largura)
    img = cv2.resize(img, (largura, alt), interpolation = cv2.cv2.INTER_AREA)
    return img 

#Função que retorna a cor com maior quantidade de número de pixels 
def máximo(pred, pblue, pgreen):
    if pred > pblue and pred > pgreen:
        return "red"
    if pblue > pred and pblue > pgreen:
        return "blue"
    if pgreen > pred and pgreen > pblue:
        return "green"

camera = cv2.VideoCapture(0)

while True:
    (sucesso, frame) = camera.read()
    if not sucesso:
        break
    frame = redim(frame, 320)
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    kernel = np.ones((9,9), np.uint8)
#mascara de vermelho 
    mask1 = cv2.inRange(frame_hsv,(166, 84,141), (186, 255, 255))
#mascara de azul
    mask2 = cv2.inRange(frame_hsv, (99, 100, 117), (117, 255, 255))
#mascara de verde
    mask3 = cv2.inRange(frame_hsv,(36, 0, 0), (75, 255,255))
    mask0 = cv2.bitwise_or(mask1, mask2)
    mask = cv2.bitwise_or(mask0, mask3)
#tirar ruido
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
#retorno o numero de pixels de cada mascara colorida
    pred = cv2.countNonZero(mask1)
    pblue = cv2.countNonZero(mask2)
    pgreen = cv2.countNonZero(mask3)

    print(máximo(pred,pblue, pgreen))

    cv2.imshow('Tracking', redim(frame, 640))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break 

camera.release()
cv2.destroyAllWindows()
