import logging
import os
import re
import sys
import yaml

from git import Repo, Git

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)8s | %(message)s',
)


def commits_iter(git, repo, commits_range):
    commits_list = git.log(commits_range, '--pretty=format:%H').split('\n')
    # Start scanning from the beginning of PR/commit
    for sha in commits_list:
        commit = repo.commit(sha)
        message = commit.message.strip()

        if '[cmc-skip]' in message:
            logging.info('Found [cmc-skip] flag, skipping the rest')
            break

        yield (sha, message)

        # Supposed to be first commit of current branch
        if sha == commit_b:
            logging.info('Found end of current changeset, stopping')
            break


if __name__ == '__main__':
    logging.critical('Starting ...')

    # Loading params

    config_fname = os.environ.get('CMC_CONFIG') or '/app/conf/default.yml'

    commit_a = os.environ.get('CMC_COMMIT_A')
    commit_b = os.environ.get('CMC_COMMIT_B')

    if not (commit_a and commit_b):
        logging.warning('Doesn\'t look like valid commits range, exiting: {commit_a}...{commit_b}')
        sys.exit(1)

    logging.warning(f'Changeset is {commit_a}...{commit_b}')

    # Loading config
    try:
        with open(config_fname) as fp:
            config = yaml.load(fp, Loader=yaml.BaseLoader)
        logging.info(f'Using config: {config}')
    except Exception as e:
        logging.error(f'Could not load config, exiting\n{e}')
        sys.exit(1)

    git = Git(os.getcwd())
    repo = Repo(os.getcwd())

    # Get commits
    commits_range = f'{commit_a}...{commit_b}'
    if not commits_range.endswith('^'):
        commits_range += '^'

    commits = commits_iter(git, repo, commits_range)

    # Check matches
    success = True
    for sha, message in commits:
        # Pass if at least one of patterns has matched
        matched = [
            bool(re.findall(p, message))
            for p
            in config.get('patterns', [])
        ]
        matched = any(matched)

        first_line = message.split("\n")[0].strip()
        if matched:
            logging.warning(f'✓ {sha[:7]} {first_line}')
        else:
            logging.warning(f'✗ {sha[:7]} {first_line}')

        # Become False if at least one match has failed
        success = success and matched

    logging.critical('Commits checker passed: ' + ('OK' if success else 'FAILED'))

    sys.exit(0 if success else 1)
