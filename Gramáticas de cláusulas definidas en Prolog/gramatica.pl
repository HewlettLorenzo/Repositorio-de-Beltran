% Acá definimos léxico, le adjudicamos género y número.
det(el,   masc, sing).
det(la,   fem,  sing).
det(los,  masc, pl).
det(las,  fem,  pl).
det(un,   masc, sing).
det(una,  fem,  sing).

noun(empleado,   masc, sing).
noun(empleada,   fem,  sing).
noun(empleados,  masc, pl).
noun(empleadas,  fem,  pl).
noun(sueldo,     masc, sing).
noun(sueldos,    masc, pl).

iv(trabaja,  sing).
iv(trabajan, pl).

tv(cobra,   sing).
tv(cobran,  pl).

% DCG de árbol: Se construye el término A
o_tree(o(SN,SV)) -->
    sn(_Gen,_Num,SN),
    sv(_Num,SV).

% Acá son las entradas de las oraciones.
o --> o_tree(_).      % phrase(o, ...) → true/false
o(A) --> o_tree(A).  % phrase(o(A), ...) → A = árbol

% Sintagma nominal //3
% sn(Gen,Num,ÁrbolSN)

sn(Gen,Num, sn(det(Det), n(Noun))) -->
    det(Det,Gen,Num),
    noun(Noun,Gen,Num).

% Sintagma verbal //2
% sv(Num,ÁrbolSV)
%   intransitivo y transitivo

sv(Num, sv(vt(V))) -->
    iv(V,Num).

sv(Num, sv(vt(V), OBJ)) -->
    tv(V,Num),
    sn(_G2,_N2, OBJ).

% Acá se implementan reglas auxiliares.
det(W,Gen,Num)   --> [W], { det(W,Gen,Num) }.
noun(W,Gen,Num)  --> [W], { noun(W,Gen,Num) }.
iv(W,Num)        --> [W], { iv(W,Num) }.
tv(W,Num)        --> [W], { tv(W,Num) }.