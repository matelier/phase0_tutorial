#!/usr/bin/env python3
"""nfinput.data のテンプレート中の $1 を走査値で置換しながら PHASE を繰り返し実行する。

元の scan.sh の Python 版。環境変数 PHASE0 に phase 実行形式ファイルを指定して実行する。

    PHASE0=/path/to/phase python3 scan.py
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

# エネルギー換算に使う定数（元スクリプトの値）
HARTREE_TO_EV = 27.211386245981  # 単位変換

# output000 の TH 行からエネルギーを切り出す桁位置（1-origin の 35-54 に対応）
TH_COL_SLICE = slice(34, 54)

TEMPLATE = Path("nfinput.data")
INPUT = Path("nfinp.data")
OUTPUT = Path("data.txt")
MPIEXEC = "mpiexec"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument(
        "--e-offset",
        dest="e_offset",
        type=float,
        default=7.87,
        help="エネルギーオフセット（既定: 7.87）",
    )
    p.add_argument(
        "--n-unit",
        dest="n_unit",
        type=float,
        default=4.0,
        help="単位変換倍率（既定: 4、FCCのBravais格子は基本格子の4倍）",
    )
    p.add_argument(
        "--start", type=int, default=495, help="走査開始値（1/100 単位、既定: 495）"
    )
    p.add_argument(
        "--stop", type=int, default=621, help="走査終了値（含む、既定: 621）"
    )
    p.add_argument("--step", type=int, default=5, help="刻み幅（既定: 5）")
    p.add_argument(
        "--ne", type=int, default=1, help="PHASE/0 のバンド並列数 ne（既定: 1）"
    )
    p.add_argument(
        "--nk", type=int, default=4, help="PHASE/0 の k 点並列数 nk（既定: 4）"
    )
    return p.parse_args(argv)


def resolve_phase0() -> Path:
    """環境変数 PHASE0 を検証して返す。"""
    raw = os.environ.get("PHASE0")
    if not raw:
        sys.exit("エラー: 環境変数 PHASE0 が設定されていません")

    phase0 = Path(raw).expanduser()
    if not (phase0.is_file() and os.access(phase0, os.X_OK)):
        sys.exit(f"エラー: PHASE0='{raw}' は実行可能なファイルではありません")
    return phase0.resolve()


def extract_energy(output: Path) -> float:
    """output000 の最後の TH 行からエネルギーを取り出す。"""
    th_lines = [ln for ln in output.read_text().splitlines() if "TH" in ln]
    if not th_lines:
        raise RuntimeError(f"{output} に TH を含む行がありません")

    field = th_lines[-1][TH_COL_SLICE].strip()
    try:
        return float(field)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"{output} の TH 行から数値を読めません: {field!r}") from exc


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    phase0 = resolve_phase0()
    print(f"PHASE0: {phase0}")

    if not TEMPLATE.is_file():
        sys.exit(f"エラー: テンプレート '{TEMPLATE}' が見つかりません")

    template = TEMPLATE.read_text()

    for i in range(args.start, args.stop + 1, args.step):
        print(i, flush=True)

        # 整数のループ変数をオングストローム単位に変換（例: 495 -> 4.95）
        a = i / 100

        # テンプレート中のプレースホルダ $1 を置換
        INPUT.write_text(template.replace("$1", str(a)))

        subprocess.run(
            [
                MPIEXEC,
                "-n",
                str(args.ne * args.nk),
                str(phase0),
                f"ne={args.ne}",
                f"nk={args.nk}",
            ],
            check=True,
        )

        out = Path("output000")
        if not out.is_file():
            sys.exit("エラー: output000 が生成されていません")

        e = extract_energy(out)
        y = (e + args.e_offset) * args.n_unit * HARTREE_TO_EV

        with OUTPUT.open("a") as fh:
            fh.write(f"{a} {y:.10f}\n")

        shutil.move(str(out), f"output{i}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
