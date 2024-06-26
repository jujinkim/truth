from github import Github
import subprocess
import config

class GitCommitter:

    def __init__(self, repo_path, github_token, user_name, repo_name):
        self.repo_path = repo_path
        self.github_token = github_token
        self.repo_name = repo_name
        self.user_name = user_name
        self.new_post_branch_prefix = 'post/new-post-' + config.url_tistory.replace('.', '-') + '-'

    def checkout_n_create_branch(self, post_num):
        branch_name  = f'{self.new_post_branch_prefix}{post_num}'
        #checkout 'main' and create new branch, if there is already branch, it will checkout to the branch
        subprocess.check_output(['git', '-C', self.repo_path, 'checkout', 'main'])
        try:
            subprocess.check_output(['git', '-C', self.repo_path, 'checkout', branch_name])
        except subprocess.CalledProcessError:
            subprocess.check_output(['git', '-C', self.repo_path, 'checkout', '-b', branch_name])
        return branch_name        

    def commit_and_push_to_postnum_branch(self, post_num):
        #commit and push
        subprocess.check_output(['git', '-C', self.repo_path, 'add', '.'])
        subprocess.check_output(['git', '-C', self.repo_path, 'commit', '-m', 'Add new post: ' + config.url_tistory + '/' + post_num])
        subprocess.check_output(['git', '-C', self.repo_path, 'push', 'origin', self.new_post_branch_prefix + post_num])

    def create_pull_request_n_cleanup(self, post_num):
        #create pull request
        g = Github(self.github_token)
        repo = g.get_user().get_repo(self.repo_name)
        repo.create_pull(title='Add new post: ' + post_num, body='This is an automated pull request', head=self.new_post_branch_prefix + post_num, base='main')
        #cleanup branch
        subprocess.check_output(['git', '-C', self.repo_path, 'checkout', 'main'])
        subprocess.check_output(['git', '-C', self.repo_path, 'branch', '-D', self.new_post_branch_prefix + post_num])