from argparse import ArgumentParser, Namespace
from json import load
from os.path import exists

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

x_variable = "issue_number"
y_variable = "comments"


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
        "-c",
        "--comments-per-issues-graph-filename",
        help="The filename of the graph of number of issues",
        type=str,
        required=True,
    )

    return parser.parse_args()


def plot_CommentsPerIssue_Line(
    pregeneratedData: list = None,
    filename: str = "comments_per_issue.png",
):
    figure: Figure = plt.figure()

    plt.title("Number of Comments Per Issue Number")
    plt.ylabel("Number of Comments")
    plt.xlabel("Issues Number")

    data: list = pregeneratedData
    issue_number: list = []
    number_of_comments: list = []
    for pair in data:
        issue_number.append(pair[x_variable])
        number_of_comments.append(pair[y_variable])

    plt.plot(issue_number, number_of_comments)
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

    comments_per_issue: list = json_1

    plot_CommentsPerIssue_Line(
        pregeneratedData=comments_per_issue,
        filename=args.comments_per_issues_graph_filename,
    )


if __name__ == "__main__":
    main()
