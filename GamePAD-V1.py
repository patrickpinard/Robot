# Auteur : Patrick Pinard 
# Date : 27.1.2019
# Objet : gestion d'un gamepad Logitech pour contrôle du robot
# Version : 0.6  (pas terminé)
# -*- coding: utf-8 -*-

#   Clavier MAC :      
#  {} = "alt/option" + "(" ou ")"
#  [] = "alt/option" + "5" ou "6"
#   ~  = "alt/option" + n    
#   \  = Alt + Maj + / 

import sys
import time
import inputs
import logging
import Robot

#ABS_Z      (rotation de l'épaule)
#ABS_RZ     (flexion de l'épaule)
#ABS_Y      (flexion du coude)
#ABS_HAT0Y  (flexion du poignet)
#ABS_X      (rotation du poignet)
#ABS_HAT0X  (fermeture / ouverture de la pince)

time_to_sleep = 0.5

def stretch(x, in_min, in_max, out_min, out_max):
    x, in_min, in_max, out_min, out_max = map(float, (x, in_min, in_max, out_min, out_max))
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;


def Reset(state):
    if state==1:
        print('Réinitialisation du robot demmarrée')  
        robot.hand.open()
        time.sleep(time_to_sleep)
        robot.hand.close()
        time.sleep(time_to_sleep)
        robot.hand.grip(50)
        time.sleep(time_to_sleep)
        robot.shoulder.flex(90)
        time.sleep(time_to_sleep)
        robot.shoulder.rotate(90)
        time.sleep(time_to_sleep)
        robot.elbow.flex(90)
        print('Robot réinitialisé')     
        logging.info('Robot réinitialisé')
        return

def B1(state):
    if state==1:
        print('BOUTTON 1')
        logging.info("Pression du bouton 1")
    
def B2(state):
    if state==1:
        print('BOUTTON 2')
        logging.info("Pression du bouton 2")

def B3(state):
    if state==1:
        print('BOUTTON 3')
        logging.info("Pression du bouton 3")

def B4(state):
    if state==1:
        print('BOUTTON 4')  
        logging.info("Pression du bouton 4")    

def OpenGrip(state):
    if state==1:
        robot.hand.open()
        print("Ouverture de la pince")
        logging.info("Ouverture de la pince")
    
def B6(state):
    if state==1:
        print('BOUTTON 6')  
        logging.info("Pression du bouton 6")

def CloseGrip(state):
    if state==1:
        robot.hand.close()
        print("Fermeture de la pince")
        logging.info("Fermeture de la pince")
    
def B8(state):
    if state==1:
        print('BOUTTON 8')
        logging.info("Pression du bouton 8")
        
def B9(state):
    if state==1:
        print('BOUTTON 9')
        logging.info("Pression du bouton 9")
    
def B10(state):
    if state==1:
        print('BOUTTON 10')
        logging.info("Pression du bouton 10")

def ABS_Z(state):
    angle = round(stretch(state, 0, 255, 0, 180))
    print("Rotation de l'épaule à : ", angle, " degrés")
    robot.shoulder.rotate(angle)
    logging.info("Rotation de l'épaule de %s" % angle)

def ABS_RZ(state):
    angle = round(stretch(state, 0, 255, 0, 180))
    print('ABS_RZ', state, 'Angle :', angle)
    #logging.info('ABS_RZ")
        
def ABS_X(state):
    angle = round(stretch(state, 0, 255, 0, 180))
    print('Rotation du poignet à :', angle, ' degrés')
    robot.hand.rotate(angle)
    logging.info("Rotation du poignet (ABS_X) de %s" % angle)

def ABS_Y(state):
    angle = round(stretch(state, 0, 255, 0, 180))
    print('Flexion du coude à :', angle, ' degrés')
    robot.elbow.flex(angle)
    logging.info("Flexion du coude (ABS_Y) de %s" % angle)

def ABS_RX(state):
    angle = round(stretch(state, 0, 255, 0, 180))
    print('ABS_RX', state,  'Angle :', angle)
    #logging.info('ABS_RZ")

def ABS_RY(state):
    angle = round(stretch(state, 0, 255, 0, 180))
    print('ABS_RY', state,  'Angle :', angle)
    #logging.info('ABS_RZ")

def ABS_RZ(state):
    angle = round(stretch(state, 0, 255, 0, 180))
    print("Flexion de l'épaule à :", angle, " degrés")
    robot.shoulder.flex(angle)
    logging.info("Flexion de l'épaule à %s degrés " % angle)

def Grip(state):   
    # Ouverture / fermeture de la pince  de +/- 5 pourcent
    percent =robot.hand.servo_grip.current_percent  
    if state==1 and percent<100:
        percent = percent + 5
        print('Ouverture de la pince à :', percent, ' pourcent')
        robot.hand.grip(percent)
        logging.info("Ouverture de la pince à %s" % percent)
        return
    elif state==-1 and percent>5:
        percent = percent - 5
        print('Fermeture de la pince à :', percent, ' pourcent')
        robot.hand.grip(percent)
        logging.info("Fermeture de la pince à %s" % percent)
        return
    elif state==0:
        return
    logging.info("Aucun changement de la pince")

def HandFlex(state):
    # Mouvement du poignet de +/- 5 degrés
    angle = robot.hand.servo_flex.current_angle 
    if state==1 and angle<180:
        angle = angle + 5
        print('Flexion du poignet à :', angle, ' degrés')
        robot.hand.flex(angle)
        logging.info("Flexion du poignet de %s" % angle)
        return
    elif state==-1 and angle>0:
        angle = angle - 5
        print('Flexion du poignet à :', angle, ' degrés')
        robot.hand.flex(angle)
        logging.info("Flexion du poignet de %s" % angle)
        return
    elif state==0:
        logging.info("Aucun changement de flexion du poignet")   
        return


event_lut = {
    'BTN_TRIGGER'   : Reset,            
    'BTN_THUMB'     : B2,           
    'BTN_THUMB2'    : B3,           
    'BTN_TOP'       : B4,           
    'BTN_TOP2'      : OpenGrip,           
    'BTN_PINKIE'    : B6,           
    'BTN_BASE'      : CloseGrip,           
    'BTN_BASE2'     : B8,           
    'BTN_BASE3'     : B9,           
    'BTN_BASE4'     : B10,          
    'ABS_Z'         : ABS_Z,
    'ABS_RZ'        : ABS_RZ,
    'ABS_X'         : ABS_X,
    'ABS_Y'         : ABS_Y,
    'ABS_RX'        : ABS_RX,
    'ABS_RY'        : ABS_RY,
    'ABS_HAT0X'     : Grip,
    'ABS_HAT0Y'     : HandFlex,
}

#ABS_Z      (rotation de l'épaule/BASE)
#ABS_RZ     (flexion de l'épaule)
#ABS_Y      (flexion du coude)
#ABS_HAT0Y  (flexion du poignet)
#ABS_X      (rotation du poignet)
#ABS_HAT0X  (fermeture / ouverture de la pince)

def event_loop(events):
    '''
    This function is called in a loop, and will get the events from the
    controller and send them to the functions we specify in the `event_lut`
    dictionary
    '''
    for event in events:
        #print(event.state)
        call = event_lut.get(event.code)
        if callable(call):
            call(event.state)


if __name__ == '__main__':
    
    pads = inputs.devices.gamepads

    if len(pads) == 0:
        raise Exception("Couldn't find any Gamepads!")

    robot = Robot.Build("myRobot")
  
    try:
        while True:
            event_loop(inputs.get_gamepad())
    except KeyboardInterrupt:
        del robot
        print("Bye!")
