# GitHub API

[English](#english) · [中文](#中文)

## English

This repo reads public GitHub data with Python or curl. You can read a repository's details, its issues and pull requests and its contributors, and look up a user's profile and repositories. You need one EveryInfra API key. You do not need a GitHub account or cookie. The same API also works as an MCP tool in Claude and Cursor. Billing is per call: these 5 capabilities cost $0.96 per 1,000 calls (about $0.00096 per call). Failed calls and empty results are not charged. The EveryInfra GitHub API has 9 capabilities, all listed on the platform page: <https://everyinfra.com/en/github-api?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>

### Quick start

```bash
git clone https://github.com/everyinfra/github-api.git
cd github-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<your API key>
python main.py repo "https://github.com/facebook/react"
python main.py issues "https://github.com/facebook/react" --out issues.csv
python main.py contributors "https://github.com/facebook/react" --out contributors.csv
python main.py user <username>
python main.py repos <username> --out user_repos.csv
```

- For `repo`, `issues` and `contributors`, pass a repository link or owner/repo, for example facebook/react.
- `issues` returns both issues and pull requests; `is_pull_request` tells them apart. By default only open ones are listed.
- For `user` and `repos`, pass a username, for example the `username` from a `contributors` result. Organization accounts work too.
- Without `--out`, the command prints the first 3 rows as JSON. With `--out`, it saves a .csv or .json file. The CSV has a BOM, so Excel opens it without garbled text.
- Register at everyinfra.com, then create the API key in the console. Steps: <https://everyinfra.com/en/docs?utm_source=github&utm_medium=example_repo&utm_campaign=github-api#quickstart>

### curl

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"github","action":"repository","params":{"url":"https://github.com/facebook/react"}}'
```

All capabilities use the same URL. Change `action` and `params` to call another one. Examples for `repository_issues`, `contributors`, `user`, and `user_repositories` are in [examples/curl.sh](examples/curl.sh).

### Claude and Cursor (MCP)

The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. EveryInfra runs the server, so you install no local program.

Claude Code:

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor and other clients that read `mcp.json` ([examples/mcp.json](examples/mcp.json)):

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Custom connectors in Claude on the web and desktop, and ChatGPT, accept only a URL. Enter <https://api.everyinfra.com/mcp/all>, sign in to EveryInfra when asked, and allow access. You do not need to enter a key. Full steps: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>

### Price

| `action` | Per 1,000 calls |
|---|---|
| `repository` | $0.96 |
| `repository_issues` | $0.96 |
| `contributors` | $0.96 |
| `user` | $0.96 |
| `user_repositories` | $0.96 |

- Billing is per call, about $0.00096 each. Failed calls, empty results, parameter errors, and authentication failures are not charged.
- A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>
- Prices for the other 4 GitHub capabilities are on the platform page: <https://everyinfra.com/en/github-api?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>

### Fields

These are the fields that the 5 capabilities returned in our test. Each meaning is the first sentence of the field's entry in the API documentation. The link under each table has the full text.

#### `repository` (repository details)

| Field | Meaning |
|---|---|
| `id` | GitHub's numeric ID, as a string. |
| `full_name` | Repository name as owner/repo; a renamed or transferred repository shows its new name. |
| `name` | Name of the object itself, for account, product and business capabilities. |
| `owner_username` | Username of the repository owner (user or organization). |
| `owner_url` | Profile link of the repository owner. |
| `owner_avatar_url` | Avatar image of the repository owner. |
| `url` | Link to the record on the platform. |
| `description` | Summary or description, usually shorter than text. |
| `homepage` | Project homepage set on the repository; absent when none is set. |
| `language` | Main programming language, such as Python; absent when GitHub does not detect a language. |
| `license` | License name, such as MIT License; absent when none is declared. |
| `topics` | Repository topic tags; absent when there are none. |
| `star_count` | Stars. |
| `fork_count` | Forks. |
| `open_issue_count` | Open issues plus open pull requests, as GitHub counts them. |
| `default_branch` | Default branch name. |
| `is_fork` | Whether the repository itself is a fork (repository / user_repositories). |
| `is_archived` | Whether the repository is archived (read-only). |
| `size_kb` | Repository size in KB, as GitHub reports it. |
| `created_at` | Creation time, same format as posted_at. |
| `updated_at` | Last update time, ISO 8601 UTC. |
| `pushed_at` | Time of the last code push, ISO 8601 UTC. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/github-api/repository?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>

#### `repository_issues` (Repository issues and PRs)

| Field | Meaning |
|---|---|
| `id` | GitHub's numeric ID, as a string. |
| `number` | Issue or pull request number within the repository. |
| `url` | Link to the record on the platform. |
| `title` | Title. null when the platform has no titles (for example text-only posts). |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `state` | open or closed. |
| `is_pull_request` | true for a pull request, false for an issue. |
| `is_draft` | Whether a pull request is a draft; false for issues. |
| `labels` | Label names; absent when there are none. |
| `comment_count` | Comments. null means not disclosed, not 0. |
| `reaction_count` | Total emoji reactions. |
| `repository` | Repository the row belongs to, as owner/repo. |
| `author_username` | Author's username (@handle), usually usable in URLs. |
| `author_id` | Author's unique ID on the platform. |
| `author_avatar_url` | Link to the author's avatar image (signed and expiring on most platforms). |
| `author_type` | Author account type: User, Bot or Organization. |
| `author_association` | The author's relation to the repository, as GitHub reports it: OWNER, MEMBER, COLLABORATOR, CONTRIBUTOR, FIRST_TIME_CONTRIBUTOR, NONE and so on. |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `updated_at` | Last update time, ISO 8601 UTC. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/github-api/repository_issues?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>

#### `contributors` (repository contributors)

| Field | Meaning |
|---|---|
| `rank` | Position in this response from 1: by commit count for contributors, in Trending order for trending. |
| `username` | Username (@handle). |
| `id` | GitHub's numeric ID, as a string. |
| `url` | Link to the record on the platform. |
| `avatar_url` | Avatar image link. |
| `contribution_count` | Commits to this repository (contributors). |
| `account_type` | Account type: User, Bot or Organization. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/github-api/contributors?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>

#### `user` (user profile)

| Field | Meaning |
|---|---|
| `username` | Username (@handle). |
| `id` | GitHub's numeric ID, as a string. |
| `display_name` | Display name; can differ from username. |
| `company` | Company written on the profile; absent when empty. |
| `location` | Location description passed through as is; the format varies by platform. |
| `follower_count` | Followers. null means not disclosed, not 0. |
| `following_count` | Accounts followed. null means not disclosed, not 0. |
| `public_repo_count` | Public repositories. |
| `public_gist_count` | Public gists. |
| `avatar_url` | Avatar image link. |
| `url` | Link to the record on the platform. |
| `account_type` | Account type: User, Bot or Organization. |
| `created_at` | Creation time, same format as posted_at. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/github-api/user?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>

#### `user_repositories` (user repositories)

| Field | Meaning |
|---|---|
| `id` | GitHub's numeric ID, as a string. |
| `full_name` | Repository name as owner/repo; a renamed or transferred repository shows its new name. |
| `name` | Name of the object itself, for account, product and business capabilities. |
| `owner_username` | Username of the repository owner (user or organization). |
| `owner_url` | Profile link of the repository owner. |
| `owner_avatar_url` | Avatar image of the repository owner. |
| `url` | Link to the record on the platform. |
| `description` | Summary or description, usually shorter than text. |
| `star_count` | Stars. |
| `fork_count` | Forks. |
| `open_issue_count` | Open issues plus open pull requests, as GitHub counts them. |
| `default_branch` | Default branch name. |
| `is_fork` | Whether the repository itself is a fork (repository / user_repositories). |
| `is_archived` | Whether the repository is archived (read-only). |
| `size_kb` | Repository size in KB, as GitHub reports it. |
| `created_at` | Creation time, same format as posted_at. |
| `updated_at` | Last update time, ISO 8601 UTC. |
| `pushed_at` | Time of the last code push, ISO 8601 UTC. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `homepage` | Project homepage set on the repository; absent when none is set. |
| `language` | Main programming language, such as Python; absent when GitHub does not detect a language. |
| `license` | License name, such as MIT License; absent when none is declared. |

All parameters and fields: <https://everyinfra.com/en/github-api/user_repositories?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>

### FAQ

**Do I need a GitHub account or cookie to call the API?**

No. Send the `Authorization: Bearer` header with your API key. The request body holds `platform`, `action`, and the capability parameters. You do not scan a QR code, keep a login session, or open a browser.

**How much does it cost? Are failed calls charged? Is there a free allowance?**

Billing is per call, from $0.81 per 1,000 calls. Failed calls, empty results, parameter errors, and authentication failures are not charged. A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>

**Can I connect the GitHub API to Claude or Cursor?**

Yes. The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. You install no local program. Setup for Claude, Cursor, ChatGPT, and Claude Code: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>.

**What legal points apply when I use GitHub data?**

The EveryInfra Terms of Service require you to make sure your use of the data follows applicable law and the terms of the relevant platform. Do not use the data for anything illegal or anything that violates privacy or intellectual property rights. Do not use bulk scraping for harassment, fraud, or other abuse. When you use personal information such as nicknames and avatars, keep only the fields your business needs.

**Which GitHub data can I get?**

The EveryInfra GitHub API has 9 capabilities:

- repository details
- user profile
- user repositories
- Repository issues and PRs
- issue search
- issue comments
- repository contributors
- repository forks
- trending list

Parameters and return fields for each capability are on the platform page: <https://everyinfra.com/en/github-api?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>

### Tested

Before release, we ran the 5 commands in Quick start against the live API with this repo's code.

| Command | Time (Singapore, UTC+8) | Rows | Charged |
|---|---|---|---|
| `python main.py repo "https://github.com/facebook/react"` | 2026-11-25 13:17 | 1 | $0.000958 |
| `python main.py issues "https://github.com/facebook/react" --out issues.csv` | 2026-11-25 13:17 | 30 | $0.000958 |
| `python main.py contributors "https://github.com/facebook/react" --out contributors.csv` | 2026-11-25 13:18 | 30 | $0.000958 |
| `python main.py user <username>` | 2026-11-25 13:18 | 1 | $0.000958 |
| `python main.py repos <username> --out user_repos.csv` | 2026-11-25 13:18 | 30 | $0.000958 |

## 中文

本仓库用 Python 或 curl 读 GitHub 公开数据：读仓库详情、Issue 与 PR 列表和贡献者，查用户资料和用户名下的仓库。只需一把 EveryInfra API Key，不用 GitHub 账号和 Cookie，也能作为 MCP 工具接进 Claude、Cursor。按调用次数计费，这 5 个能力每千次 $0.96（每次约 $0.00096），失败和空结果不收费。GitHub 共 9 个能力：<https://everyinfra.com/github-api?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>

### 快速开始

```bash
git clone https://github.com/everyinfra/github-api.git
cd github-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<你的 API Key>
python main.py repo "https://github.com/facebook/react"
python main.py issues "https://github.com/facebook/react" --out issues.csv
python main.py contributors "https://github.com/facebook/react" --out contributors.csv
python main.py user <用户名>
python main.py repos <用户名> --out user_repos.csv
```

- `repo`、`issues`、`contributors` 传仓库链接或 owner/repo，如 facebook/react。
- `issues` 同时返回 Issue 和 PR，用 `is_pull_request` 区分；默认只列 open 的。
- `user` 和 `repos` 传用户名，可用 `contributors` 结果里的 `username`；组织账号也可以。
- 不加 `--out` 时打印前 3 条 JSON；加 `--out` 存成 .csv 或 .json。CSV 带 BOM，Excel 直接打开不乱码。
- API Key 在 everyinfra.com 注册后到控制台创建，步骤见 <https://everyinfra.com/docs?utm_source=github&utm_medium=example_repo&utm_campaign=github-api#quickstart>

### 用 curl 调

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"github","action":"repository","params":{"url":"https://github.com/facebook/react"}}'
```

