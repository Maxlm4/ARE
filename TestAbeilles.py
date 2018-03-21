import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.animation as anim

N=100 #taille de la région étudiée (côté en m, donc 1 hectare)
Nb_ruches=4 #nombre de  ruches
Liste_ruches=[] #liste des coordonnées de chaque rûche
for i in range(Nb_ruches):
    x=np.random.choice(N)
    x0 = x % N
    y=np.random.choice(N)
    y0 = y % N              #coordonnées de la rûche
    Liste_ruches.append((x0,y0))
Info_ruches=[] #Toutes les informations sur chaque ruche
Nb_abeilles=30000 #nombre initial d'abeilles dans la ruche
Nb_ab_dedans=Nb_abeilles #nombre d'abeiles dans la rûche
Nb_but_dehors=0  #nombre de butineuses hors de la ruche
reperage=0 #nombre de zones florales découvertes
liste_reper=[] #liste des zones florales découvertes
distance=0 #distance initiale du repérage par rapport à la ruche
Nb_zones=25 #nombre de zones florales à découvrir
Arrivée=0 #0 signifie que les butineuses partent, 1 qu'elles butinent et 2 qu'elles rentrent à la rûche et 3 qu'elles sont dans la rûche
Nb_groupes=0 #nombre de groupe de butineuses
T_groupe=0 #Taille des groupes de butineuses
qtt_miel=10000000 #qantité de miel dans la rûche en mg
taux_mort=121 #nombre de secondes avant la mort d'une abeille (naturellement), obtenu en divisant l'espérance de vie d'une abeille par le nombre d'abeilles
Liste_direct=[] #Liste des directions à prendre pour aller vers une fleur
Temps_recolte_passe=0 #temps réeelement passé par les butineuses sur les fleurs actuellement
for i in Liste_ruches:
    x0,y0=i
    Info_ruches.append((x0,y0,Nb_abeilles,Nb_ab_dedans,Nb_but_dehors,reperage,liste_reper,distance,Nb_zones,Arrivée,Nb_groupes,T_groupe,Liste_direct,Temps_recolte_passe,qtt_miel))
nb_steps=5000 #nombre d'images total
Nb_zone_fleur= 200 #nombre de zones florales
liste_zone_fleur=[] #liste des coordonnées des zones florales
while len(liste_zone_fleur)<Nb_zone_fleur:
    x=np.random.choice(N)
    x1 = x % N
    y=np.random.choice(N)
    y1 = y % N
    if (x1,y1) not in liste_zone_fleur and (x1,y1) not in Liste_ruches:
        liste_zone_fleur.append((x1,y1))
taux_nat=57 #nombre de secondes avant une naissance
s=0 #nombre de secondes écoulées
j=0 #nombre de jours écoulés
saison='printemps' #saison de départ
Temps_interrecolte=3720 #nombre de secondes entre chaque récolte
Temps_recolte=600 #temps à butiner
Nb_abeilles_tot=Nb_ruches*Nb_abeilles #nombre total d'abeilles dans la région
Liste_Nb_abeilles_tot=[Nb_abeilles_tot]




terrain=np.zeros([N,N])

for k in Info_ruches:
    x0,y0,Nb_abeilles,_,_,_,_,_,_,_,_,_,_,_,_=k
    terrain[x0][y0]=Nb_abeilles


results=[]
results.append(terrain.copy())

