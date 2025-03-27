#include "qdp.h"

using namespace QDP;

int main(int argc, char *argv[])
{
  QDP_initialize(&argc, &argv);

  const int L = 8;
  const int latt_size[Nd] = {L, L, L, 2*L};
  
  multi1d<int> nrow(Nd);
  nrow = latt_size;

  Layout::setLattSize( nrow );
  Layout::create();

  LatticeReal a,b,c;
  random(a);
  b = a + a;

  QDPIO::cout << sum(a) << std::endl;

  QDP_finalize();
  return 0;
}
