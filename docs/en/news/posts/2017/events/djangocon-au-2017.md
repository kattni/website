---
title: We'll be at DjangoCon AU 2017!
date: 2017-08-04
authors:
- freakboy3742
- glasnt
- hawkowl
categories:
- Events
event:
  name: DjangoCon AU 2017
  url: ''
  date: 2017-08-04
  end_date: 2017-08-04
  description: |-
    DjangoCon AU is annual gathering of Django developers in Australia,
    celebrating it's 5th year in 2017. It is held as a one day specialist
    event at the start of PyCon AU.

    DjangoCon AU content will be Django specific, but there will also be
    useful Django-related content in the main PyCon program.

    There will also be Django developers at the sprints held after PyCon.
involvement:
- type: attending
  team_members:
  - freakboy3742
  - glasnt
  - hawkowl
  date: 2017-08-04
  end_date: 2017-08-04
- type: talk
  team_members:
  - freakboy3742
  title: Red User, Blue User, MyUser, auth.User
  url: ''
  date: 2017-08-04
  end_date: 2017-08-04
  description: |-
    Django's <nospell>contrib.auth</nospell> framework allows to you specify a custom user
    model. Why does this matter? When should you use a custom user model?
    And how do you live with it once you've got one?

    Django's <nospell>contrib.auth</nopell> is a key part of most Django websites. However,
    there are some important details you need to understand if you're going
    to make good use of custom user models. Some of these details are
    technical - for example, custom user models require some special
    consideration when interacting with migrations.

    But even more important are the details about why custom user models are
    important in the first place. Custom User models were necessary to break
    some really common anti-patterns about user identity - anti-patterns
    that are baked into Django's default user model, and are extraordinarily
    common in the wider web development world.

    In this talk, you'll learn about user identity: what it means, and what
    you have to think about when you're developing the user modelling parts
    of your Django project. You'll also learn how to use Django's custom
    user model in practice.
---

{{ generate_event_post(authors, event, involvement, team) }}
