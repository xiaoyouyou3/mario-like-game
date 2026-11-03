"""要件(REQ) → テストケース(TC) → テストコードのトレーサビリティを機械検査する。

Usage: python scripts/trace_check.py --stage spec|tests|all
  spec : 全 REQ が少なくとも1つの TC（または手動確認 MC）から参照されているか
  tests: 全 TC に対応するテストコード(# TC-NNN)があるか、仕様にない TC をテストが参照していないか
終了コード: 0=問題なし / 1=ギャップあり / 2=入力ファイルなし
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQ_FILE = ROOT / "docs/requirements/requirements.md"
SPEC_FILE = ROOT / "docs/test-specs/test-spec.md"
TESTS_DIR = ROOT / "tests"

REQ_ROW = re.compile(r"^\|\s*(REQ-\d+)\s*\|", re.MULTILINE)
TC_ROW = re.compile(r"^\|\s*(TC-\d+)\s*\|(.*)$", re.MULTILINE)
MC_ROW = re.compile(r"^\|\s*(MC-\d+)\s*\|(.*)$", re.MULTILINE)
REQ_REF = re.compile(r"REQ-\d+")
TC_MARK = re.compile(r"#\s*(TC-\d+(?:\s*,\s*TC-\d+)*)")


def read(path: Path) -> str:
    if not path.exists():
        print(f"入力ファイルがありません: {path.relative_to(ROOT)}")
        sys.exit(2)
    return path.read_text(encoding="utf-8")


def spec_gaps() -> tuple[set[str], dict[str, set[str]], list[str]]:
    reqs = set(REQ_ROW.findall(read(REQ_FILE)))
    spec_text = read(SPEC_FILE)
    tc_to_reqs = {
        tc: set(REQ_REF.findall(rest)) for tc, rest in TC_ROW.findall(spec_text)
    }
    mc_to_reqs = {
        mc: set(REQ_REF.findall(rest)) for mc, rest in MC_ROW.findall(spec_text)
    }
    covered = set().union(*tc_to_reqs.values(), *mc_to_reqs.values())
    problems = [f"REQ に対応する TC / MC がない: {r}" for r in sorted(reqs - covered)]
    refs = {**tc_to_reqs, **mc_to_reqs}
    problems += [
        f"存在しない REQ を参照: {k} -> {r}"
        for k, rs in sorted(refs.items())
        for r in sorted(rs - reqs)
    ]
    return reqs, tc_to_reqs, problems


def test_gaps(tc_ids: set[str]) -> list[str]:
    marked: set[str] = set()
    for f in TESTS_DIR.rglob("test_*.py"):
        for group in TC_MARK.findall(f.read_text(encoding="utf-8")):
            marked.update(re.findall(r"TC-\d+", group))
    problems = [
        f"TC に対応するテストコードがない: {t}" for t in sorted(tc_ids - marked)
    ]
    problems += [
        f"仕様書にない TC をテストが参照: {t}" for t in sorted(marked - tc_ids)
    ]
    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["spec", "tests", "all"], default="all")
    stage = parser.parse_args().stage
    _, tc_to_reqs, problems = spec_gaps()
    if stage in ("tests", "all"):
        problems += test_gaps(set(tc_to_reqs))
    for p in problems:
        print(f"NG  {p}")
    print(
        f"{'OK' if not problems else 'FAIL'}: stage={stage} REQ->TC->test ギャップ {len(problems)} 件"
    )
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
