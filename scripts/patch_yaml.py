#!/usr/bin/env python3

# Horrible hack to patch YAML while preserving comments and whitespace.
# Has the nice "perk" of working with yaml-string-in-yaml.
#
# In particular, patching key.key2 in the following YAML will work:
#
#   key: |
#       # yaml string in yaml
#       key2: value

import argparse

def patch_yaml(filename, path, value):
    path = path.split('.')

    lines = []
    with open(filename, 'r') as f:
        for line in f:
            stripped = line.lstrip()
            indent = line[:-len(stripped)]
            if path and stripped.startswith(f'{path[0]}:'):
                if len(path) == 1:
                    line = f'{indent}{path[0]}: {value}\n'
                path.pop(0)
            lines.append(line)

    with open(filename, 'w') as f:
        f.write(''.join(lines))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('path')
    parser.add_argument('value')

    args = parser.parse_args()
    patch_yaml(**vars(args))

if __name__ == '__main__':
    main()
