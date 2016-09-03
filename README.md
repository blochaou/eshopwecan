# eshopwecan
E-commerce avec des produits Amazon prêts à vendre
##Objectifs
1. S'initer au e-commerce avant de s'engager dans un grand projet en ligne
2. Vendre en ligne sans gérer les stocks , la livraison et les retours
3. Gagner de l'argent avec les commissions Amazon
4. Démarrer votre propre activité de vente en ligne

## Prérequis
1. Python 3.5
2. Pip 3.5
3. [Compte Amazon Partenaire](https://partenaires.amazon.fr/)

## Installation
1. Créer un répertoire nommé myproject  
    *mkdir myproject*  
2. Naviguer dans le répertoire myproject  
    *mv myproject*  
3. Créer un environnement virtuel nommé env  
    *virtualen env*  
4. cloner le echopwecan  
    *git clone https://github.com/blochaou/eshopwecan*  
  
Après l'installation , la structure de votre répertoire doit se présentée comme suit:    
>myproject  
    >env  
    >eshopwecan 

Activer votre environnement virtuel  
*source env\bin\activate*  
Naviguer dans le répertoire eshopwecan  
*mv eshopwecan*  
Installer tous les packages dans le fichiers requirements  
*pip3.5 install -r requirements.txt*

## Configuration
Naviguer dans le répertoire eshopwecan  
*mv eshopwecan*  
Ouvrez le fichier settings.py et modifier les valeurs  
#### Paramètres Amazon
AMAZON_ACCESS_KEY = ''  
AMAZON_SECRET_KEY = ''  
AMAZON_ASSOC_TAG = ''  
#### Paramètres du site
Le nom du site  
EWC_APP_NAME = ''  
Votre slogan  
EWC_APP_SLOGAN=''

##Execution
Revenir dans le répertoire myproject/eshopwecan  
Démarrer votre application  
python3.5 manage.py runserver 0.0.0.0:9000  
Ouvrez votre navigateur et naviguer vers http://127.0.0.1:9000  
Votre site devrait s'ouvrir  

##Exemple de site eshopwecan
[http://www.le24avril.com](http://www.le24avril.com)

##Contributeur
Blochaou Francois

## Support
En cas de souci , veuillez  contacter [BEF Technology Sarl](http://www.bef-technology.com)

## Licence
Copyright © 2016 [BEF Technology Sarl](http://www.bef-technology.com)
