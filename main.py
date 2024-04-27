import config
import argparse
from git_committer import *
from article_downloader import *
from hugo_post_creator import *
import os

testfiles_path = 'testfiles'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("postNum", type=int, help="the post number of the tistory post")
    parser.add_argument("--debug", help="instead of create commit, create debug file output")
    args = parser.parse_args()

    configSuccess = config.read_config(args.debug)
    # Check config variables
    if (not configSuccess):
        print("Please fill the config variables in truth_config.txt")
        return
    
    # Check if the post number is valid
    if (args.postNum < 1):
        print("Post number should be greater than 0")
        return
    
    postNum = str(args.postNum)
    fullUrl = "https://" + config.url_tistory + '/' + postNum
    print("Tistory post url: ", fullUrl)

    # 1. Create and checkout git branch (not debug mode)
    print("Creating and checking out git branch")
    if (not args.debug):
        git = GitCommitter(config.repo_path, config.github_token, config.user_name, config.repo_name)
        branch_name = git.checkout_n_create_branch(postNum)

    # 2. Download article
    print("Downloading article")
    articledl = ArticleDownloader()
    article = articledl.download_article(
        fullUrl,
        config.title_tag_selector,
        config.article_tag_selector
    )

    print("Title: ", article.title)
    print("Year", datetime.fromisoformat(article.published_time).year if article.published_time else datetime.now().year)
    print("Url: ", article.link)
    if (args.debug):
        # Write downloaded article to debug file
        with open(f'{testfiles_path}\{postNum}.txt', 'w', encoding='utf-8') as f:
            f.write(article.title + '\n--------\n' + article.link + '\n--------\n' + article.content)

    # 3. Create post file
    print("Creating post file")
    post_creator = HugoPostCreator()
    file_name = config.url_tistory.replace('.', '-') + '-' + postNum + '.md'
    debug_file_path = os.path.join(testfiles_path, file_name)
    year = str(datetime.fromisoformat(article.published_time).year) if article.published_time else str(datetime.now().year)
    post_file_path = os.path.join(config.repo_path, 'content', 'post', year, file_name)
    postPath = debug_file_path if args.debug else post_file_path
    post_creator.create_post(article, postPath)

    # If debug mode, return
    if (args.debug):
        return

    # 4. Push to the git repository
    print("Pushing to git repository")
    git.commit_and_push_to_postnum_branch(postNum)

    # 5. Create pull request
    print("Creating pull request")
    git.create_pull_request_n_cleanup(postNum)

    print("Done")

if __name__ == '__main__':
    main()