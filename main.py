from config import *
import argparse
from git_committer import *
from rss_downloader import *
from article_downloader import *
from hugo_post_creator import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rss", help="if existed, download the article from the rss url")
    parser.add_argument("postNum", type=int, help="the post number of the tistory post")
    parser.add_argument("--debug", help="instead of create commit, create debug file output")
    args = parser.parse_args()

    configSuccess = read_config(args.debug)
    # Check config variables
    if (not configSuccess):
        print("Please fill the config variables in truth_config.txt")
        return
    
    # Check if the post number is valid
    if (args.postNum < 1):
        print("Post number should be greater than 0")
        return
    
    postNum = str(args.postNum)
    print("Tistory post url: ", url_tistory + postNum)

    # 1. Create and checkout git branch (not debug mode)
    if (not args.debug):
        git = GitCommitter(repo_path, github_token, repo_name)
        branch_name = git.checkout_n_create_branch(postNum)

    # 2. Download article
    if (args.rss):
        rssdl = RssDownloader()
        article = rssdl.get_feed_entries(args.rss, postNum)
    else:
        articledl = ArticleDownloader()
        article = articledl.download_article(url_tistory + postNum)

    print("Title: ", article.title)
    print("Url: ", article.url)
    if (args.debug):
        print("Article: ", article.content)
        with open('post_debug.md', 'w') as f:
            f.write(f'# {article.title}\n\n')
            f.write(f'[Link]({article.url})\n\n')
            f.write(article.content)
        return

    # 3. Create post file
    post_creator = HugoPostCreator()
    post_creator.create_post(article, f'{repo_path}/content/posts/{postNum}.md')

    # 4. Push to the git repository
    git.commit_and_push_to_postnum_branch(postNum)

    # 5. Create pull request
    git.create_pull_request_n_cleanup(postNum)

if __name__ == '__main__':
    main()