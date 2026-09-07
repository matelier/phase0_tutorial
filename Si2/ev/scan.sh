#!/usr/bin/env bash
set -euo pipefail

# 環境変数PHASE0に、phase実行形式ファイルを指定してから実行してください。
: "${PHASE0:?エラー: 環境変数 PHASE0 が設定されていません}"

if [[ ! -x "$PHASE0" ]]; then
    echo "エラー: PHASE0='$PHASE0' は実行可能なファイルではありません" >&2
    exit 1
fi

echo "PHASE0: $PHASE0"


file=data.txt

for i in `seq 495 5 621`
do
    echo $i
    a=`echo "scale=2; $i / 100.0" | bc`
    sed 's/$1/'$a'/g' nfinput.data > nfinp.data

    mpiexec -n 4 $PHASE0 ne=1 nk=4

    e=`grep TH output000 | tail -n 1 | cut -c 35-54`
    y=`echo "scale=10; (($e + 7.87) * 4) * 27.211386245981" | bc`  #

    echo $a $y >> $file
    mv output000 output$i
done
