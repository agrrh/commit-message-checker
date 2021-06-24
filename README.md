# Info

Commit messages checker.

Designed to validate commit messages against some conventional patterns.

# Usage

Runs against git repository located in `/code` directory.

Would stop the process if `[cmc-skip]` substring found in one of commit messages.

## Variables

- `CMC_CONFIG` - path to config file, see examples in `conf/`

- `CMC_COMMIT_A` - commit to start analysis from

- `CMC_COMMIT_B` - final commit to analyze

## Sample run

```bash
docker run --rm -ti \
  -e CMC_CONFIG=/app/conf/default.yml \  # or use "./.cmc.yml" if it's inside repository
  -e CMC_COMMIT_A=abcdef0 \
  -e CMC_COMMIT_B=abcdef1 \
  -v $(pwd):/code \
  agrrh/commit-message-checker
```
