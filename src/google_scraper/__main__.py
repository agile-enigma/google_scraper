import sys
import getopt
import google_scraper


def main():
    help_menu = (
        "\nGoogle Scraper..."
        "\nFor detailed information on usage and additional features see the README."
        + "\n\nUsage: python3 google_scraper.py [OPTIONS]"
        + "\n\nOptions:"
        + "\n\t--help/-h: display this help menu"
        + "\n\t--start_date/-s: takes start date as argument. format: mm/dd/yyyy"
        + "\n\t--end_date/-e: takes end date as argument. format: mm/dd/yyyy"
        + "\n\t--query/-q: takes Google search query as argument. enclose in single quotes"
    )

    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "hs:e:q:", ["help", "start_date=", "end_date=", "query="]
        )
    except getopt.GetoptError as error:
        print(error)
        sys.exit(2)

    h = False
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(help_menu)
            sys.exit(0)
        if opt in ("-s", "--start_date"):
            start_date = arg
        if opt in ("-e", "--end_date"):
            end_date = arg
        if opt in ("-q", "--query"):
            query = arg

    if (
        "start_date" not in locals()
        or "end_date" not in locals()
        or "query" not in locals()
    ):
        print(
            "missing required argument(s). required arguments are "
            "start_date, end_date, and query. exiting..."
        )
        sys.exit(1)

    google_scraper.scrape(start_date, end_date, query)


if __name__ == "__main__":
    main()
