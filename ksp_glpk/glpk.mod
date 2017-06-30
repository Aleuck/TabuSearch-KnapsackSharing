param nOfGroups;
param nOfObjects;

param g{1..nOfGroups, 1..noOfObjects} binary;
/* object is in group */

param p{1..nOfObjects};
/* objects' profit */

param w{1..nOfObjects};
/* objects' weight */

param C;
/* knapsack's capacity */

var sol{1..nOfObjects} binary;
/* object is in solution */

maximize min_lucro: min{g in 1..numOfGroups} sum{o in 1..numOfObjects} sol[o]*p[o]*g[g][o];
s.t. capacidade: sum{o in O} w[o]*s[o] <= C;
