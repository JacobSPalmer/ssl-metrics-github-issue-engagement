from argparse import ArgumentParser, Namespace
from os.path import exists

#TODO specify from _ import _
import pathlib
import json

def get_argparse() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="GH Issue Engagement",
        usage="This program generates JSON file containing specific data related to a repositories issue engagement.",
    )
    parser.add_argument(
        "-i",
        "--input",
        help="Raw repository issues json file to be used. These files can be generated using the "
             "ssl-metrics-github-issues tool.",
        default="issues.json",
        type=str,
        required=False,
    )
    parser.add_argument(
        "-s",
        "--save-json",
        help="Specify name to save analysis to JSON file.",
        default="issue_engagement.json",
        type=str,
        required=True,
    )
    return parser.parse_args()

def getIssueEngagementReport(
        input_json: str,
) -> list:

    with open(pathlib.Path("../issues.json")) as json_file:
    # with open("issues.json") as json_file:
        data = json.load(json_file)
        data = [dict(issue_number=k1['number'],
                     comments=k1['comments']) for k1 in data]

    return data

def storeJSON(
        issues: list,
        output_file: str,
) -> bool:
    data = json.dumps(issues)
    file = pathlib.Path("../{}".format(output_file))
    # file = output_file
    with open(file=file, mode="w") as json_file:
        json_file.write(data)
    return exists(file)

def main() -> None:
    args: Namespace = get_argparse()

    issues_json = getIssueEngagementReport(
        input_json=args.input,
    )

    storeJSON(
        issues=issues_json,
        output_file=args.save_json,
    )

if __name__ == "__main__":
    # main()
    storeJSON(
        issues=getIssueEngagementReport("input.json"),
        output_file="IE_report.json",
    )

