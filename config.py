url_tistory = ""
title_tag_selector = "article#content .inner h1"
article_tag_selector = "#article-view .tt_article_useless_p_margin.contents_style"
repo_path = ""
repo_name = ""
github_token = ""

def read_config():
    with open('truth_config.txt') as f:
        for line in f:
            name, value = line.strip().split('=', 1)
            if name == 'url_tistory':
                globals()[name] = value
            elif name == 'title_tag_selector':
                globals()[name] = value
            elif name == 'article_tag_selector':
                globals()[name] = value
            elif name == 'repo_path':
                globals()[name] = value
            elif name == 'repo_name':
                globals()[name] = value
            elif name == 'github_token':
                globals()[name] = value

    # write the config variables to truth_config.txt again
    with open('truth_config.txt', 'w') as f:
        f.write(f'url_tistory={url_tistory}\n')
        f.write(f'title_tag_selector={title_tag_selector}\n')
        f.write(f'article_tag_selector={article_tag_selector}\n')
        f.write(f'repo_path={repo_path}\n')
        f.write(f'repo_name={repo_name}\n')
        f.write(f'github_token={github_token}\n')
    