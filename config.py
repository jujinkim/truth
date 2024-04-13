url_tistory = ""
title_tag_selector = "article#content .inner h1"
article_tag_selector = "#article-view .tt_article_useless_p_margin.contents_style"

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