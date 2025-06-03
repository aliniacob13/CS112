FPATH = __file__.rsplit("/", maxsplit=1)[0] + "/"
def save_matrix(n):
    matrice=[[int(x) for x in input().split()] for _ in range(n)] #citesc din input matricea
    return matrice #o returnez
def load_matrix(fisier, matrice):
    with open(FPATH+fisier, "w") as g: #citesc din matrice
        nr_coloane=len(matrice[0])
        for line in matrice:
            if len(line)!=nr_coloane:
                g.write("NU E MATRICE\n")
                return
        for line in matrice: #parcurg linie cu linie 
            formatted_line = " ".join(map(str, line)) #le fac din integer in str
            g.write(formatted_line + "\n") #pun in fisier
    
    g.close() #inchid fisierul

def load_automata(fisier):
    rules=[]
    states=[]
    symbols=[]
    with open(FPATH+fisier,"r+") as f:
         lines=f.read().strip()
    sections=lines.split("#")
    for section in sections:
        paragraph=section.strip().split("\n")
        """
        try:
            l=[]
            dict=[]
            print(paragraph[1])
            if paragraph[1]=="[States]":
                for i in range(2,len(paragraph)):
                    l.append(i)
                states=" ".join(l)
            elif paragraph[1]=="[Symbols]":
                for i in range(2,len(paragraph)):
                    l.append(i)
                symbols=" ".join(l)
            elif paragraph[1]=="Rules":
                l1=[]
                for i in range(2,len(paragraph)):   
                    l1.append(i)
                rules="".join(l1)
        except:
            continue
        """
        if len(paragraph) < 2:
            continue  #evitam sectiuni goale

        header = paragraph[0].strip()  #Prima linie a sectiunii

        if header == "[States]":
            states = [line.strip() for line in paragraph[1:] if line.strip()]
        elif header == "[Symbols]":
            symbols = [line.strip() for line in paragraph[1:] if line.strip()]
        elif header == "[Rules]":
            rules = [[int(num) for num in line.split()] for line in paragraph[1:] if line.strip()]
    
    print("States:", states)
    print("Symbols:", symbols)
    print("Rules:", rules)
load_automata("text.txt")

"""
n=int(input())
m=save_matrix(n) #apelez functia de save
print(m) #afisez matricea
load_matrix("date.in",m) #pun matricea in fisierul respectiv
"""
"""
->state
[
initial state
final state
]
->Symbols 
->Rules

[States]
starile:
q0 #comentarii
q1
End
[Symbols]
0
1
End
[Rules]
q0, simbolul, q1
q0, 1, q1
q1, 0, q0
q1, 1, q0
"""
