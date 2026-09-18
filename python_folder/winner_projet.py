from random import *
import random
message=""
result=[]
ticket_gagner=[]
mise=1
ticket_par_jour=5
nombre_de_match=365*ticket_par_jour
cote_total=1
times=1
"""
app furtears
app asks :
-mise
-nombre d'équipes

publication :
estimation :
si on joue tous les jour ce jeux pendant 1 mois  une année
on va gagner combien ou perdre combien 
après combien de tentative et temps si on joue 3 tickets par jour que l'on espère gagner 
la chance de gagner 


"""


def main():
    global mise,times
    mise=int(input("veillez saisir votre mise : "))
    times=int(input("veillez saisir le nombre d'équipe : "))
    plays(times)
    publication_masuelle()
 

def play(choice):
    score=randint(0,2)
    if choice==score or score==0:
        return True
    return False




def plays(times):
    global cote_total
    for i in range(times):
        choice=randint(1,2)
        result.append(play(choice))
        value=random.choice([1.50,1.56])
        cote_total=cote_total*value
        
        # cote_total=cote_total*randint(2,3)

def check_result(result):
     if False in result : 
        
         return False
     else : 
        
         ticket_gagner.append(calcul_gain()) 
         return True
     

def calcul_gain():
    global cote_total
    gain =mise*cote_total
    cote_total=1
    return gain



# def publication():
#      if ticket_gagner :
#          for ticket in ticket_gagner:
#             print(f"vous avez gagné {ticket}\n")
#      else: print("aucun ticket gagné")
#      print(result)



def publication_masuelle():
    mise_totale=mise*nombre_de_match
    message = """
    Statistique Mensuelle :
    -----------------------
    """

    for i in range(nombre_de_match) :
        global result,cote_total
        plays(times)
        check_result(result)
        result.clear()
        cote_total=1

 
    if ticket_gagner :
         somme_totale=0
         for ticket in ticket_gagner:
            somme_totale+=ticket
         msg= f"Benefice de {somme_totale-mise_totale}" if somme_totale-mise_totale>0 else f"Perdue {somme_totale-mise_totale}"
         print(f" {message}\n Nombre des tickets total: {nombre_de_match}\n les nombres des tickets gagnés: {len(ticket_gagner)}\nles nombres des tickets echoués : {nombre_de_match-len(ticket_gagner)}\nla sommes totale gagnée :{somme_totale}\nla sommes totale mise: {mise_totale}\n {msg}")

    else: 
        print(f"{message} \n aucun ticket gagné \n l'argent perdue {mise_totale} ")
        
    
main()