# Auteur  : Patrick Pinard 
# Date    : Janvier 2019
# Objet   : Création d'un robot avec pince, main, coude et épaule depuis un fichier "config.ini"
# Version : 0.8  (pas terminé)

# -*- coding: utf-8 -*-

#   Clavier MAC :      
#  {} = "alt/option" + "(" ou ")"
#  [] = "alt/option" + "5" ou "6"
#   ~  = "alt/option" + n    
#   \  = Alt + Maj + / 
  

import Servo
import configparser
import logging
import sys
import time

# Chargement de la configuration du robot depuis le fichier "config.ini"

configuration_file = "config.ini"
config = configparser.ConfigParser() 
config.read(configuration_file) 

# Information des servo-moteurs connectés à la carte PWM (PCA9685) 
SHOULDER_FLEX_SERVO_ID   = config.get('servo','SHOULDER_FLEX_SERVO_ID')
SHOULDER_ROTATE_SERVO_ID = config.get('servo','SHOULDER_ROTATE_SERVO_ID')
ELBOW_FLEX_SERVO_ID      = config.get('servo','ELBOW_FLEX_SERVO_ID')
WRIST_FLEX_SERVO_ID      = config.get('servo','WRIST_FLEX_SERVO_ID') 
WRIST_ROTATE_SERVO_ID    = config.get('servo','WRIST_ROTATE_SERVO_ID') 
GRIP_SERVO_ID            = config.get('servo','GRIP_SERVO_ID')

# Configuration du logging
LOGFILENAME              = config.get('logging','LOGFILENAME')
LOGLEVEL                 = config.get('logging','LOGLEVEL')
FILEMODE                 = config.get('logging','FILEMODE')

# LOG LEVEL = Critical, Error, Warning, Info, Debug, Not Set