def simulation():
    global s
    global Temps_recolte
    global Temps_interrecolte
    global Info_ruches
    global taux_nat
    global taux_mort
    global saison
    global Nb_ruches

    for i in range(nb_steps):
        Nb_abeilles_tot=0
        s=s+1

        if s==86400: #une journée écoulée
            j=j+1
            s=0
            if j==91: #une saison écoulée
                Ab_tot=Liste_Nb_abeilles_tot[nb_steps-1]
                if saison=='printemps':
                    taux_nat=216
                    saison='été'
                    taux_mort=abs(3628800/(AB_tot/Nb_ruches))#esprérance de vie de 42 jours par le nombre d'abeilles moyen dans une  ruche
                elif saison=='été':
                    saison='automne'
                    taux_mort=abs(17280000/(AB_tot/Nb_ruches)) #esprérance de vie de 200 jours par le nombre d'abeilles moyen dans une  ruche
                elif saison=='automne':
                    taux_nat=144
                    saison='hiver'
                    taux_mort=abs(3628800/(AB_tot/Nb_ruches)) #esprérance de vie de 42 jours par le nombre d'abeilles moyen dans une  ruche
                elif saison=='hiver':
                    taux_nat=57
                    saison='printemps'
                    taux_mort=abs(3628800/(AB_tot/Nb_ruches)) #esprérance de vie de 42 jours par le nombre d'abeilles moyen dans une  ruche
                j=0
                    

        
        Info_ruches_copy=[]
        for k in Info_ruches:
            x0, y0, Nb_abeilles, Nb_ab_dedans, Nb_but_dehors, reperage, liste_reper, distance, Nb_zones, Arrivée, Nb_groupes, T_groupe, Liste_direct, Temps_recolte_passe,qtt_miel=k


            if s==60000: #Au bout d'un certain temps, les abeilles vont consommer le miel
                qtt_miel=qtt_miel-3*Nb_abeilles-14000 # 3mg mangés par chaque abeille, 14g utilisés pour la production de cire


            if s/taux_mort==int(s/taux_mort): #mort d'une abeille naturelle
                Nb_abeilles=Nb_abeilles-1
                Nb_ab_dedans=Nb_ab_dedans-1
                terrain[x0][y0]=Nb_ab_dedans

            
            if s/taux_nat==int(s/taux_nat):                 #naissance d'une abeille
                Nb_abeilles=Nb_abeilles+1
                Nb_ab_dedans=Nb_ab_dedans+1
                terrain[x0][y0]=Nb_ab_dedans

                                  
            if reperage<Nb_zones:
                liste_repera=liste_reper.copy()
                distance=distance+1
                for j in range(-distance,distance+1):
                    for k in range(-distance,distance+1):               #zone de repérage carrée autour de la ruche
                        if j==-distance or j==distance or k==-distance or k==distance: #zone encore inexplorée
                            if (j+x0,k+y0) in liste_zone_fleur:
                                reperage=reperage+1
                                liste_repera.append((j+x0,k+y0))
                liste_reper=liste_repera.copy()
            if reperage>=Nb_zones:
            
                if Nb_but_dehors==0 and Arrivée==0 and s<=43200: #Avant que la moitié de la journée soit écoulée
                    Nb_butineuses=abs(Nb_abeilles/2)
                    Nb_groupes=reperage #nombre de groupe de butineuses
                    T_groupe=abs(Nb_butineuses/Nb_groupes) #nombre d'abeilles dans un groupe
                    Liste_direct=[] #liste des directions pour chaque groupe
                    for k in range(Nb_groupes):
                        Liste_direct.append(((x0,y0),liste_reper[k]))
                    Nb_but_dehors=Nb_butineuses
                    Nb_ab_dedans=Nb_ab_dedans-Nb_but_dehors
                
                elif Nb_but_dehors!=0:
                    if Arrivée==0:
                        Liste_dir=[]
                        for k in Liste_direct:
                            (a,b), (c,d)= k
                            if (a,b)!=(c,d):
                                terrain[a][b]=terrain[a][b]-T_groupe
                                action=0
                                while action!=2 and (a,b)!=(c,d):
                                    if abs(a-c)>abs(b-d):
                                        if a-c>0:
                                            a=a-1
                                        elif a-c<0:
                                            a=a+1
                                    elif abs(a-c)<abs(b-d):
                                        if b-d>0:
                                            b=b-1
                                        elif b-d<0:
                                            b=b+1
                                    elif abs(a-c)==abs(b-d):
                                        if a-c<0 and b-d<0:
                                            a=a+1
                                            b=b+1
                                        elif a-c<0 and b-d>0:
                                            a=a+1
                                            b=b-1
                                        elif a-c>0 and b-d>0:
                                            a=a-1
                                            b=b-1
                                        elif a-c>0 and b-d<0:
                                            a=a-1
                                            b=b+1
                                    action=action+1
                                terrain[a][b]=terrain[a][b]+T_groupe
                            Liste_dir.append(((a,b),(c,d)))
                        Liste_direct=Liste_dir.copy()
                        valid=0 #permet de vérifier si toutes les abeilles sont arrivées à destination
                        for k in Liste_direct:
                            (a,b),(c,d)=k
                            if (a,b)==(c,d):
                                valid=valid+1
                        if valid == len(Liste_direct):
                            Arrivée=1
                            for k in Liste_direct:
                                (a,b),(c,d)=k
                                crabe_araignée=np.random.choice(100) #probabilité qu'un crabe araignée se situe dans cette zone et mange une abeille
                                if crabe_araignée==50:
                                    terrain[a][b]=terrain[a][b]-1
                                    Nb_but_dehors=Nb_but_dehors-1
                                    Nb_abeilles=Nb_abeilles-1
                                  
                                  
                    elif Arrivée==1:
                        Temps_recolte_passe=Temps_recolte_passe+1
                        if Temps_recolte_passe==Temps_recolte:
                            Temps_recolte_passe=0
                            Arrivée=2
                            Liste_dir=[]
                            for k in Liste_direct:
                                (a,b),(c,d)=k
                                Liste_dir.append(((a,b),(x0,y0)))
                            Liste_direct=Liste_dir.copy()
                    elif Arrivée==2:
                        Liste_dir=[]
                        for k in Liste_direct:
                            (a,b), (c,d)= k
                            if (a,b)!=(c,d):
                                terrain[a][b]=terrain[a][b]-T_groupe
                                action=0
                                while action!=2 and (a,b)!=(c,d):
                                    if abs(a-c)>abs(b-d):
                                        if a-c>0:
                                            a=a-1
                                        elif a-c<0:
                                            a=a+1
                                    elif abs(a-c)<abs(b-d):
                                        if b-d>0:
                                            b=b-1
                                        elif b-d<0:
                                            b=b+1
                                    elif abs(a-c)==abs(b-d):
                                        if a-c<0 and b-d<0:
                                            a=a+1
                                            b=b+1
                                        elif a-c<0 and b-d>0:
                                            a=a+1
                                            b=b-1
                                        elif a-c>0 and b-d>0:
                                            a=a-1
                                            b=b-1
                                        elif a-c>0 and b-d<0:
                                            a=a-1
                                            b=b+1
                                    action=action+1
                                terrain[a][b]=terrain[a][b]+T_groupe
                            Liste_dir.append(((a,b),(c,d)))
                        Liste_direct=Liste_dir.copy()
                        valid=0 #permet de vérifier si toutes les abeilles sont arrivées à destination
                        for k in Liste_direct:
                            (a,b),(c,d)=k
                            if (a,b)==(c,d):
                                valid=valid+1
                        if valid == len(Liste_direct):
                            Arrivée=3
                            Nb_ab_dedans=Nb_ab_dedans+Nb_but_dehors
                            qtt_miel=qtt_miel+13*Nb_but_dehors #chaque abeille ramène 13 mg de miel
                            if qtt_miel>30000000: #capacité de miel maximum dans une rûche en mg
                                qtt_miel=30000000
                            Nb_but_dehors=0
                elif Arrivée==3 and Nb_but_dehors==0:
                    Temps_recolte_passe=Temps_recolte_passe+1
                    if Temps_recolte_passe==Temps_interrecolte:
                        Temps_recolte_passe=0
                        Arrivée=0
                
                    
            Info_ruches_copy.append((x0,y0,Nb_abeilles,Nb_ab_dedans,Nb_but_dehors,reperage,liste_reper,distance,Nb_zones,Arrivée,Nb_groupes,T_groupe,Liste_direct,Temps_recolte_passe,qtt_miel))
            Nb_abeilles_tot=Nb_abeilles_tot+Nb_abeilles
        Liste_Nb_abeilles_tot.append(Nb_abeilles_tot)
        Info_ruches=Info_ruches_copy.copy()
        results.append(terrain.copy())
    return(results,Liste_Nb_abeilles_tot)
 
results,_=simulation()

    
fig = plt.figure()

# results[i] contient l'état au pas de temps i sous forme de matrice
im = plt.imshow(results[0], animated=True)

def updatefig(i):

    im.set_array(results[i+1])
    
    return im,

ani = anim.FuncAnimation(fig, updatefig, frames=1000, interval=50, blit=True)

plt.show()
