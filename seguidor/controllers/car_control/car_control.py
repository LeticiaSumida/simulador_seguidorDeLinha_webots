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
camera.enable(timestep)
width = camera.getWidth()
height = camera.getHeight()

VEL = 1.0
KP = 0.01
FRAMES_PARAR = 5
sem_linha = 0

while robot.step(timestep) != -1:

    image = camera.getImage()
    frame = np.frombuffer(image, np.uint8).reshape((height, width, 4))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)

    linha = gray[height // 2:, :]
    _, binaria = cv2.threshold(linha, 80, 255, cv2.THRESH_BINARY_INV)

    m = cv2.moments(binaria)

    if m["m00"] > 0:
        sem_linha = 0
        centro = m["m10"] / m["m00"]
        erro = centro - width / 2

        motorE.setVelocity(VEL + KP * erro)
        motorD.setVelocity(VEL - KP * erro)
    else:
        sem_linha += 1
        if sem_linha >= FRAMES_PARAR:
            motorE.setVelocity(0.0)
            motorD.setVelocity(0.0)

    cv2.imshow("Camera", cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR))
    cv2.imshow("Linha", binaria)
    cv2.waitKey(1)