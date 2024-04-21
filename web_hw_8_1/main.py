from typing import List, Any, Dict

from models import Author, Quote


def find_by_tag(tag: str) -> list[str | None]:
    print(f"Find by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


def find_by_author(author: str) -> dict[Any, list[Any]]:
    print(f"Find by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


def main():
    while True:
        message = input(">>>   ")
        if message == "exit":
            break
        find_by, value = message.split(":")
        if find_by == "name":
            result = find_by_author(value.strip())
            print(result)
        if find_by == "tag":
            result = find_by_tag(value)
            print(result)
        if find_by == "tags":
            result = []
            for tag in value.split(","):
                result.extend(find_by_tag(tag))
            print(result)


if __name__ == '__main__':
    main()