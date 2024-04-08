import sys
from config import *

def main(postNum):
    read_config()
    postUrl = url_tistory + "/" + postNum
    print("Tistory post url: ", postUrl)

    pass

if __name__ == '__main__':
    main(sys.argv[1])