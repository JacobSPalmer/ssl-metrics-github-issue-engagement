from argparse import ArgumentParser, Namespace
from datetime import datetime
from json import load
from os.path import exists
from typing import Any, KeysView

import matplotlib.pyplot as plt
from dateutil.parser import parse
from intervaltree import IntervalTree
from matplotlib.figure import Figure
from progress.bar import Bar


def get_argparse() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="PROGRAM NAME",
        usage="PROGRAM DESCRIPTION",
    )
    parser.add_argument(
        "-i",
        "--input",
        help="The input JSON file that is to be used for graphing",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-s",
        "--issues_per_day_line_filename",
        help="The filename of the graph of number of issues per day",
        type=str,
        required=True,
    )

    return parser.parse_args()


def createIntervalTree(
    data: list, filename: str = "issues_to_graph2.json"
) -> IntervalTree:
    tree: IntervalTree = IntervalTree()
    day0: datetime = parse(data[0]["created_at"]).replace(tzinfo=None)

    with Bar(f"Creating interval tree from {filename}... ", max=len(data)) as pb:
        for issue in data:
            createdDate: datetime = parse(issue["created_at"]).replace(tzinfo=None)
            if issue["state"] == "closed":
                closedDate: datetime = parse(issue["closed_at"]).replace(tzinfo=None)
            else:
                closedDate: datetime = datetime.now(tz=None)

            begin: int = (createdDate - day0).days
            end: int = (closedDate - day0).days

            try:
                issue["endDayOffset"] = 0
                tree.addi(begin=begin, end=end, data=issue)
            except ValueError:
                issue["endDayOffset"] = 1
                tree.addi(begin=begin, end=end + 1, data=issue)
            pb.next()

    return tree


def fillDictBasedOnKeyValue(
    dictionary: dict, tree: IntervalTree, key: str, value: Any
) -> dict:
    data: dict = {}
    keys: KeysView = dictionary.keys()

    maxKeyValue: int = max(keys)
    minKeyValue: int = min(keys)

    with Bar(
        f'Getting the total number of "{key} = {value}" issues per day... ',
        max=maxKeyValue,
    ) as pb:
        for x in range(minKeyValue, maxKeyValue):
            try:
                data[x] = dictionary[x]
            except KeyError:
                count = 0
                interval: IntervalTree
                for interval in tree.at(x):
                    if interval.data[key] == value:
                        count += 1
                data[x] = count

            pb.next()

    return data


def plot_IssuesPerDay_Line(
    pregeneratedData_Issues: dict = None,
    filename: str = "issues_per_day_line.png",
):
    figure: Figure = plt.figure()

    plt.title("Number of Issues Per Day")
    plt.ylabel("Number of Issues")
    plt.xlabel("Day")

    data: dict = pregeneratedData_Issues

    plt.bar(data.keys(), data.values(), color="blue")

    figure.savefig(filename)

    return exists(filename)


def main() -> None:
    args: Namespace = get_argparse()

    if args.input[-5::] != ".json":
        print("Invalid input file type. Input file must be JSON")
        quit(1)

    with open(args.input, "r") as data:
        json_1 = load(data)
        data.close()

    tree: IntervalTree = createIntervalTree(data=json_1, filename=args.input)

    startDay: int = tree.begin()
    endDay: int = tree.end()

    if len(tree.at(endDay)) == 0:
        endDay -= 1

    baseDict: dict = {startDay: len(tree.at(startDay)), endDay: len(tree.at(endDay))}

    issues: dict = fillDictBasedOnKeyValue(
        dictionary=baseDict, tree=tree, key="state", value="open"
    )

    plot_IssuesPerDay_Line(
        pregeneratedData_Issues=issues,
        filename=args.issues_per_day_line_filename,
    )


if __name__ == "__main__":
    main()
