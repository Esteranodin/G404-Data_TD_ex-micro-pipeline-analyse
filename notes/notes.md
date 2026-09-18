### Notes de nettoyage

![alt text](structure.png)


Le fichier brut reste inchangé, les correctiosn sont faites sur une copie.  
Le fichier nettoyé ne contient que les données pour analyse et aucune durée invalide ne doit entrer dans les calculs.

#### Ligne identique
- même identifiant
- autres valeurs sont les identiques
$\rightarrow$ suppression d'une des deux lignes : si Màj garder la dernière sinon la première écrite.
Ici je décide de conserver la première ligne.
> Conservation d'une trace de la ligne supprimée avec un masque

![alt text](suppression.png)

#### Résumé journal nettoyage :

- valeur vide : exclue ;
- texte non convertible : exclu ;
- valeur négative : corrigée avec sa valeur absolue, car elle est interprétée comme une erreur de saisie.
- normalisation des strings (suppr. espace et bas de casse) pour les canaux
- vérification avec une RegEX des identifiants : TKT-0000

> La ligne source permet une traçabilité et de retrouver la ligne dans le fichier brut  
> Et permet de faire correspondre les première lignes de chaques format : ligne 0 du df -> la 2 du csv (en-tête étant la 1)


#### Valeurs rares :

Une durée élevée n’est pas automatiquement une erreur. Elle peut être inhabituelle mais plausible. Elle est donc conservée et signalée dans l’analyse.

> Les valeurs rares plausibles sont conservées. Elles seront étudiées dans les graphiques et pourront influencer la moyenne, l’écart-type et la forme des distributions.


![alt text](journal.png)



### Notes d'analyse

![alt text](description_base.png)

#### Email

Les durées sont les plus dispersées. La moyenne est beaucoup plus élevée que la médiane :
Cela indique une distribution étirée vers les grandes durées. Plusieurs tickets dépassent 200 minutes, avec des valeurs allant jusqu’à 418 minutes.

Le canal email possède donc un centre comparable aux autres canaux, mais une forme très différente : davantage de valeurs extrêmes et une forte asymétrie vers la droite.

#### Phone

Les durées sont très regroupées autour de 90 minutes. La moyenne et la médiane sont presque identiques, ce qui indique une distribution relativement équilibrée.

C’est le canal le moins dispersé. Les tickets sont généralement compris entre environ 77 et 102 minutes, même si quelques valeurs plus élevées existent.

#### Chat

Les durées sont plus dispersées que pour phone. La médiane est inférieure à la moyenne, ce qui montre que quelques tickets longs tirent la moyenne vers le haut.

La majorité des durées se situe entre environ 60 et 110 minutes, avec quelques valeurs supérieures à 180 minutes.

#### Conclusion 

Les trois canaux ont des durées moyennes proches de 90 minutes. Toutefois, la moyenne seule est insuffisante :

- phone est le canal le plus régulier ;
- chat présente une dispersion intermédiaire ;
- email est le plus variable et contient les durées les plus longues.  

On ne peut donc pas dire que les canaux ont exactement les mêmes performances. Ils ont un centre similaire, mais des dispersions et des valeurs inhabituelles très différentes.