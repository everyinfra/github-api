#!/usr/bin/env bash
# GitHub API 的 curl 示例：所有能力都发到同一个地址，只换 action 和 params。
# curl examples for the GitHub API: every capability uses the same URL; only action and params change.
#
#   export EVERYINFRA_API_KEY=<your API key>
#   bash examples/curl.sh repository https://github.com/facebook/react        # 仓库链接或 owner/repo / a repo link or owner/repo
#   bash examples/curl.sh repository_issues https://github.com/facebook/react
#   bash examples/curl.sh contributors https://github.com/facebook/react
#   bash examples/curl.sh user <username>                                     # contributors 结果里的 username / the username from a contributors result
#   bash examples/curl.sh user_repositories <username>
set -euo pipefail
: "${EVERYINFRA_API_KEY:?Set EVERYINFRA_API_KEY first: https://everyinfra.com/docs#quickstart}"
action=${1:?"usage: bash examples/curl.sh <repository|repository_issues|contributors|user|user_repositories> <value>"}
value=${2:?"value: a repository url or a username"}

case "$action" in
  repository | repository_issues | contributors) params="{\"url\":\"$value\"}" ;;
  user | user_repositories)                      params="{\"username\":\"$value\"}" ;;
  *) echo "unknown action: $action (use repository, repository_issues, contributors, user or user_repositories)" >&2; exit 2 ;;
esac

curl -sS -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"platform\":\"github\",\"action\":\"$action\",\"params\":$params}"
echo
