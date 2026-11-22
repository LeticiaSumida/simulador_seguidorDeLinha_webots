
from controller import Robot
import cv2
import numpy as np

robot = Robot()
timestep = int(robot.getBasicTimeStep())

motorE = robot.getDevice('motorE')
motorD = robot.getDevice('motorD')

motorE.setPosition(float('inf'))
motorD.setPosition(float('inf'))

camera = robot.getDevice('camera')
camera.enable(64)

while robot.step(timestep) != -1:

    image = camera.getImage()

    width = camera.getWidth()
    height = camera.getHeight()

    frame = np.frombuffer(image, np.uint8).reshape((height, width, 4))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    linha = gray[int(height * 0.50):height, :]

    _, imagem_binaria = cv2.threshold(
        linha, 80, 255, cv2.THRESH_BINARY_INV
    )

    momentos = cv2.moments(imagem_binaria)

    if momentos["m00"] > 0:

        centro = int(momentos["m10"] / momentos["m00"])
        meio = width // 2

        if centro < meio - 10:
            motorE.setVelocity(0.5)
            motorD.setVelocity(1.0)

        elif centro > meio + 10:
            motorE.setVelocity(1.0)
            motorD.setVelocity(0.5)

        else:
            motorE.setVelocity(1.0)
            motorD.setVelocity(1.0)

    else:
            motorE.setVelocity(0.0)
            motorD.setVelocity(0.0)

    cv2.imshow("Camera", frame)
    cv2.imshow("Linha", imagem_binaria)
    cv2.waitKey(1)

cv2.destroyAllWindows()
