import cv2
import mediapipe as mp

def distancia_euclidiana(p1, p2):
    d = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    return d

def draw_bounding_box(image, hand_landmarks):
    image_height, image_width, _ = image.shape
    x_min, y_min = image_width, image_height
    x_max, y_max = 0, 0
    
    for landmark in hand_landmarks.landmark:
        x, y = int(landmark.x * image_width), int(landmark.y * image_height)
        if x < x_min: x_min = x
        if y < y_min: y_min = y
        if x > x_max: x_max = x
        if y > y_max: y_max = y
    
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)
with mp_hands.Hands(
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      continue

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    image_height, image_width, _ = image.shape
    if results.multi_hand_landmarks:
        if len(results.multi_hand_landmarks):
            for num, hand_landmarks in enumerate(results.multi_hand_landmarks):
                
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                
                draw_bounding_box(image, hand_landmarks)

                # Obtener coordenadas de los puntos clave
                index_finger_tip = (int(hand_landmarks.landmark[8].x * image_width),
                                int(hand_landmarks.landmark[8].y * image_height))
                index_finger_pip = (int(hand_landmarks.landmark[6].x * image_width),
                                int(hand_landmarks.landmark[6].y * image_height))
                index_finger_mcp = (int(hand_landmarks.landmark[5].x * image_width),
                                int(hand_landmarks.landmark[5].y * image_height))
                
                thumb_tip = (int(hand_landmarks.landmark[4].x * image_width),
                                int(hand_landmarks.landmark[4].y * image_height))
                thumb_pip = (int(hand_landmarks.landmark[2].x * image_width),
                                int(hand_landmarks.landmark[2].y * image_height))
                thumb_mcp = (int(hand_landmarks.landmark[1].x * image_width),
                                int(hand_landmarks.landmark[1].y * image_height))
                
                middle_finger_tip = (int(hand_landmarks.landmark[12].x * image_width),
                                int(hand_landmarks.landmark[12].y * image_height))
                middle_finger_pip = (int(hand_landmarks.landmark[10].x * image_width),
                                int(hand_landmarks.landmark[10].y * image_height))
                middle_finger_mcp = (int(hand_landmarks.landmark[9].x * image_width),
                                int(hand_landmarks.landmark[9].y * image_height))
                
                ring_finger_tip = (int(hand_landmarks.landmark[16].x * image_width),
                                int(hand_landmarks.landmark[16].y * image_height))
                ring_finger_pip = (int(hand_landmarks.landmark[14].x * image_width),
                                int(hand_landmarks.landmark[14].y * image_height))
                
                pinky_tip = (int(hand_landmarks.landmark[20].x * image_width),
                                int(hand_landmarks.landmark[20].y * image_height))
                pinky_pip = (int(hand_landmarks.landmark[18].x * image_width),
                                int(hand_landmarks.landmark[18].y * image_height))
                
                wrist = (int(hand_landmarks.landmark[0].x * image_width),
                                int(hand_landmarks.landmark[0].y * image_height))
                
                ring_finger_pip2 = (int(hand_landmarks.landmark[5].x * image_width),
                                int(hand_landmarks.landmark[5].y * image_height))
                
                ring_finger_mcp = (int(hand_landmarks.landmark[13].x * image_width),
                                int(hand_landmarks.landmark[13].y * image_height))

                pinky_mcp = (int(hand_landmarks.landmark[17].x * image_width),
                             int(hand_landmarks.landmark[17].y * image_height))

                # Mantener las condiciones existentes para A-F
                if abs(thumb_tip[1] - index_finger_pip[1]) <45 \
                    and abs(thumb_tip[1] - middle_finger_pip[1]) < 30 and abs(thumb_tip[1] - ring_finger_pip[1]) < 30\
                    and abs(thumb_tip[1] - pinky_pip[1]) < 30:
                    cv2.putText(image, 'A', (700, 150), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                3.0, (0, 0, 255), 6)
                    
                elif index_finger_pip[1] - index_finger_tip[1]>0 and pinky_pip[1] - pinky_tip[1] > 0 and \
                    middle_finger_pip[1] - middle_finger_tip[1] >0 and ring_finger_pip[1] - ring_finger_tip[1] >0 and \
                        middle_finger_tip[1] - ring_finger_tip[1] <0 and abs(thumb_tip[1] - ring_finger_pip2[1])<40:
                    cv2.putText(image, 'B', (700, 150), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                3.0, (0, 0, 255), 6)
                    
                elif abs(index_finger_tip[1] - thumb_tip[1]) < 360 and \
                    index_finger_tip[1] - middle_finger_pip[1]<0 and index_finger_tip[1] - middle_finger_tip[1] < 0 and \
                        index_finger_tip[1] - index_finger_pip[1] > 0:
                   cv2.putText(image, 'C', (700, 150), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                3.0, (0, 0, 255), 6)
                
                # Letra D
                elif index_finger_pip[1] - index_finger_tip[1] > 0 and \
                     middle_finger_pip[1] - middle_finger_tip[1] < 0 and \
                     ring_finger_pip[1] - ring_finger_tip[1] < 0 and \
                     pinky_pip[1] - pinky_tip[1] < 0 and \
                     abs(thumb_tip[0] - index_finger_tip[0]) < 50:
                    cv2.putText(image, 'D', (700, 150), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                3.0, (0, 0, 255), 6)
                
                # Letra E
                elif index_finger_pip[1] - index_finger_tip[1] < 0 and \
                     middle_finger_pip[1] - middle_finger_tip[1] < 0 and \
                     ring_finger_pip[1] - ring_finger_tip[1] < 0 and \
                     pinky_pip[1] - pinky_tip[1] < 0 and \
                     thumb_tip[1] < index_finger_mcp[1]:
                    cv2.putText(image, 'E', (700, 150), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                3.0, (0, 0, 255), 6)
                
                # Letra F
                elif  pinky_pip[1] - pinky_tip[1] > 0 and middle_finger_pip[1] - middle_finger_tip[1] > 0 and \
                    ring_finger_pip[1] - ring_finger_tip[1] > 0 and index_finger_pip[1] - index_finger_tip[1] < 0 \
                        and abs(thumb_pip[1] - thumb_tip[1]) > 0 and distancia_euclidiana(index_finger_tip, thumb_tip) <65:

                    cv2.putText(image, 'F', (700, 150), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                3.0, (0, 0, 255), 6)
                # Mantener otras letras y números...

                # OK modificado - ahora verifica la posición horizontal y vertical
                elif distancia_euclidiana(thumb_tip, index_finger_tip) < 50 and \
                     middle_finger_pip[1] - middle_finger_tip[1] > 0 and \
                     ring_finger_pip[1] - ring_finger_tip[1] > 0 and \
                     pinky_pip[1] - pinky_tip[1] > 0 and \
                     thumb_tip[0] > index_finger_mcp[0]:  # Asegura que el pulgar esté a la derecha
                    cv2.putText(image, 'OK', (700, 150), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                3.0, (0, 255, 0), 6)

                # PAUSE modificado - usa distancias entre dedos y posiciones relativas
                elif index_finger_pip[1] - index_finger_tip[1] < -30 and \
                     middle_finger_pip[1] - middle_finger_tip[1] < -30 and \
                     ring_finger_pip[1] - ring_finger_tip[1] > 0 and \
                     pinky_pip[1] - pinky_tip[1] > 0 and \
                     abs(index_finger_tip[0] - middle_finger_tip[0]) < 50 and \
                     abs(index_finger_tip[1] - middle_finger_tip[1]) < 50 and \
                     thumb_tip[1] > index_finger_mcp[1]:  # Pulgar debajo de los dedos extendidos
                    cv2.putText(image, 'PAUSE', (700, 150), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                3.0, (0, 255, 0), 6)
                # Número 1    
                elif index_finger_pip[1] - index_finger_tip[1] > 0 and \
                     middle_finger_pip[1] - middle_finger_tip[1] < 0 and \
                     ring_finger_pip[1] - ring_finger_tip[1] < 0 and \
                     pinky_pip[1] - pinky_tip[1] < 0 and \
                     thumb_tip[0] < index_finger_mcp[0]:  # Pulgar hacia dentro
                    cv2.putText(image, '1', (700, 150), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                3.0, (0, 0, 255), 6)
                    
                # Número 2
                elif index_finger_pip[1] - index_finger_tip[1] > 0 and \
                     middle_finger_pip[1] - middle_finger_tip[1] > 0 and \
                     ring_finger_pip[1] - ring_finger_tip[1] < 0 and \
                     pinky_pip[1] - pinky_tip[1] < 0 and \
                     thumb_tip[1] > middle_finger_mcp[1]:  # Pulgar doblado
                    cv2.putText(image, '2', (700, 150), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                3.0, (0, 0, 255), 6)
                
                # Número 3
                elif index_finger_pip[1] - index_finger_tip[1] > 0 and \
                     middle_finger_pip[1] - middle_finger_tip[1] > 0 and \
                     ring_finger_pip[1] - ring_finger_tip[1] > 0 and \
                     pinky_pip[1] - pinky_tip[1] < 0 and \
                     thumb_tip[1] > ring_finger_mcp[1]:  # Pulgar doblado
                    cv2.putText(image, '3', (700, 150), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                3.0, (0, 0, 255), 6)

                elif index_finger_pip[1] - index_finger_tip[1] > 0 and \
                     middle_finger_pip[1] - middle_finger_tip[1] > 0 and \
                     ring_finger_pip[1] - ring_finger_tip[1] > 0 and \
                     pinky_pip[1] - pinky_tip[1] > 0 and \
                     thumb_tip[1] > pinky_mcp[1]:
                    cv2.putText(image, '4', (700, 150), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                3.0, (0, 0, 255), 6)

                # Número 5
                elif index_finger_pip[1] - index_finger_tip[1] > 0 and \
                     middle_finger_pip[1] - middle_finger_tip[1] > 0 and \
                     ring_finger_pip[1] - ring_finger_tip[1] > 0 and \
                     pinky_pip[1] - pinky_tip[1] > 0 and \
                     thumb_tip[1] < pinky_pip[1]:
                    cv2.putText(image, '5', (700, 150), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                3.0, (0, 0, 255), 6)  

                

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
cv2.destroyAllWindows()