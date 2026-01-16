import re
from pathlib import Path
import datetime
from textwrap import dedent
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import yaml


def validate_url(url):
    """
    Validates a URL.

    NOTE: CHECK YOUR ENTRY. There are edge cases where this will pass with an invalid entry.
    """
    try:
        urlopen(Request(url, method="HEAD"))
        return True
    except (URLError, HTTPError, ValueError):
        # If the URL fails to open, fall back to parsing the URL string. This enables
        # verification when an internet connection is unavailable.
        print("URL validation failed.")
        network_connection = input("Are you currently connected to the internet? (y/n): ")
        if network_connection == "y":
            print("Invalid URL.")
            return False
        else:
            parsing_validated = False
            while not parsing_validated:
                parsing_url = urlparse(url)
                if parsing_url.scheme in ["http", "https"] and parsing_url.netloc != "":
                    print("URL is the correct format, however it has not been validated. Verify it on post creation.")
                    return True
                else:
                    print("Invalid URL.")
                    return False


def request_post_type():
    post_type = None
    while post_type is None:
        post_type_entry = input("Choose post type (blog, event, or resource): ") or "blog"
        if post_type_entry in ["blog", "event", "resource"]:
            post_type = post_type_entry
        else:
            print("Invalid post type. Choose between 'blog', 'event', or 'resource'.")
    return post_type


def request_blog_metadata():
    blog_title = input("Blog post title: ")
    blog_authors = input("Post author's GitHub user ID; separate multiple authors with a comma: ")

    date = datetime.date.today()
    return {
        "title": blog_title,
        "date": date,
        "authors": [blog_author.strip() for blog_author in blog_authors.split(",")],
        "categories": ["Buzz"],
    }


def request_event_metadata():
    event_name = input("Event name: ")
    event_url = None
    while event_url is None:
        event_url_entry = input("Event URL: ")
        if validate_url(event_url_entry):
            event_url = event_url_entry
    valid_event_start_date = False
    while not valid_event_start_date:
        try:
            event_start_date_input = input("Event start date (e.g. 2026-05-13): ")
            event_start_date = datetime.datetime.strptime(event_start_date_input, "%Y-%m-%d").date()
            valid_event_start_date = True
        except ValueError:
            print("Invalid date format. Must be YYYY-DD-MM format.")
    valid_event_end_date = False
    while not valid_event_end_date:
        try:
            event_end_date_input = input("Event end date (e.g. 2026-05-19; leave blank if same as event start date): ") or event_start_date_input
            event_end_date = datetime.datetime.strptime(event_end_date_input, "%Y-%m-%d").date()
            valid_event_end_date = True
        except ValueError:
            print("Invalid date format. Must be YYYY-DD-MM format.")
    involvements = []
    authors = set()
    while True:
        involvement_metadata = {}
        involvement_types = {
            "1": "attending",
            "2": "keynote",
            "3": "talk",
            "4": "tutorial",
            "5": "sprint",
            "6": "booth",
            "7": "organizing",
        }
        involvement_type = None
        while involvement_type is None:
            for choice, type_option in involvement_types.items():
                print(f"{choice}: {type_option}")
            choice = input("How is the team involved? Choose a number: ")
            if choice in involvement_types:
                involvement_type = involvement_types[choice]
            else:
                print("Invalid; you must choose a number from the list.")
        involvement_metadata["type"] = involvement_type
        team_members = input("Enter GitHub user ID for all team members involved, separated by comma: ")
        team_member_list = sorted([team_member.strip() for team_member in team_members.split(",")])
        involvement_metadata["team_members"] = team_member_list
        authors.update(team_member_list)
        if involvement_type in ["keynote", "talk", "tutorial"]:
            presentation_title = input("Presentation title: ")
            involvement_metadata["title"] = presentation_title
        if involvement_type in ["keynote", "talk", "tutorial", "sprint", "booth"]:
            involvement_url = None
            while involvement_url is None:
                involvement_url_entry = input(f"{involvement_type} URL (leave blank if unavailable): ") or event_url
                if validate_url(involvement_url_entry):
                    involvement_url = involvement_url_entry
                    involvement_metadata["url"] = involvement_url
        valid_involvement_start_date = False
        while not valid_involvement_start_date:
            try:
                involvement_start_date_input = input(f"Start date of {involvement_type} at {event_name} (e.g. 2026-05-14, leave blank if same as {event_name} start date): ") or event_start_date_input
                involvement_start_date = datetime.datetime.strptime(involvement_start_date_input, "%Y-%m-%d").date()
                valid_involvement_start_date = True
            except ValueError:
                print("Invalid date format. Must be YYYY-DD-MM format.")
        valid_involvement_end_date = False
        while not valid_involvement_end_date:
            try:
                involvement_end_date_input = input(f"End date of {involvement_type} (e.g. 2026-05-19; leave blank if same as {involvement_type} start date): ") or involvement_start_date_input
                involvement_end_date = datetime.datetime.strptime(involvement_end_date_input, "%Y-%m-%d").date()
                valid_involvement_end_date = True
            except ValueError:
                print("Invalid date format. Must be YYYY-DD-MM format.")
        involvement_metadata["date"] = involvement_start_date
        involvement_metadata["end_date"] = involvement_end_date
        if involvement_type in ["keynote", "talk", "tutorial", "sprint", "booth"]:
            # if statement duplicated for the purposes of preserving desired metadata order
            involvement_metadata["description"] = dedent(f"""\
                Remove this content and update with {involvement_type} description.

                Description should begin on the line below 'description: |-' with that line left intact.""")
        involvements.append(involvement_metadata)
        further_involvement = input("Is the team involved in another way? (y/N): ") or "N"
        if further_involvement in ["N", "n", "no"]:
            break

    date = datetime.date.today()
    return {
        "title": f"We'll be at {event_name}!",
        "date": date,
        "authors": sorted(list(authors)),
        "categories": ["Events"],
        "event": {
            "name": event_name,
            "url": event_url,
            "date": event_start_date,
            "end_date": event_end_date,
            "description": dedent(f"""\
                Remove this content and update with event description.

                Description should begin on the line below 'description: |-' with that line left intact.""")
        },
        "involvement": involvements,
    }