logging.basicConfig(filename=LOGFILENAME, filemode=FILEMODE, level=LOGLEVEL, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('------------- { start logging ROBOT } -------------')

class Hand:

    """
    Classe definissant la main du robot.
    """


    def __init__(self, name, channel_grip, channel_rotate, channel_flex):
        """
        Constructeur de la classe main (hand) constitué d'un poignet (wrist) et d'une pince (grip). 
        """
        logging.info('Construction de %s' % name)
        self.name   = name
        self.servo_rotate = Servo.Servo("Servo pour rotation du poignet (WRIST_rotate)", channel_rotate)
        self.servo_flex   = Servo.Servo("Servo pour flexion du poignet (WRIST_flex)", channel_flex)
        self.servo_grip   = Servo.Servo("Servo pour pince (GRIP)", channel_grip)
        return

    def __repr__(self):
        """
        Méthode permettant d'afficher les paramètres d'une main
        """
        return "\nHAND::{0}\n{1}\n{2}\n{3}\n".format(self.name, self.servo_rotate, self.servo_flex, self.servo_grip) 
    

    def __del__(self):
        """
        Méthode permettant d'effacer une main
        """
        logging.info('Suppression de %s' % self.name)
        del self
        return

    def open(self):
        """
        Méthode permettant d'ouvrir la pince à 100%
        """
        logging.info('Ouvertue du "%s" à 100 pourcent' % (self.servo_grip.name))
        self.servo_grip.move_to_percent(100)
        return

    def close(self):
        """
        Méthode permettant de fermer la pince complètement
        """
        logging.info('Fermeture du "%s" à 0 pourcent' % (self.servo_grip.name))
        self.servo_grip.move_to_percent(0)
        return

    def grip(self, percent):
        """
        Méthode permettant de d'ouvrir la pince à un certain pourcentage
        """
        logging.info('"%s" ouverte a %s pourcent' % (self.servo_grip.name, str(percent)))
        self.servo_grip.move_to_percent(percent)
        return

    def rotate(self,angle):
        """
        Méthode permettant de de faire tourner le poignet d'un certain angle 
        """
        logging.info('Rotation du "%s" a un angle de %s degrés' % (self.servo_rotate.name, str(angle)))
        self.servo_rotate.move_to_angle(angle)
        return

    def flex(self, angle):
        """
        Méthode permettant de monter/descendre le poignet d'un certain angle
        """
        logging.info('Flexion du "%s" a un angle de %s degrés' % (self.servo_flex.name, str(angle)))
        self.servo_flex.move_to_angle(angle)
        return


class Elbow:

    """
    Classe definissant un coude (elbow) du robot avec flexion uniquement.
    """

    def __init__(self, name, channel_flex):
        """
        Constructeur du coude (elbow)  
        """
        logging.info('Construction du coude de %s' % name)
        self.name   = name
        self.servo_flex   = Servo.Servo("Servo pour flexion du coude (ELBOW_flex)", channel_flex)
        return

    def __repr__(self):
        """
        Méthode permettant d'afficher les paramètres de coude
        """
        return "\nELBOW::{0}\n{1}\n".format(self.name, self.servo_flex) 
    

    def __del__(self):
        """
        Méthode permettant d'effacer le coude
        """
        logging.info('Suppression du coude de %s' % self.name)
        del self
        return

   
    def flex(self, angle):
        """
        Méthode permettant de flechir le coude d'un certain angle
        """
        logging.info('Flexion du coude de "%s" à un angle de %s degrés' % (self.name, angle))
        self.servo_flex.move_to_angle(angle)
        return



class Shoulder:

    """
    Classe definissant une épaule (Shoulder).
    """


    def __init__(self, name, channel_flex, channel_rotate):
        """
        Constructeur de l'épaule (shoulder)  
        """
        logging.info("Démarrage de la construction de l'épaule de %s" % name)
        self.name   = name
        self.servo_flex   = Servo.Servo("Servo pour flexion de l'épaule (SHOULDER_flex)", channel_flex)
        self.servo_rotate   = Servo.Servo("Servo pour rotation de l'épaule (SHOULDER_rotate)", channel_rotate)
        logging.info('Construction épaule de %s terminée' % self.name)
        return

    def __repr__(self):
        """
        Méthode permettant d'afficher les paramètres de l'épaule
        """
        return "\nSHOULDER::{0}\n{1}\n{2}\n".format(self.name, self.servo_flex, self.servo_rotate) 
    

    def __del__(self):
        """
        Méthode permettant d'effacer l'épaule
        """
        logging.info("Suppression de l'épaule de %s" % self.name)
        del self
        return

   
    def flex(self, angle):
        """
        Méthode permettant de flechir l'épaule  d'un certain angle
        """
        logging.info("Flexion de l'épaule de %s à un angle de %s degrés" % (self.name, str(angle)))
        self.servo_flex.move_to_angle(angle)
        return

    def rotate(self,angle):
        """
        Méthode permettant de de faire tourner l'épaule d'un certain angle 
        """
        logging.info("Rotation de l'épaule avec le %s à un angle de %s degrés" % (self.servo_rotate.name, str(angle)))
        self.servo_rotate.move_to_angle(angle)
        return
        

class Build:

    """
    Classe definissant une main de robot caracterise par :
        - name : nom du robot
        - hand : la main composée du poignet et de la pince
        - elbow : le coude
        - shoulder : l'épaule
        - les paramètres du robot sont définis dans le fichier de configuration "config.ini"
        """


    def __init__(self, name):
        """
        Constructeur de la classe. 
        """
        logging.info('----------[ Construction de %s ]------------------' % name) 
        self.name = name
        self.hand = Hand(name, GRIP_SERVO_ID, WRIST_ROTATE_SERVO_ID, WRIST_FLEX_SERVO_ID)   
        self.elbow = Elbow(name, ELBOW_FLEX_SERVO_ID) 
        self.shoulder = Shoulder(name, SHOULDER_FLEX_SERVO_ID, SHOULDER_ROTATE_SERVO_ID) 
        logging.info('------[ Fin de construction de %s ]---------------' % self.name)  
        return

    def __repr__(self):
        """
        Méthode permettant d'afficher les paramètres du robot
        """
        return "{0} {1} {2}".format(self.hand, self.elbow, self.shoulder) 
    

    def __del__(self):
        """
        Méthode permettant d'effacer une main
        """
        logging.info("Suppression de %s" % self.name)  
        del self
        return

    