所有能力都发到同一个地址，换 `action` 和 `params` 就行；`repository_issues`、`contributors`、`user`、`user_repositories` 的写法见 [examples/curl.sh](examples/curl.sh)。

### 接进 Claude、Cursor（MCP）

远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key；服务器由 EveryInfra 运行，不用装本地程序。

Claude Code：

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor 等读 `mcp.json` 的客户端（[examples/mcp.json](examples/mcp.json)）：

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Claude 网页版和桌面版的自定义连接器、ChatGPT 只能填网址：填 <https://api.everyinfra.com/mcp/all>，连接时登录 EveryInfra 并允许，不用填 Key。完整步骤见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>

### 价格

| 能力 | `action` | 每千次 |
|---|---|---|
| 仓库详情 | `repository` | $0.96 |
| 仓库的 Issue 与 PR | `repository_issues` | $0.96 |
| 仓库贡献者 | `contributors` | $0.96 |
| 用户资料 | `user` | $0.96 |
| 用户的仓库 | `user_repositories` | $0.96 |

- 按调用次数计费，每次约 $0.00096；失败、空结果、参数错误和鉴权失败都不收费。
- 新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>
- GitHub 其他 4 个能力的单价见平台页 <https://everyinfra.com/github-api?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>

### 返回字段

下面是这 5 个能力实测返回的字段，含义取自接口文档每条说明的第一句，完整说明在每张表下面的链接里。

