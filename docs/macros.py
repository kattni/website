from textwrap import dedent

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
