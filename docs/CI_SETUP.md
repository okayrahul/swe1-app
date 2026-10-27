# CI account setup and assignment verification

The configuration files cannot activate external accounts on their own. Complete
these settings once, then verify the running pipeline.

## 1. Travis CI

Sign in at https://app.travis-ci.com/ with GitHub and enable
`okayrahul/swe1-app`. In repository settings, enable builds for both pushes and
pull requests. Do not allow deployment secrets in fork pull request builds.

In Travis repository settings, add the following environment variables with
**Display value in build log** disabled:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

Use an IAM deployment identity authorized for the existing Elastic Beanstalk
application and its S3 upload bucket. Do not use root account credentials or put
keys in GitHub files. Replace any previously exposed credentials before use.

The configured destination is:

- Region: `us-east-1`
- Application: `rahul-swe1-app`
- Environment: `rahul-swe1-app-env`
- S3 bucket: `elasticbeanstalk-us-east-1-174135522077`

Confirm these still match the existing AWS environment before the first build.

## 2. Coveralls

Sign in at https://coveralls.io/ with GitHub and enable `okayrahul/swe1-app`.
The Coveralls client recognizes Travis build metadata automatically. If the
repository needs a token, add `COVERALLS_REPO_TOKEN` in Travis repository settings,
with its value hidden from logs. Never commit the token.

## 3. Require passing status checks

After Travis has run at least once, open:

https://github.com/okayrahul/swe1-app/settings/branches

Add or update a protection rule for `main`:

- Enable **Require status checks to pass before merging**.
- Select the actual Travis pull request check shown by GitHub, commonly
  `Travis CI - Pull Request` or `continuous-integration/travis-ci/pr`.
- Do not require the push-only check on pull requests.

Use the check name reported by the real first build rather than guessing it.

## 4. Verify the Definition of Done

1. Push a branch containing the CI setup and open a pull request against `main`.
2. Confirm that a Travis pull request build starts and checks pass.
3. On a temporary branch, introduce a formatting or lint violation. Confirm its
   PR build fails. Remove the violation and confirm the next build passes.
4. Confirm that Coveralls displays the uploaded coverage report and README badge.
5. Merge the passing setup PR. Confirm the successful `main` build deploys to EB.
6. Open `/polls/`, submit a vote, and confirm results load on the deployed app.
7. Confirm branch protection prevents merging a PR with a failed required check.

## Submission

- Travis: https://app.travis-ci.com/github/okayrahul/swe1-app
- Application: http://rahul-swe1-app-env.eba-2syr3zrb.us-east-1.elasticbeanstalk.com/polls/
- Repository: https://github.com/okayrahul/swe1-app

The deployment uses the existing single-instance SQLite configuration. Its data
is local to the instance and can be reset during redeployment or replacement.
