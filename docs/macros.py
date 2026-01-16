import datetime
from textwrap import dedent
import yaml

def attendees(authors, team):
    if len(authors) == 1:
        return team["authors"][authors[-1]]["short_name"]
    else:
        return ", ".join(team["authors"][author]["short_name"] for author in authors[:-1]) + " and " + team["authors"][authors[-1]]["short_name"]


def talk_title_punctuation(talk_title):
    if talk_title.endswith(("!", "?")):
        return talk_title
    else:
        return f"{talk_title}."


def get_blog_metadata(contents):
    return next(yaml.load_all(contents, Loader=yaml.SafeLoader))


def define_env(env):
    @env.macro
    def fa(*tags):
        tags = " ".join(f"fa-{tag}" for tag in tags)
        return f'<i class="{tags}"></i>'

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
    def upcoming_events(files):
        """Generate upcoming events list for beeware.org homepage sidebar."""
        this_year = datetime.datetime.now().year
        next_year = this_year + 1
        events = []
        for filename, file_data in files.src_uris.items():
            if filename.startswith(tuple(f"news/posts/{year}/events/" for year in [this_year, next_year])):
                metadata = next(yaml.load_all(file_data.content_string, Loader=yaml.SafeLoader))
                if metadata["event"]["date"] < datetime.date.today():
                    if metadata["event"]["date"] == metadata["event"]["end_date"]:
                        event_date = metadata["event"]["date"].strftime("%B %d, %Y")
                    else:
                        event_date = f"{metadata["event"]["date"].strftime("%B %d")}-{metadata["event"]["end_date"].strftime("%d, %Y")}"
                    events.append((metadata["event"]["date"], f"- [{metadata["event"]["name"]}: {event_date}]({file_data.url})"))
        if events:
            return "\n".join(item[1] for item in sorted(events)[:5])
        return "Nothing at the moment..."

    @env.macro
    def latest_news(files):
        """Generate "Latest news" latest blog post link for beeware.org homepage sidebar."""
        this_year = datetime.datetime.now().year
        last_year = this_year - 1
        posts = (
            (get_blog_metadata(file_data.content_string), file_data)
            for filename, file_data in files.src_uris.items()
            if filename.startswith(tuple(f"news/posts/{year}/buzz/" for year in [last_year, this_year]))
        )

        def metadata_date(item):
            metadata, _ = item
            return metadata["date"]

        metadata, file_data = max(posts, key=metadata_date)
        return f"{metadata["date"].strftime("%B %d")}: [{metadata["title"]}]({file_data.url})"
