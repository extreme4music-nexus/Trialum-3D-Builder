# Trialum Builder — Windows Git lock recovery (18 November 2026)

## User-provided error, not a GitHub authentication problem

Reported in `Problemi.txt`:

```
fatal: Unable to create 'C:/Users/tonic/Documents/Applio-github/Trialum-3D-Builder/.git/index.lock': No such file or directory
fatal: update_ref failed for ref 'ORIG_HEAD': cannot lock ref 'ORIG_HEAD': Unable to create 'C:/Users/tonic/Documents/Applio-github/Trialum-3D-Builder/.git/ORIG_HEAD.lock': No such file or directory
```

This indicates the Git executable was able to start and was trying to modify **local Git metadata**, not remote authentication. The message does NOT prove the entire `.git` folder was deleted: its path may have become inaccessible while Git was running (folder relocated, security/permissions, temporary interruption, another Git process). The previous Builder UI incorrectly appended a generic Git Credential Manager warning to every Git failure; that is fixed.

## Safe Windows checks

1. **Save your editor work** and export an additional JSON backup (do not rely solely on browser localStorage).
2. Close old `START-BUILDER-WINDOWS.bat` terminal and stop any pending GitHub ↑/↓. Let GitHub Desktop finish its current operation.
3. In GitHub Desktop select **Trialum-3D-Builder → Repository → Show in Explorer**. Check that this is exactly the same path printed by the Builder launcher. Do not launch Builder from an old extracted ZIP or a different directory.
4. Confirm the project files `projects/`, `assets/models/`, `index.html` still exist. Enable **View → Show → Hidden items** in Windows Explorer and check whether the `.git` directory exists. **Do not delete, rename or recreate `.git`.**
5. Double-click `CONNECT-GITHUB-WINDOWS.bat` in the cloned Builder root. The new Python doctor checks the expected repo path, `.git` existence, local Git branch/origin, a harmless temporary-file write and concurrent Git locks. It prints a specific diagnostic code and NEVER does `git init`, `reset`, `force push`, `pull`, or `push`.
6. If the diagnosis passes, use either GitHub Desktop Fetch/Pull **or** Builder GitHub ↓, **not both at the same time**. Restart the localhost Python server after Pull so it uses the current code.
7. To push: save the project to the current cloned repo first. Avoid another GitHub Desktop commit/push running simultaneously. Builder GitHub ↑ will refuse unrelated staged source files and will try to publish an existing local commit rather than making a duplicate if a prior Push failed after committing.

## What the diagnostic codes mean

- `GIT_DIRECTORY_MISSING`: the expected `.git` directory no longer exists / is inaccessible in this Builder root. Confirm the local folder in GitHub Desktop; do not run `git init`.
- `GIT_METADATA_DISAPPEARED`: Git reached the local clone but could not create `index.lock` / `ORIG_HEAD.lock` because its parent path disappeared during the operation. Stop overlapping applications; check folder and security access.
- `GIT_METADATA_UNWRITABLE`: Windows rejected temporary writes or Git locks. Check actual folder permissions, antivirus/Controlled Folder Access, or storage restrictions. Do not disable security protections globally.
- `GIT_BUSY`: an existing lock/concurrent Git process may be present. Wait for it to finish; NEVER blindly delete lock files.
- `GIT_WRONG_WORKTREE`, `GIT_WRONG_BRANCH`, `GIT_WRONG_REMOTE`: Builder refuses to write to a different repository, non-main branch or remote.
- `GIT_DIRTY_WORKTREE`: local changes must be safely saved/committed before Pull.
- `GIT_STAGED_CHANGES`: browser Push refuses to accidentally commit files staged elsewhere.
- `GIT_REMOTE_AHEAD`: inspect upstream work in GitHub Desktop first; no force push.

## Last-resort recovery (only after diagnosing actual missing/corrupt metadata)

**Do not overwrite the old folder.** First make a separate backup of `projects/`, any owner-created GLBs and other hand-edited files outside the repository. Once those copies are verified, GitHub Desktop can clone the same repository to a **different, new empty directory**. Compare and transfer only owner-created design files into the new clone, review diffs and commit normally. Do not copy the old `.git` or auto-merge conflicts. If there are existing local commits not pushed, recover them from the old repository before replacing it; ask for assistance if unsure.

## Engineering changes

- `scripts/server.py`: validates local exact Git worktree, remote and branch; reports useful error codes; probes directory writable using a throwaway file; never deletes lock files; refuses unrelated staged changes; handles earlier local commits when Push failed after commit.
- `src/main.js`: displays the real error and diagnostic guidance instead of falsely blaming credentials.
- `scripts/git_doctor.py` + `CONNECT-GITHUB-WINDOWS.bat`: safe local interactive diagnostics.
- `tests/git_sync_safety.test.py`: regression tests for missing `.git`, existing locks, both exact Windows error classes and unrelated staged changes.
- `.github/workflows/bootstrap.yml`: runs these tests before generating 45 original GLB assets.

**Scope:** local Builder GitHub integration only. No change to Trialum Classic, LW-D gameplay, Android signing, Play Store or production servers.
