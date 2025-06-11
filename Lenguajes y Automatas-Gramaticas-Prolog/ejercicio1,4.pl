#1. Acá declaramos que butch es un asesino.
asesino(butch).

#2. Declaramos que Mia y Marsellus están casados.
    #Guardamos la pareja en un solo sentido.          
pareja(mia, marsellus).
    #Y declaramos casados/2 simétrico.
casados(X,Y) :- pareja(X,Y).
casados(X,Y) :- pareja(Y,X).

#3. Decimos que Zed se murió.
muerto(zed).

#4. Declaramos que Marsellus mata a todos los que le dan a Mia un masaje en los pies. 
mata(marsellus, Persona) :-
    masaje_pies(Persona, mia).

#5. Decimos que Mia ama a todos los que son buenos bailarines.
ama(mia, Persona) :-
    buen_bailarin(Persona).

#6. Acá decimos que Jules come cualquier cosa que sea nutritiva o sabrosa.
come(jules, Cosa) :-
    nutritiva(Cosa) ;
    sabrosa(Cosa).