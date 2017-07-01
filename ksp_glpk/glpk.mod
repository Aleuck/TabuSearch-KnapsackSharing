param nOfGroups;
param nOfObjects;

param g{1..nOfGroups, 1..nOfObjects};
/* object is in group */

param p{1..nOfObjects};
/* objects' profit */

param w{1..nOfObjects};
/* objects' weight */

param C;
/* knapsack's capacity */

var s{1..nOfObjects} binary;
/* object is in solution */

var min_group_profit integer, >= 0;

maximize min_profit: min_group_profit;

s.t. capacity: sum{o in 1..nOfObjects} w[o]*s[o] <= C;
s.t. min_group{j in 1..nOfGroups}: min_group_profit <= sum{o in 1..nOfObjects} g[j,o]*p[o]*s[o];
end;
