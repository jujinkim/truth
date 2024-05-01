# truth

**T**istroy a**R**ticle **U**mm... **T**o **H**ugo(Git/Github pages)  
This does:

1. Gets your tistory article.
2. Translates your article to another language.
3. Converts your article into markdown, and create Hugo article content file.
4. Creates new git branch for new post, and push/create pull request at your Github Hugo source repo.
5. Removes created temp branch.

All you have to do is just check converted hugo post file and accept the pull request.

## How to run

1. Clone this repo.
2. Create virtual environment using venv or any other tool you prefer.
3. Install required packages using setup.py or requirements.txt file.
4. Run `main.py` with arguments.
    - You need to create a setting file(`truth_config.txt`). It will be generated at the first run of `main.py`.

## Run

```bash
 python main.py <postnum>
```

I recommend setting your Tistory blog to use a number type for the post url.

## truth_config.txt

- url_tistory= Your tistory blog url, without protocol. e.g) `blog.jujinkim.com`
- title_tag_selector= Title tag selector at your tistory blog. e.g) `article#content .inner h1`
- article_tag_selector= Article tag selector at your tistoyr lbog. e.g) `#article-view .contents_style`
- repo_path= Your local Hugo site source repository directory path. e.g) `F:\Project_GIT\hugo-jujinkim-com`
- repo_name= Your Hugo site source repository name at GitHub. e.g) `hugo-jujinkim-com`
- github_token= Your GitHub Hugo site source repo token to make pull request. e.g) `github_pat_blahblah`
  - `Write access to pull requests` is required. **DO NOT share your GitHub Token.**
- from_lang= Your tistory article language. alpha-2 iso code. e.g) `ko`
- to_lang= Target langauge to translate. alp ha-2 iso code. e.g) `en`


## Why Tistory API is not used?

Damn. it was deprecated and no more supported from Feb 2024~.
