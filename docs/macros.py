import datetime
from pathlib import Path
from textwrap import dedent
import yaml

def attendees(authors, team):
    """Generates string identifying attendees of an event, based on whether there is one, or more."""
    if len(authors) == 1:
        return team["authors"][authors[-1]]["short_name"]
    else:
        return ", ".join(team["authors"][author]["short_name"] for author in authors[:-1]) + " and " + team["authors"][authors[-1]]["short_name"]


def talk_title_punctuation(talk_title):
    """Preserves talk title punctuation when talk is provided at the end of a sentence."""
    if talk_title.endswith(("!", "?")):
        return talk_title
    else:
        return f"{talk_title}."


def define_env(env):
    @env.macro
    def fa(*tags):
        """Generates the fontawesome HTML i element."""
        tags = " ".join(f"fa-{tag}" for tag in tags)
        return f'<i class="{tags}"></i>'

    @env.macro
    def generate_resource_post(resource):
        """Generate a resource post from resource template."""
        content = []

        if resource["type"] == "video" and resource["embeddable"]:
            video_url = dedent(f"""\
            <div class="resource-video">
            <iframe class="video" src="{resource["url"]})" frameborder="0" allowfullscreen></iframe>
            </div>
            """)
            content.append(video_url)

        content.append(f"""{resource["description"]}\n""")

        if resource["type"] in ["article"]:
            article_url = dedent(f"""\

            [Read the full article here.]({resource["url"]})

            """)
            content.append(article_url)

        elif resource["type"] == "podcast":
            podcast_url = dedent(f"""\

            [Click here to listen.]({resource["url"]})

            """)
            content.append(podcast_url)

        elif resource["type"] == "video" and not resource["embeddable"]:
            video_url = dedent(f"""\

            As seen at [{resource["event_name"]}]({resource["event_url"]}).

            [View the video here.]({resource["url"]})

            """
            )
            content.append(video_url)

        elif resource["type"] == "video" and resource["embeddable"]:
            content.append(f"\n\nAs seen at [{resource["event_name"]}]({resource["event_url"]}).\n\n")

        content.append("<!-- more -->")

        return "".join(content)

    @env.macro
    def generate_event_post(authors, event, involvement, team):
        """Generate an event post from event template."""
        content = []
        if event.date == event.end_date:
            event_timeframe = f"on {event.date.strftime("%B %d, %Y")}"
        elif event.date != event.end_date:
            event_timeframe = f"from {event.date.strftime('%B %d')} - {event.end_date.strftime("%B %d, %Y")}"

        organizing_introduction = None
        attending_introduction = None
        find_us = None
        for inv in involvement:
            if inv["type"] == "organizing":
                organizing_introduction = dedent(f"""\
                {attendees(authors, team)} will be organizing [{event.name}]({event.url}), which will happen {event_timeframe}!\n\n
                """)
            elif inv["type"] == "attending" or "attending" not in inv["type"]:
                attending_introduction = dedent(f"""\
                {attendees(authors, team)} will be attending [{event.name}]({event.url}) {event_timeframe}!\n\n
                """)
            else:
                find_us = f"You can find us throughout {event.name}:\n\n"

        if organizing_introduction:
            content.append(organizing_introduction)
        if attending_introduction:
            content.append(attending_introduction)
        content.append("\n<!-- more -->\n")
        content.append(f"{event.description}\n\n")
        if find_us:
            content.append(find_us)

        for inv in involvement:
            if inv["type"] == "keynote":
                keynote = dedent(f"""
                - {attendees(inv["team_members"], team)} will be keynoting {event.name}, giving a presentation entitled [{talk_title_punctuation(inv["title"])}]({inv["url"]})
                \n""")
                content.append(keynote)

            if inv["type"] == "talk":
                talk = dedent(f"""
                - {attendees(inv["team_members"], team)} will be giving a talk entitled [{talk_title_punctuation(inv["title"])}]({inv["url"]})
                \n""")
                content.append(talk)

            if inv["type"] == "tutorial":
                tutorial = dedent(f"""
                - {attendees(inv["team_members"], team)} will be hosting a tutorial entitled [{talk_title_punctuation(inv["title"])}]({inv["url"]})
                \n""")
                content.append(tutorial)

            if inv["type"] == "sprint":
                sprint = dedent(f"""
                - {attendees(inv["team_members"], team)} will be hosting a [sprint]({inv["url"]}).
                \n""")
                content.append(sprint)

            if inv["type"] == "booth":
                booth = dedent(f"""
                - {attendees(inv["team_members"], team)} will be hosting a [booth]({inv["url"]}).
                \n""")
                content.append(booth)

        conclusion = "Please come say hello, we'd love to meet you. We're looking forward to seeing you there!"
        content.append(conclusion)

        return "".join(content)

    @env.macro
    def generate_team_page(team, page):
        """Generate the team page from the .authors.yml file metadata."""
        team_page_header = dedent("""\
        So who are the people behind BeeWare? Well, there's a huge group of contributors, but the project is managed by the Bee Team.

        ## Current team members

        """)
        emeritus_team_header = """## Emeritus team members\n"""

        team_member_content = []
        emeritus_team_member_content = []
        for github_id, member_details in team["authors"].items():
            try:
                if member_details["join_date"]:
                    member_title = dedent(f"""\
                    <div class="team-member" markdown="1">
                    <div class="team-bio" markdown="1">

                    ### {member_details["name"]} {{ #{github_id} }}
                    """)

                    member_bio = (Path(page.file.src_dir) / f"about/team/{github_id}.md").read_text()

                    try:
                        mastodon = member_details["mastodon"].split("@")
                        member_image_details_mastodon = f"""<div class="team-mastodon-handle" markdown="1">{fa("mastodon", "lg", "brands")} [{member_details["mastodon"]}](https://{mastodon[2]}/@{mastodon[1]})</div>"""
                    except KeyError:
                        member_image_details_mastodon = ""

                    member_image_details = dedent(
                        f"""\
                    </div>
                    <div class="team-image-details" markdown="1">

                    ![{member_details["name"]}](/{member_details["avatar"]})

                    <div class="team-contact-details" markdown="1">
                    <div class="team-github-handle" markdown="1">{fa("github", "lg", "brands")} [{github_id}](https://github.com/{github_id})</div>
                    {member_image_details_mastodon}
                    <div class="team-email" markdown="1">{fa("envelope", "lg", "solid")} <{member_details['email']}></div>
                    </div>
                    </div>
                    </div>""")

                    team_member = member_title + member_bio + member_image_details

                    if "emeritus_date" in member_details:
                        emeritus_team_member_content.append((member_details["emeritus_date"], team_member))
                    else:
                        team_member_content.append((member_details["join_date"], team_member))
            except KeyError:
                pass

        return team_page_header + "".join(tmc[1] for tmc in sorted(team_member_content)) + emeritus_team_header + "".join(etmc[1] for etmc in sorted(emeritus_team_member_content))

    def get_metadata(contents):
        return next(yaml.load_all(contents, Loader=yaml.SafeLoader))

    @env.macro
    def upcoming_events(files):
        """Generate upcoming events list for beeware.org homepage sidebar."""
        this_year = datetime.datetime.now().year
        next_year = this_year + 1

        events = []
        for filename, file_data in files.src_uris.items():
            if filename.startswith(tuple(f"news/posts/{year}/events/" for year in [this_year, next_year])):
                metadata = get_metadata(file_data.content_string)

                if metadata["event"]["date"] < datetime.date.today():
                    if metadata["event"]["date"] == metadata["event"]["end_date"]:
                        event_date = metadata["event"]["date"].strftime("%B %d, %Y")
                    else:
                        event_date = f"{metadata["event"]["date"].strftime("%B %d")}-{metadata["event"]["end_date"].strftime("%d, %Y")}"

                    events.append((metadata["event"]["date"], f"- [{metadata["event"]["name"]}: {event_date}]({file_data.src_path})"))

        if events:
            return "\n".join(item[1] for item in sorted(events)[:5])
        return "Nothing at the moment..."

    @env.macro
    def latest_news(files):
        """Generate "Latest news" latest blog post link for beeware.org homepage sidebar."""
        this_year = datetime.datetime.now().year
        last_year = this_year - 1

        latest_post = None

        for filename, file_data in files.src_uris.items():
            if filename.startswith(tuple(f"news/posts/{year}/buzz/" for year in [last_year, this_year])):
                metadata = get_metadata(file_data.content_string)

                if latest_post is None or latest_post[0]["date"] < metadata["date"]:
                    latest_post = (metadata, file_data)

        return f"{latest_post[0]["date"].strftime("%B %d")}: [{latest_post[0]["title"]}]({latest_post[1].src_path})"
