# Auteur    : Patrick Pinard
# Date      : Janvier 2019
# Objet     : gestion en angle ou pourcent du servo-moteur
# Version   : 1
# -*- coding: utf-8 -*-

#   Clavier MAC :      
#  {} = "alt/option" + "(" ou ")"
#  [] = "alt/option" + "5" ou "6"
#   ~  = "alt/option" + n    
#   \  = Alt + Maj + / 
  
# import Adafruit_PCA_9685    (si connecté)
import logging

class Servo:

    """
    Classe definissant un servo moteur caracterise par :
        - name : nom du senseur, permet de localiser celui-ci 
        - pwm : création du servo moteur sur le PCA9685
        - min_pulse : valeur minimale de durée de la pulse (0..4096). Futaba S3003 = 550
        - max_pulse : valeur maximale de durée de la pulse (0..4096). Futaba S3003 = 2330
        - current_pulse: valeur actuelle de la pulse du servo moteur
        - current_angle : 90° par defaut (centre, position milieu)
        - current_percent : 50% par default (centre)
        - channel : numero du canal sur le PCA9685
        - freq : frequence du servo moteur (par défaut 50Hz)
        -  exemple avec	min_min: 550 et max_puls: 2330
                %   °   pulse lenght	
                0%	0	550
                25%	45	995
                50%	90	1440
                75%	135	1885
                100%	180	2330

    """

    def __init__(self, name, channel):
        """
        Constructeur de la classe Servo.
        """
    
        #self.pwm = Adafruit_PCA_9685.PCA9685()
        
        logging.info('Démarrage de la création du "%s"', name)
        self.name = name
        self.min_pulse = 550                                                        
        self.max_pulse = 2330                                                        
        self.current_pulse =  (self.max_pulse - self.min_pulse)/2 + self.min_pulse 
        self.current_angle = 90
        self.current_percent = 50
        self.channel = channel                                                      
        self.freq = 50                                                              
        #self.pwm.set_freq(self.freq)                                                
        #self.pwm.set_pwm(self.channel, 0, current_pulse)                            
        logging.info('Création du "%s" terminée', self.name)
        logging.debug('%s créé avec pulse min : %s  pulse max : %s sur le canal %s du PCA9685 avec fréquence %s.' %(self.name, (self.min_pulse), (self.max_pulse), (self.channel), (self.freq)))
       
        return

    def __repr__(self):
        """
        Méthode permettant d'afficher les paramètres d'un servo moteur
        """
        return "\nSERVO::name  : {}\n  min_pulse    : {}\n  max_pulse    : {}\n  curr_pulse   : {}\n  curr_angle   : {}\n  curr_percent : {}\n  channel      : {}\n  frequency    : {}".format(self.name,self.min_pulse,self.max_pulse,self.current_pulse, self.current_angle, self.current_percent, self.channel, self.freq)

    def __del__(self):
        """
        Méthode permettant d'effacer un servo moteur
        """ 
        del self
        return

    def move(self):
        """
        Méthode permettant de déplacer le servo moteur 
        """
        if self.current_pulse > self.max_pulse or self.current_pulse < self.min_pulse:
            print("pulse value {0} out of servo range.".format(self.current_pulse))
            logging.error('Déplacement du %s avec une longueur de pulse de %s' % (self.name, self.current_pulse))
            return
        #self.pwm.set_pwm(self.channel, 0, self.current_pulse)
        logging.debug('Déplacement du %s avec une longueur de pulse de %s' % (self.name, self.current_pulse))
        return
        
    def move_to_angle(self, angle):
        """
        Méthode permettant de déplacer le servo moteur d'un angle compris entre 0 et 180°
        0° = self.min_pulse   /   180° = self.max_pulse
        """
        if angle > 180 or angle < 0:
            logging.error('Déplacement du %s à un angle de %s degrés pas possible' % (self.name, angle))
            return
        pulse = int(((angle/180) * (self.max_pulse - self.min_pulse)) + self.min_pulse)
        self.current_pulse = pulse
        self.current_angle = angle
        self.current_percent = int((angle/180)*100) 
        self.move()
        logging.info('Déplacement du %s à un angle de %s (°)' %(self.name, str(self.current_angle)))
        return


    def move_to_percent(self, percent):
        """
        Méthode permettant de déplacer le servo moteur d'un angle compris entre 0 et 100&
        """
        if percent > 100 or percent < 0:
            logging.error("Déplacement du %s de %s pourcent pas possible" % (self.name,percent))
            return
        self.current_pulse = int(((percent/100) * (self.max_pulse - self.min_pulse)) + self.min_pulse)
        self.current_percent = percent
        self.current_angle = int(180* (percent/100))
        self.move()
        logging.info("Déplacement du %s à %s pourcent" %(self.name, str(self.current_percent)))
        return

    def reset(self):
        """
        Méthode permettant de réinitialiser le servo moteur
        """
        
        #self.pwm.set_pwm(self.channel,0, 0)
        self.current_pulse = 0
        self.current_percent = 0
        self.current_angle = 0
        logging.info('Réinitialisation du %s' % self.name)
        return


