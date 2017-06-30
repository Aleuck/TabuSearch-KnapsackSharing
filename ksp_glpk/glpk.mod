set O;
/* objetos */

param p{o in O};
/* object's profit */

param w{o in O};
/* object's weight */

param g{o in O};
/* object's group */

param C;
/* knapsack's capacity */

var s{o in O}, binary;
/* solution (object o is in knapsack) */

maximize min_lucro: min{o in O} p[o]*s[o];
s.t. capacidade: sum{o in O} w[o]*s[o] <= C;
