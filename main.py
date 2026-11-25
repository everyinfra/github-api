"""GitHub API 示例（GitHub API in Python）。

  python main.py repo "https://github.com/facebook/react"                                # 仓库详情 / repository detail
  python main.py issues "https://github.com/facebook/react" --out issues.csv             # Issue 与 PR / issues and PRs
  python main.py contributors "https://github.com/facebook/react" --out contributors.csv # 仓库贡献者 / contributors
  python main.py user <用户名>                                                           # 用户资料 / user profile
  python main.py repos <用户名> --out user_repos.csv                                     # 用户的仓库 / a user's repositories
"""
import argparse

from everyinfra import fetch, report

STATES = ["all", "closed", "open"]
SORTS = ["comments", "created", "updated"]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("repo", help="仓库详情 / one repository")
    r.add_argument("url")
    i = sub.add_parser("issues", help="仓库的 Issue 与 PR / issues and PRs of a repository")
    i.add_argument("url")
    i.add_argument("--state", choices=STATES, help="open / closed / all")
    i.add_argument("--sort", choices=SORTS, help="created / updated / comments")
    c = sub.add_parser("contributors", help="仓库贡献者 / contributors of a repository")
    c.add_argument("url")
    u = sub.add_parser("user", help="用户资料 / user profile")
    u.add_argument("username")
    re = sub.add_parser("repos", help="用户的仓库 / a user's repositories")
    re.add_argument("username")
    re.add_argument("--sort", choices=SORTS, help="created / updated / pushed / full_name")
    for x in (r, i, c, u, re):
        x.add_argument("--out", help="存成 .csv 或 .json / write .csv or .json")
    a = p.parse_args()

    if a.cmd == "repo":
        rows, charged = fetch("repository", {"url": a.url})
    elif a.cmd == "issues":
        params = {"url": a.url, **({"state": a.state} if a.state else {}), **({"sort": a.sort} if a.sort else {})}
        rows, charged = fetch("repository_issues", params)
    elif a.cmd == "contributors":
        rows, charged = fetch("contributors", {"url": a.url})
    elif a.cmd == "user":
        rows, charged = fetch("user", {"username": a.username})
    else:
        params = {"username": a.username, **({"sort": a.sort} if a.sort else {})}
        rows, charged = fetch("user_repositories", params)
    report(rows, charged, a.out)


if __name__ == "__main__":
    main()
