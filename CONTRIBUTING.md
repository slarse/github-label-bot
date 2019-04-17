# Contributing to Labelbot
Labelbot is very much a prototype project right now, and it's uncertain whether
we will continue working on it. It kind of just works for us in its current
state, as far as we need it to. We wouldn't mind accepting a useful PR, though,
especially when it comes to the AWS Lambda documentation and setup procedures.

> **A note on features:** We are quite happy with the current featuers of Labelbot, and
> are mostly looking to improve stability. If you are looking to perform radical
> changes to the functionality, you are probably better of just forking the project
> and doing your own thing!

## Pull request process
* Fork the project.
* _Before_ you start working on something, open a PR with your suggested
  improvement.
  - This is to avoid wasting time on something that will not be accepted.
* If your idea is approved, then you can start work.
* Before pushing finalizing your PR, make sure it passes all of our pre-commit
  hooks.
  - [See the `pre-commit` documentation for details on how to install them](https://pre-commit.com/)
  - Most notably, we format the code with
    [Black](https://github.com/ambv/black), but there are a few other checks as
    well.
* When you are done, tag either `@slarse` or `@jcroona` in a comment on the PR
  saying that it needs looking over!
