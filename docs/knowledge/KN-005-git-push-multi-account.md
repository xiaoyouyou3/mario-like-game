# KN-005 `git push` が「Repository not found」になる

| 項目 | 内容 |
|---|---|
| 分類 | Git |
| 確度 | 確認済み |
| 関連 | - |
| 記録日 | 2026-11-13 |

## 症状
`git push` が「Repository not found」になる

## 原因
`gh` に `xiaoyouyou3` と `kobataka-team` の 2 アカウントが登録されていて、git が別アカウントの認証情報を先に使った。`origin` は https で、gh の認証は ssh だった。STATE.md に書いていたリポジトリ URL（kobataka-team）も誤りだった。

## 対処
`git -c credential.helper= -c credential.helper='!gh auth git-credential' push` で通った（既存のヘルパーを空にして、gh の認証だけを使う）。恒久対応は `git config --global --unset-all credential.helper && gh auth setup-git`（`~/.gitconfig` を書き換えるので、ユーザーが実行する）。

## 再発防止
プッシュ前に `gh auth status` でアクティブなアカウントを確認する。STATE.md の URL は `git remote -v` と照合する。

## 根拠
`gh repo view` ではリポジトリが見えるのに、https のプッシュだけ 404 だった。上記のコマンドで `4c75edb..721fbe2` が反映された。
