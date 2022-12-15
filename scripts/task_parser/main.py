from task_parser import Page


def main(): 
    page = Page(url="https://codeforces.com/contest/1769/problem/A")
    page.write_to_file()
    page.dispose()

if __name__ == "__main__":
    main()