def request_resource_metadata():
    resource_types = {
        "1": "video",
        "2": "article",
        "3": "podcast",
    }
    resource_type = None
    while resource_type is None:
        for choice, type_option in resource_types.items():
            print(f"{choice}: {type_option}")
        choice = input("What type of resource are you adding? Choose a number: ")
        if choice in resource_types:
            resource_type = resource_types[choice]
        else:
            print("Invalid; you must choose a number from the list.")
    resource_title = input("Resource title: ")
    resource_url = None
    while resource_url is None:
        resource_url_entry = input("Resource URL: ")
        if validate_url(resource_url_entry):
            resource_url = resource_url_entry
    valid_resource_publication_date = False
    while not valid_resource_publication_date:
        try:
            resource_publication_date_input = input("Resource publication date (e.g. 2026-01-01): ")
            resource_publication_date = datetime.datetime.strptime(resource_publication_date_input, "%Y-%m-%d").date()
            valid_resource_publication_date = True
        except ValueError:
            print("Invalid date format. Must be YYYY-DD-MM format.")
    if resource_type == "video":
        valid_resource_event_date = False
        while not valid_resource_event_date:
            try:
                resource_event_date_input = input("Event end date (e.g. 2026-01-01): ")
                resource_event_date = datetime.datetime.strptime(resource_event_date_input, "%Y-%m-%d").date()
                valid_resource_event_date = True
            except ValueError:
                print("Invalid date format. Must be YYYY-DD-MM format.")
    authors = set()
    resource_authors = input(
        "Enter GitHub user ID for all team members involved, separated by comma: "
    )
    resource_authors_list = sorted(
        [resource_author.strip() for resource_author in resource_authors.split(",")]
    )
    authors.update(resource_authors_list)

    date = datetime.date.today()
    return {
        "title": blog_title,
        "date": date,
        "authors": [blog_author.strip() for blog_author in blog_authors.split(",")],
        "categories": ["Buzz"],
    }


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

    def represent_str(self, data):
        if '\n' in data:
            return self.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')
        return super().represent_str(data)

yaml.add_representer(str, NoAliasDumper.represent_str, Dumper=NoAliasDumper)


def generate_filename(filename_metadata):
    filename = f"{re.sub(r"[^\w ]", "", filename_metadata["title"]).lower().replace(" ", "-")}.md"
    Path(Path(__file__).parent.parent / f"docs/en/news/posts/{filename_metadata["date"].year}/{filename_metadata["categories"][0].lower()}").mkdir(parents=True, exist_ok=True)
    return Path(__file__).parent.parent / f"docs/en/news/posts/{filename_metadata["date"].year}/{filename_metadata["categories"][0].lower()}" / filename


def generate_entry(metadata, payload):
    filename = generate_filename(metadata)

    if filename.is_file():
        print("Post already exists.")
        pass
    else:
        content = yaml.dump(metadata, Dumper=NoAliasDumper, sort_keys=False, width=9999)
        filename.write_text(f"---\n{content}---\n{payload}")
    print(f"File created: {filename}")


if __name__ == "__main__":
    post_type = request_post_type()
    if post_type == "blog":
        metadata = request_blog_metadata()
        payload = dedent("""\
        Add blog post introduction here.

        <!-- more -->

        Add blog post content here.""")
    elif post_type == "event":
        metadata = request_event_metadata()
        payload = "{{ generate_event_post(authors, event, involvement, team) }}"
    else:
        raise Exception(f"Post type '{post_type}' not supported.")
    generate_entry(metadata, payload)
