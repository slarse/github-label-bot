# Labelbot
[![Build Status](https://travis-ci.com/slarse/labelbot.svg)](https://travis-ci.com/slarse/labelbot)
[![Documentation Status](https://readthedocs.org/projects/labelbot/badge/?version=latest)](https://labelbot.readthedocs.io/en/latest/?badge=latest)
[![Code Coverage](https://codecov.io/gh/slarse/labelbot/branch/master/graph/badge.svg)](https://codecov.io/gh/slarse/labelbot)
![Supported Python Versions](https://img.shields.io/badge/python-3.6%2C%203.7-blue.svg)
![Supported Platforms](https://img.shields.io/badge/platforms-Linux-blue.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

![Labelbot usage example](images/labeling.gif)

**Labelbot in action:** Setting labels for a visitor with read access.

## Overview
To set a label on an issue, a user needs write access to the repository.
However, it can sometimes be desirable to allow visitors without write access
to set certain pre-defined labels, without the need for manual intervention by
a maintainer. Labelbot is a GitHub bot that allows users to use simple markup
in issue bodies to request certain labels. Labelbot will only set a requested
label if it is present in the `.allowed-labels` file in the root of the
project. This allows maintainers to define a subset of labels that visitors can
set. If the file is not present, Labelbot will do nothing at all.

## Syntax
The markup syntax used in the issue body looks like this:

```
:label:`<REQUESTED_LABEL>`
```

`<REQUESTED_LABEL>` should be replaced with a requested label. For example, if
the requested label is `help`, the markup would look like:

```
:label:`help`
```

As `:label:` is (completely coincidentally) GitHub markup for a label symbol,
this will be rendered quite nicely in the web interface. There are no
restrictions upon where in the issue label markup is placed, or how many
labels are requested. Do however note that you need one `:label:` markup symbol
for each distinct label.

## Example usage
There is an example repo over at
[jcroona/labelbot-demo](https://github.com/jcroona/labelbot-demo) that has a
Labelbot worker installed. At the project root, you will find the following
`.allowed-labels` file:

```
question
feature request
formal complaint
help
```

A visitor can open an issue with a body like this:

```
I can't get Labelbot to work, help!

:label:`help` :label:`formal complaint`
```

Labelbot will then set the labels `help` and `formal complaint` on the issue.
This process is illustrated in the gif at the top of this page.
_[Head over to the repo](https://github.com/jcroona/labelbot-demo) and try it
out yourself if you'd like!_

## Deploying Labelbot
Labelbot is meant to be used with AWS Lambda. Unfortunately, we cannot host a
public instance of Labelbot as we do not have the funds for it. The
[docs](https://labelbot.readthedocs.io) contain instructions for how to deploy
your own instance.
