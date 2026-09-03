#!/bin/sh

inivol=1000
n=21
dv=10
np=2
nk=2
ne=1
PHASE0="mpiexec -n ${np} $HOME/phase0_2024.01/bin/phase ne=${ne} nk=${nk}"
rm -f nfefn.data
echo ${PHASE0}
for v in `seq 1 $n`;do
  vol=$( echo "($v-1)*$dv + $inivol" | bc -l )
  a=$( echo "e(l($vol)/3)" | bc -l )
  echo "volume : $vol"
  mkdir -p vol$vol
  cp file_names.data vol$vol
  sed "s/__A__/$a/g" nfinp.data > vol$vol/nfinp.data
  cd vol$vol
  ${PHASE0}
  cd ..
  echo -n $vol>> nfefn.data ; tail -1 vol$vol/nfefn.data >>nfefn.data
done
