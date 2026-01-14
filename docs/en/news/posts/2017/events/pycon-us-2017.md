---
title: We'll be at PyCon US 2017!
date: 2017-05-17
authors:
- freakboy3742
- glasnt
- swenson
- phildini
- hawkowl
categories:
- Events
event:
  name: PyCon US 2017
  url: https://us.pycon.org/2017/
  date: 2017-05-17
  end_date: 2017-05-22
  description: ''
involvement:
- type: tutorial
  team_members:
  - freakboy3742
  - glasnt
  title: Cross-platform Native GUI development with BeeWare
  url: https://us.pycon.org/2017/
  date: 2017-05-17
  end_date: 2017-05-17
  description: |-
    Have you ever wanted to write a GUI application you can run on your
    laptop? What about an app that you can run on your phone? Historically,
    these have been difficult to achieve with Python, and impossible to
    achieve without learning a different API for each platform. But no more.

    BeeWare is a collection of tools and libraries that allows you to build
    cross-platform native GUI applications in pure Python, targeting
    desktop, mobile and web platforms. In this tutorial, you'll be
    introduced to the BeeWare suite of tools and libraries, and use those
    tools to develop, from scratch, a simple GUI application. You'll then
    deploy that application as a standalone desktop application, a mobile
    phone application, and a single page webapp - without making any changes
    to the application's codebase.
- type: talk
  team_members:
  - freakboy3742
  title: How to write a Python transpiler
  url: https://us.pycon.org/2017/
  date: 2017-05-19
  end_date: 2017-05-19
  description: |-
    We all know Python is a powerful, expressive and accessible programming
    language. What you may *not* know is how much of the internals of Python
    itself is exposed for you to use and manipulate, in the form of APIs
    that are just as powerful, expressive and accessible as Python itself.

    In this talk, you'll be introduced to the tools and libraries Python
    provides to manipulate the compilation and execution of Python code. You
    will also see how you can use those tools to target execution
    environments other than the CPython virtual machine, and, specifically,
    how the BeeWare project uses them in the VOC transpiler to run Python
    code on the Java virtual machine.
- type: booth
  team_members:
  - freakboy3742
  - phildini
  - glasnt
  - swenson
  - hawkowl
  url: https://us.pycon.org/2017/
  date: 2017-05-19
  end_date: 2017-05-19
- type: talk
  team_members:
  - glasnt
  title: Snek in the browser
  url: https://us.pycon.org/2017/
  date: 2017-05-19
  end_date: 2017-05-19
  description: |-
    Python is a decades-strong language with a large community, and it has a
    solid foundation on the server, but it doesn't have a good user story in
    the browser... until now.

    The BeeWare project aims to bring Python natively, everywhere. Using a
    combination of the Batavia and Toga projects, we can develop and
    entirely native web experience in Python, no JavaScript required.

    During this talk, you will learn about how the BeeWare project has built
    Batavia, a Python virtual machine in JavaScript; and Toga, a
    multi-platform native API wrapper; a combination of which can be used to
    build an entire web platform in Python only.
- type: sprint
  team_members:
  - swenson
  - glasnt
  - phildini
  - freakboy3742
  - hawkowl
  url: https://us.pycon.org/2017/
  date: 2017-05-22
  end_date: 2017-05-22
---
{{ generate_event_post(authors, event, involvement, team) }}
