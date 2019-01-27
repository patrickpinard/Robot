# Auteur : Patrick Pinard - 2019
# Objet : gestion d'un robot 6 axes avec un joystick Logitech. Configuration dans fichier "config.ini"
# Version : 1
# -*- coding: utf-8 -*-

import RobotV3 as Robot

if __name__ == '__main__':
    robot = Robot.Build("myRobot")
    robot.hand.open()
    robot.hand.close()
    robot.hand.rotate(45)
    robot.hand.flex(10)
    robot.elbow.flex(30)
    robot.shoulder.flex(20)
    robot.shoulder.rotate(75)
    print(robot)
    del robot