url_tistory = ""

def read_config():
    with open('truth_config.txt') as f:
        for line in f:
            name, value = line.strip().split('=', 1)
            if name == 'url_tistory':
                globals()[name] = value