#### `repository`（仓库详情）

| 字段 | 含义 |
|---|---|
| `id` | GitHub 内部数字 ID（字符串）。 |
| `full_name` | 仓库全名 owner/repo；仓库改过名或转过主人时是新名字。 |
| `name` | 仓库名（不含 owner）。 |
| `owner_username` | 仓库主人（用户或组织）的用户名。 |
| `owner_url` | 仓库主人的 GitHub 主页链接。 |
| `owner_avatar_url` | 仓库主人的头像链接。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `description` | 简介或描述，通常比 text 短。 |
| `homepage` | 仓库填写的项目主页；没填时没有这个字段。 |
| `language` | 仓库的主要编程语言，如 Python；GitHub 没判定出语言时不返回这个字段。 |
| `license` | 开源许可证名称（如 MIT License）；没声明时没有；分叉列表不给。 |
| `topics` | 仓库主题标签列表；没有时没有这个字段。 |
| `star_count` | 星标数。 |
| `fork_count` | 分叉数。 |
| `open_issue_count` | 未关闭的 Issue 加 PR 数（GitHub 口径）。 |
| `default_branch` | 默认分支名。 |
| `is_fork` | 这个仓库本身是不是分叉（repository / user_repositories）。 |
| `is_archived` | 仓库是否已归档（只读）。 |
| `size_kb` | 仓库大小，单位 KB（GitHub 口径）。 |
| `created_at` | 创建时间，格式同 posted_at。 |
| `updated_at` | 最近更新时间，ISO 8601 UTC。 |
| `pushed_at` | 最近一次推送代码的时间，ISO 8601 UTC（repository / user_repositories / forks）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/github-api/repository?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>

