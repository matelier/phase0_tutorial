# PHASE/0チュートリアル（ドキュメント）

講習会などで用いる例題とその説明です。講習会ではWSL利用を想定しますが、一般的なLinuxやmacOSでも実行できます。
HTML版ドキュメントは[こちら](https://phase0-tutorial-wsl.readthedocs.io/ja/latest/) を参照してください。

# Sphinx設定

説明文の整形にSphinxを用います。

Read the Docsが提供しているテーマと併せてインストールします。

```sh
pip install sphinx
pip install sphinx_rtd_theme
```

`uv`仮想環境向け

```sh
uv init --python 3.13
uv venv
source .venv/bin/activate
uv add sphinx
uv add sphinx_rtd_theme
```

例題PHASE/0入力ファイルは`main`ブランチに分離しました。
