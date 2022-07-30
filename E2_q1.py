import json
from typing import Dict, List


def checks_invited_guests_violating_restrictions(guests, k):
    for id in guests:
        if guests[id]["status"] == "invited" and (guests[id]["known"] < k or guests[id]["unknown"] < k):
            return True

    return False


def main():
    n: int = 25
    k: int = 3

    # all guests must known and unknown of at least k other guests

    # example of relation
    # if (a, b) => (b, a) naturally occurs
    friends: List = [
        (1, 2), (1, 3), (1, 4),
        (2, 4), (2, 5),
        (3, 5), (3, 6), (3, 7),
        (4, 5),
        (6, 7), (6, 8),
        (7, 8),
        (8, 4),
        (20, 1), (20, 2), (20, 3)
    ]

    print(f"Candidates size is {n} and pairs of friends of size {len(friends)}")
    # for a, b in friends:
    #     print(a, b)

    # create list of guests
    guests: Dict = {}

    # O(n)
    for i in range(n):
        guests[i+1] = {
            "status": "invited",
            "known": 0,
            "unknown": abs(n)
        }

    # O(m)
    for a, b in friends:
        guests[a]["known"] += 1
        guests[a]["unknown"] -= 1

        guests[b]["known"] += 1
        guests[b]["unknown"] -= 1

    print(json.dumps(guests, indent=2, sort_keys=True))

    total_uninviting: int = 0
    while checks_invited_guests_violating_restrictions(guests, k):
        uninvited = {}

        # O(n)
        for id in guests:
            if guests[id]["status"] == "invited" and (guests[id]["known"] < k or guests[id]["unknown"] < k):
                # print(f"Uninviting guest { id }")

                guests[id]["status"] = "uninvited"
                guests[id]["known"] = 0
                guests[id]["unknown"] = 0

                uninvited[id] = True
                n -= 1

        print(f"Uninvited size is { len(uninvited) }")

        # O(m)
        for a, b in friends:
            # works only if (a,b) appears once

            # O(1)
            # it's just that using the hash is the obvious way to implement
            # __contains__ on a hash table
            if a in uninvited and b not in uninvited:
                print(f"{a} was uninvited but {b} was not, should update {b} known list")

                guests[b]["known"] -= 1
                guests[b]["unknown"] = abs(n - guests[b]["known"])

            if b in uninvited and a not in uninvited:
                print(f"{b} was uninvited but {a} was not, should update {a} known list")

                guests[a]["known"] -= 1
                guests[a]["unknown"] = abs(n - guests[a]["known"])

            # only updates guests unknown
            if a not in uninvited and b not in uninvited:
                guests[a]["unknown"] = abs(n - guests[a]["known"])
                guests[b]["unknown"] = abs(n - guests[b]["known"])

            print(json.dumps(guests, indent=2, sort_keys=True))

    count: int = 0
    for id in guests:
        if guests[id]["status"] == "invited":
            count += 1
            print(f"Guest {id} invite: {guests[id]}")

    print(f"Total number of guests: {count}")


# entry point
if __name__ == "__main__":
    main()