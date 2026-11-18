#!/usr/bin/env python3
"""Safe read-only (apart from a throwaway write probe) Windows Git diagnosis.
DO NOT run git init, delete lock files, reclone, or modify user projects.
"""
from __future__ import annotations
import sys
from server import ROOT, guard, git, GitFault, failure

def main():
 try:
  sys.stdout.reconfigure(encoding="utf-8",errors="replace")
 except (AttributeError,ValueError):
  pass
 print("="*58)
 print("Trialum 3D Builder — локална GitHub проверка")
 print("="*58)
 print("Builder папка:",ROOT)
 print("Git метаподатоци:",ROOT/".git")
 try:
  gitdir=guard()
  print("Git папка:",gitdir)
  print("Branch:",git("branch","--show-current"))
  print("Origin: Trialum-3D-Builder (проверена точна адреса)")
  dirty=git("status","--short")
  print("Локални измени:", "има" if dirty else "нема")
  if dirty:
   print("Првите изменети ставки:")
   for line in dirty.splitlines()[:20]:
    print(" ",line)
  print("✅ Локалната .git папка и Git CLI моментално се достапни.")
  print("За време на GitHub ↑/↓ не користи истовремено Fetch/Pull/Push во GitHub Desktop.")
  print("Проверка е успешна; не се направени Git commit, pull, push или reset.")
  return 0
 except (GitFault,RuntimeError) as e:
  result=failure(e)
  print("❌ Код:",result["code"])
  print("Проблем:",result["error"])
  print("Насока:",result["hint"])
  print()
  print("ВАЖНО: Не бриши .git или .lock, не прави git init, reset --hard,")
  print("force push или reclone додека имаш незачувани Builder проекти.")
  print("Во GitHub Desktop отвори Repository > Show in Explorer.")
  print("Провери дали тоа е истата папка од која е стартуван Builder.")
  return 2

if __name__=="__main__":
 sys.exit(main())