#### `repository_issues`（仓库的 Issue 与 PR）

| 字段 | 含义 |
|---|---|
| `id` | GitHub 内部数字 ID（字符串）。 |
| `number` | Issue 或 PR 在仓库里的编号。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `title` | 标题。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `state` | open 或 closed。 |
| `is_pull_request` | 这一条是 PR（true）还是 Issue（false）。 |
| `is_draft` | PR 是否草稿；Issue 为 false。 |
| `labels` | 标签名列表；没有标签时没有这个字段。 |
| `comment_count` | 评论数。 |
| `reaction_count` | 表情回应总数。 |
| `repository` | 所在仓库 owner/repo。 |
| `author_username` | 作者用户名（@handle），通常可用于拼 URL。 |
| `author_id` | 作者在原平台的唯一 ID。 |
| `author_avatar_url` | 作者头像图片链接（多数平台带签名、会过期）。 |
| `author_type` | 作者账号类型：User、Bot 或 Organization。 |
| `author_association` | 作者和仓库的关系，GitHub 原值：OWNER、MEMBER、COLLABORATOR、CONTRIBUTOR、FIRST_TIME_CONTRIBUTOR、NONE 等。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `updated_at` | 最近更新时间，ISO 8601 UTC。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/github-api/repository_issues?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>

#### `contributors`（仓库贡献者）

| 字段 | 含义 |
|---|---|
| `rank` | 在这次返回里的名次，从 1 开始（contributors 按提交数，trending 按 GitHub Trending 榜单顺序）。 |
| `username` | 用户名（@handle）。 |
| `id` | GitHub 内部数字 ID（字符串）。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `avatar_url` | 头像图片链接。 |
| `contribution_count` | 在这个仓库的提交数（contributors）。 |
| `account_type` | 账号类型：User、Bot 或 Organization。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/github-api/contributors?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>

#### `user`（用户资料）

| 字段 | 含义 |
|---|---|
| `username` | 用户名（@handle）。 |
| `id` | GitHub 内部数字 ID（字符串）。 |
| `display_name` | 显示名，可能与 username 不同。 |
| `company` | 个人资料里填的公司；没填时没有。 |
| `location` | 地理位置描述，原文透传，格式随平台而异。 |
| `follower_count` | 粉丝数。 |
| `following_count` | 关注数。 |
| `public_repo_count` | 公开仓库数。 |
| `public_gist_count` | 公开 Gist 数。 |
| `avatar_url` | 头像图片链接。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `account_type` | 账号类型：User、Bot 或 Organization。 |
| `created_at` | 创建时间，格式同 posted_at。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/github-api/user?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>

