import requests
from datetime import datetime, timedelta
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

x_month = []
commit_count_add_speed = []
issues_count_add_speed = []
resolved_issues_add_speed = []
comments_count_add_speed = []
contributor_count_add_speed = []

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

            x_month.append(month)

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
                # 获取每月问题数量
                issues_url = f"{base_url}/issues?since={first_day}&until={last_day}&state=all&per_page=100"
                issues = get_all_pages(issues_url, headers, session)
                issues_count = len(issues)
                issues_count_add_speed.append(issues_count / 30)

                # 获取每月的提交数量
                commits_url = f"{base_url}/commits?since={first_day}&until={last_day}&per_page=100"
                commits = get_all_pages(commits_url, headers, session)
                commit_count = len(commits)
                commit_count_add_speed.append(commit_count / 30)

                # 获取每月的已解决问题数量
                resolved_issues_url = f"{base_url}/issues?since={first_day}&until={last_day}&per_page=100&state=closed"
                resolved_issues = get_all_pages(resolved_issues_url, headers, session)
                resolved_issues_count = len(resolved_issues)
                resolved_issues_add_speed.append(resolved_issues_count / 30)

                # 获取每月的评论数量
                comments_url = f"{base_url}/issues/comments?since={first_day}&until={last_day}&per_page=100"
                comments = get_all_pages(comments_url, headers, session)
                comment_count = len(comments)
                comments_count_add_speed.append(comment_count / 30)

                # 获取每月的贡献者数量
                # contributors_url = f"{base_url}/contributors?since={first_day}&until={last_day}&per_page=100"
                # contributors = get_all_pages(contributors_url, headers, session)
                # contributor_count = len(contributors)
                # contributor_count_add_speed.append(contributor_count / 30)

                # 打印每月的统计信息
                print(f"\nStats for {year}-{month:02d}:")
                print(f"Commit Count: {commit_count}")
                print(f"Issues Count: {issues_count}")
                print(f"Resolved Issues Count: {resolved_issues_count}")
                print(f"Comment Count: {comment_count}")
                # print(f"Contributor Count: {contributor_count}")

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

def draw_axis(ax, list_x, list_y, draw_color, draw_style):
    sort, x, y = [], [], []
    for i in range(len(list_x)):
        sort.append((list_x[i], list_y[i]))

    new_sort = sorted(sort, key=lambda x:x[0])
    for i in range(len(new_sort)):
        x.append(new_sort[i][0])
        y.append(new_sort[i][1])

    ax.plot(x, y, color=draw_color, linestyle=draw_style, label='resolved_issues')


def create_plt_picture(owners, repo_names, start_month, end_month, access_token, colors, style):
    """
    绘制关系图
    :param owners: owners列表
    :param repo_names: repo_names列表
    :param start_month: 开始日期
    :param end_month: 结束日期
    :param access_token: 令牌
    :param colors: 颜色
    :param style: 样式
    :return: null
    """
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(12, 12))

    ax1 = fig.add_subplot(221)
    ax1.set_xlabel("commit count speed")
    ax1.set_ylabel('resolved issues speed')
    ax1.set_title('relationship between resolved issues speed and commit count speed')

    ax2 = fig.add_subplot(222)
    ax2.set_xlabel("issues count speed")
    ax2.set_ylabel('resolved issues speed')
    ax2.set_title('relationship between resolved issues speed and issues count speed')

    ax3 = fig.add_subplot(223)
    ax3.set_xlabel("comments count speed")
    ax3.set_ylabel('resolved issues speed')
    ax3.set_title('relationship between resolved issues speed and comments count speed')

    # ax4 = fig.add_subplot(224)
    # ax4.set_xlabel("contributor count speed")
    # ax4.set_ylabel('resolved issues speed')
    # ax4.set_title('relationship between resolved issues speed and contributor count speed')


    for i in range(len(owners)):
        get_repository_stats_by_month(owners[i], repo_names[i], start_month, end_month, access_token)
        draw_axis(ax1, commit_count_add_speed, resolved_issues_add_speed, colors[i], style[i])
        draw_axis(ax2, issues_count_add_speed, resolved_issues_add_speed, colors[i], style[i])
        draw_axis(ax3, comments_count_add_speed, resolved_issues_add_speed, colors[i], style[i])
        # draw_axis(ax4, contributor_count_add_speed, resolved_issues_add_speed, colors[i], style[i])
        commit_count_add_speed.clear()
        issues_count_add_speed.clear()
        comments_count_add_speed.clear()
        # contributor_count_add_speed.clear()
        resolved_issues_add_speed.clear()

    fig.suptitle("resolved issues influenced by the speed of commit counts, comments counts and contributors", y=0.015)
    plt.tight_layout()

    # 图片存储路径
    plt.savefig("C:\\Users\\86183\\Desktop\\result.png")
    plt.clf()

if __name__ == "__main__":
    # 请替换为您要爬取的仓库的 owner 和 repo_name
    # 下为owners, repo_name的列表，以及他们所对应的颜色和线
    owners = ["meteor", "left", "kong", "apache"]
    repo_names = ["meteor", "left", "kong", "dubbo"]
    colors = ['red', "yellow", 'blue', 'black']
    style = ['-', ":", '-.', '--']

    # 获取过去十年的信息（2014年1月至2023年12月）
    start_month = (2023, 1)
    end_month = (2023, 6)

    # 替换为您的个人访问令牌
    access_token = "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"

    create_plt_picture(owners, repo_names, start_month, end_month, access_token, colors, style)


