# PHASE/0チュートリアル（ドキュメント）

講習会などで用いている例題とその説明です。WSLで実行することを想定していますが、一般的なLinuxやmacOSにおいても問題なく実行できます。
[こちらから](https://phase0-tutorial-wsl.readthedocs.io/ja/latest/) HTML版のドキュメントをみることができます

# Sphinx設定

説明文の整形にSphinxを用います。

Read the Docsが提供しているテーマと併せてインストールします。

```sh
pip install sphinx
pip install sphinx_rtd_theme
```

例題のPHASE/0入力ファイルは`main`ブランチに分離しました。