#### `user_repositories`（用户的仓库）

| 字段 | 含义 |
|---|---|
| `id` | GitHub 内部数字 ID（字符串）。 |
| `full_name` | 仓库全名 owner/repo；仓库改过名或转过主人时是新名字。 |
| `name` | 仓库名（不含 owner）。 |
| `owner_username` | 仓库主人（用户或组织）的用户名。 |
| `owner_url` | 仓库主人的 GitHub 主页链接。 |
| `owner_avatar_url` | 仓库主人的头像链接。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `description` | 简介或描述，通常比 text 短。 |
| `star_count` | 星标数。 |
| `fork_count` | 分叉数。 |
| `open_issue_count` | 未关闭的 Issue 加 PR 数（GitHub 口径）。 |
| `default_branch` | 默认分支名。 |
| `is_fork` | 这个仓库本身是不是分叉（repository / user_repositories）。 |
| `is_archived` | 仓库是否已归档（只读）。 |
| `size_kb` | 仓库大小，单位 KB（GitHub 口径）。 |
| `created_at` | 创建时间，格式同 posted_at。 |
| `updated_at` | 最近更新时间，ISO 8601 UTC。 |
| `pushed_at` | 最近一次推送代码的时间，ISO 8601 UTC（repository / user_repositories / forks）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `homepage` | 仓库填写的项目主页；没填时没有这个字段。 |
| `language` | 仓库的主要编程语言，如 Python；GitHub 没判定出语言时不返回这个字段。 |
| `license` | 开源许可证名称（如 MIT License）；没声明时没有；分叉列表不给。 |

完整参数和字段：<https://everyinfra.com/github-api/user_repositories?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>

### 常见问题

**调用时要不要提供 GitHub 账号或 Cookie？**

不用，请求头带 `Authorization: Bearer` 和 API Key 就能调，请求体写 `platform`、`action` 和能力参数。不用扫码、维护登录状态，也不用开浏览器。

**怎么收费？失败了收不收钱？有免费额度吗？**

按调用次数计费，每千次 $0.81 起。失败、空结果、参数错误和鉴权失败都不收费。新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见定价页 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>

**能把 GitHub 接口接进 Claude、Cursor 吗？**

能，远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key，不用装本地程序。Claude、Cursor、ChatGPT、Claude Code 配置见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>。

**用 GitHub 数据要注意哪些合规问题？**

EveryInfra 服务条款要求你自行确保数据用法符合适用法律和相关平台条款，禁止用于违法、侵犯隐私或知识产权，或批量抓取用于骚扰、欺诈等恶意用途。用到昵称、头像等个人信息时，只留业务用得上的字段。

**可以拿到 GitHub 的哪些数据？**

GitHub 有 9 个能力：仓库详情、用户资料、用户的仓库、仓库的 Issue 与 PR、Issue 搜索、Issue 评论、仓库贡献者、仓库分叉、热榜。每个能力的参数和返回字段见平台页 <https://everyinfra.com/github-api?utm_source=github&utm_medium=example_repo&utm_campaign=github-api>

### 实测记录

发布前用本仓的代码对线上接口跑过一遍，命令就是「快速开始」里的 5 条。

| 命令 | 时间（新加坡时间） | 返回条数 | 扣费 |
|---|---|---|---|
| `python main.py repo "https://github.com/facebook/react"` | 2026-11-25 13:17 | 1 | $0.000958 |
| `python main.py issues "https://github.com/facebook/react" --out issues.csv` | 2026-11-25 13:17 | 30 | $0.000958 |
| `python main.py contributors "https://github.com/facebook/react" --out contributors.csv` | 2026-11-25 13:18 | 30 | $0.000958 |
| `python main.py user <用户名>` | 2026-11-25 13:18 | 1 | $0.000958 |
| `python main.py repos <用户名> --out user_repos.csv` | 2026-11-25 13:18 | 30 | $0.000958 |

`repository` 返回的一条（正文截到 60 字，作者字段没放进来）：

```json
{
  "id": "10270250",
  "description": "The library for web and native user interfaces.",
  "language": "JavaScript",
  "star_count": 252887,
  "fork_count": 51803,
  "open_issue_count": 1596,
  "updated_at": "2026-11-25T05:08:23+00:00"
}
```

## License

MIT
