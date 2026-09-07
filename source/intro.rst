はじめに
================================

概要
------------------

本稿は第一原理バンド計算ソフトウェアPHASE/0のチュートリアルです。
第一原理バンド計算は多大な計算リソースが必要な場合が多いですが、本チュートリアルは一般的なパソコンでも実行できるような規模の問題のみを扱い、その実行方法や結果の見方について解説します。
環境としては、\ `Windows上で構築したWSL環境 <https://learn.microsoft.com/ja-jp/windows/wsl/install>`_ を想定していますが、一般的なGNU/LinuxやmacOSでも実行できるはずです。
お手元のパソコンにおいて実際に例題を実行することを通じて、初学者がPHASE/0の基本的な使い方を自習することができることを目的としています。
紹介されている例題の入力ファイルは `GitHubで公開されているため <https://github.com/Materials-Science-Software-Consortium/phase0_tutorial_wsl/tree/main/wsl>`_ 自由にダウンロードすることができるようになっています。

本チュートリアルの構成
-----------------------

\ :ref:`si2_chapter` では簡単に計算できる例として2原子からなるシリコン結晶の例を扱います。
基本となるself-consistent field (SCF) 計算を実行し、それをもとに電子状態密度やバンド構造、誘電関数の計算などを実行します。
また、振動解析や :math:`EV` 曲線の計算を行う方法も紹介します。
\ :ref:`mag_chapter` では磁性の扱い方を紹介します。
磁性を有効にする方法や磁性を考慮している場合の結果の解析方法などを説明します。
\ :ref:`surf_chapter` では表面の計算の方法を紹介します。
PHASE/0は平面波基底に基づいて計算を行うため、扱えるのは厳密にいうと周期系のみです。
しかし表面に垂直な方向に十分な厚さの"真空層"を設けることによって事実上表面と変わらない系を扱うことはできます。
ここではその方法について説明します。
また、単純な結晶では必要ない「構造最適化」の方法を説明し、さらに原子ごとの電子状態を解析する方法についても説明します。
\ :ref:`defect_chapter` では点欠陥のエネルギー計算を扱います。
ここでは、第一原理計算において「生成エネルギー」はどのように計算するかを説明します。
最後に、\ :ref:`sup_chapter` においてはPHASE/0を活用するためのちょっとしたコツなどを紹介していきます。


環境設定など
----------------------

本チュートリアルを実行するにはPHASE/0と可視化用のソフトウェアがお使いのパソコンにインストールされている必要があります。
もしインストールされていないのであれば、\ `このサイトの情報 <https://github.com/Materials-Science-Software-Consortium/phase0_install/tree/main/WSL>`_ などを参考にインストールします。
WSL環境を用意し、UbuntuなどのLinuxディストリビューションをインストールすることができたらPHASE/0のインストールと可視化用ソフトウェアのgnuplot, evinceのインストールを行ってください。
本稿では以降ホームディレクトリーに |PHASE020XX.YY| がインストールされていることを仮定して説明を進めます。
また、原子配置の可視化に `VESTA <https://jp-minerals.org/vesta/jp/>`_ を用いるので、こちらもインストールしておくことが推奨されます。

PHASE/0の引用情報など
-----------------------

- ホームページ
  https://azuma.nims.go.jp/

- GitHub
  https://github.com/Materials-Science-Software-Consortium

- 論文
  Takahiro Yamasaki, Akiyoshi Kuroda, Toshihiro Kato, Jun Nara, Junichiro Koga, Tsuyoshi Uda, Kazuo Minami, and Takahisa Ohno,
  "Multi-axis Decomposition of Density Functional Program for Strong Scaling up to 82,944 Nodes on the K Computer: Compactly Folded 3D-FFT Communicators in the 6D Torus Network"
  Computer Physics Communications 244, 264-276 (2019).
  https://doi.org/10.1016/j.cpc.2019.04.008

