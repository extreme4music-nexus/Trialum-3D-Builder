#!/usr/bin/env python3
"""Regression checks for Windows index.lock / ORIG_HEAD.lock recovery."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
import server as srv

class GitSyncSafety(unittest.TestCase):
 def test_missing_git_metadata_is_reported_without_reinitializing_or_deleting(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)
   (root/"projects").mkdir()
   (root/"projects"/"owner-design.json").write_text('{"keep":true}')
   with patch.object(srv,"ROOT",root):
    with self.assertRaises(srv.GitFault) as error:
     srv.guard()
    self.assertEqual(error.exception.code,"GIT_DIRECTORY_MISSING")
    self.assertFalse((root/".git").exists())
    self.assertEqual((root/"projects"/"owner-design.json").read_text(),'{"keep":true}')

 def test_git_lock_present_blocks_operations_and_does_not_delete_lock(self):
  with tempfile.TemporaryDirectory() as d:
   gitdir=Path(d)/".git"
   gitdir.mkdir()
   lock=gitdir/"index.lock"
   lock.write_text("external Git operation")
   with self.assertRaises(srv.GitFault) as caught:
    srv.ensure_writable_gitdir(gitdir)
   self.assertEqual(caught.exception.code,"GIT_BUSY")
   self.assertEqual(lock.read_text(),"external Git operation")

 def test_missing_windows_git_lock_parent_gets_correct_error_code(self):
  for lock in ("index.lock","ORIG_HEAD.lock"):
   msg=("fatal: Unable to create 'C:/Users/example/Documents/Trialum-3D-Builder/.git/"
        +lock+"': No such file or directory")
   fake=subprocess.CompletedProcess(args=["git","add"],returncode=128,stdout="",stderr=msg)
   with patch.object(srv.subprocess,"run",return_value=fake):
    with self.assertRaises(srv.GitFault) as e:
     srv.git("add","--","projects")
    self.assertEqual(e.exception.code,"GIT_METADATA_DISAPPEARED")
    self.assertNotIn("credentials",e.exception.hint.lower())

 def test_different_worktree_refuses_push(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); (root/".git").mkdir()
   def stub(*args,**kwargs):
    if args==("rev-parse","--show-toplevel"):return str(root.parent)
    return "main"
   with patch.object(srv,"ROOT",root), patch.object(srv,"git",side_effect=stub):
    with self.assertRaises(srv.GitFault) as err:
     srv.guard()
    self.assertEqual(err.exception.code,"GIT_WRONG_WORKTREE")

 def test_staged_unrelated_source_is_not_committed(self):
  with patch.object(srv,"guard"),patch.object(srv,"staged_paths",return_value=["scripts/server.py"]),patch.object(srv,"git") as mock:
   with self.assertRaises(srv.GitFault) as err:
    srv.publish_designs()
   self.assertEqual(err.exception.code,"GIT_STAGED_CHANGES")
   mock.assert_not_called()

 def test_gitdir_write_probe_only_uses_temporary_file(self):
  with tempfile.TemporaryDirectory() as d:
   dot=Path(d)/".git";dot.mkdir()
   srv.ensure_writable_gitdir(dot)
   self.assertEqual(list(dot.iterdir()),[])

if __name__=="__main__":
 unittest.main(verbosity=2)
