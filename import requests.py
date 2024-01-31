import requests
from datetime import datetime, timedelta
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_repository_stats_by_month(owner, repo_name, start_month, end_month, access_token):
    base_url = f"https://api.github.com/repos/{owner}/{repo_name}"
     # 获取仓库信息
    repo_info_response = requests.get(base_url)

    # 检查响应状态
    if repo_info_response.status_code != 200:
        print(f"Failed to retrieve repository information. Status code: {repo_info_response.status_code}")
        return

    repo_info = repo_info_response.json()

    # 打印仓库基础信息
    print("Repository Information:")
    print("Name:", repo_info.get('name', 'N/A'))
    print("Description:", repo_info.get('description', 'N/A'))
    print("Stars:", repo_info.get('stargazers_count', 'N/A'))
    print("Forks:", repo_info.get('forks_count', 'N/A'))
    print("Watchers:", repo_info.get('subscribers_count', 'N/A'))
    print("Issues:", repo_info.get('open_issues_count', 'N/A'))
    print("URL:", repo_info.get('html_url', 'N/A'))
    print("\n")
    # 创建一个带重试机制的 Session
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    for year in range(start_month[0], end_month[0] + 1):
        for month in range(1, 13):
            if (year, month) > end_month:
                break

            first_day = f"{year}-{month:02d}-01T00:00:00Z"
            last_day = (datetime(year, month, 1) + timedelta(days=32)).replace(day=1).isoformat()

            # 随机化延迟，避免被封禁
            delay = random.uniform(0.5, 1.5)  # 随机延迟1到3秒
            time.sleep(delay)

            headers = {
                "Authorization": f"token {access_token}",
                "Accept": "application/vnd.github.v3+json"
            }

            # 添加超时设置和重试机制
            try:
                # 获取每月的提交数量
                commits_url = f"{base_url}/commits?since={first_day}&until={last_day}&per_page=100"
                commits = get_all_pages(commits_url, headers, session)
                commit_count = len(commits)

                # 获取每月的已解决问题数量
                resolved_issues_url = f"{base_url}/issues?since={first_day}&until={last_day}&per_page=100&state=closed"
                resolved_issues = get_all_pages(resolved_issues_url, headers, session)
                resolved_issues_count = len(resolved_issues)

                # 获取每月的评论数量
                comments_url = f"{base_url}/issues/comments?since={first_day}&until={last_day}&per_page=100"
                comments = get_all_pages(comments_url, headers, session)
                comment_count = len(comments)

                # 获取每月的贡献者数量
                contributors_url = f"{base_url}/contributors?since={first_day}&until={last_day}&per_page=100"
                contributors = get_all_pages(contributors_url, headers, session)
                contributor_count = len(contributors)

                # 打印每月的统计信息
                print(f"\nStats for {year}-{month:02d}:")
                print(f"Commit Count: {commit_count}")
                print(f"Resolved Issues Count: {resolved_issues_count}")
                print(f"Comment Count: {comment_count}")
                print(f"Contributor Count: {contributor_count}")

            except Exception as e:
                print(f"Error during request: {e}")

def get_all_pages(url, headers, session):
    all_results = []
    page = 1
    while True:
        response = session.get(f"{url}&page={page}", headers=headers, timeout=10)
        results = response.json()
        if not results:
            break
        all_results.extend(results)
        page += 1
    return all_results

if __name__ == "__main__":
    # 请替换为您要爬取的仓库的 owner 和 repo_name
    owner = "freeCodeCamp"
    repo_name = "freeCodeCamp"

    # 获取过去十年的信息（2014年1月至2023年12月）
    start_month = (2023, 1)
    end_month = (2023, 12)

    # 替换为您的个人访问令牌
    access_token = "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"

    get_repository_stats_by_month(owner, repo_name, start_month, end_month, access_token)