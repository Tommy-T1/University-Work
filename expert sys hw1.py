confess = 1  
keep_q = 0 
result = "" 
pris_A_Con = 0 
pris_B_Con = 0
def pri_delima(pris_A,pris_B):
    if pris_A == confess and pris_B == confess:
        pris_A_Con = 5
        pris_B_Con = 5
    elif pris_A == confess and pris_B == keep_q:
        pris_A_Con = 0
        pris_B_Con = 10
    elif pris_A == keep_q and pris_B == confess:
        pris_A_Con = 10
        pris_B_Con = 0
    elif pris_A == keep_q and pris_B == confess:
        pris_A_Con = 1
        pris_B_Con = 1
    return(pris_B_Con,pris_A_Con)

def sen_time(pris_A_Con,pris_B_con):
    if pris_A_Con == 5 and pris_B_Con == 5:
        result = "Both wil go to jail for 5 years"
    elif pris_A_Con == 0 and pris_B_Con == 10 :
        result = "Prisoner B will go to jail for 10 years, and Prisoner A will go free"
    elif pris_A_Con == 10 and pris_B_Con == 0:
        result = "Prisoner A will go to jail for 10 years, and prisoner B wil go free"
    elif pris_A_Con == 1 and pris_B_con == 1:
        result = "Both will go to jail for 1 year"
    return(result)

print(result)