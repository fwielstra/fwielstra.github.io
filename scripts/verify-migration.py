"""Check that the content migrated from Jekyll to Astro differs from the originals only by
whitelisted markup changes (front matter keys, Liquid tags). Prose must be byte-for-byte equal.

Usage: python3 scripts/verify-migration.py [git ref of the Jekyll version, default: cab6822]
"""
import difflib, pathlib, re, subprocess, sys

ref = sys.argv[1] if len(sys.argv) > 1 else 'cab6822'

def git_ls(path):
    return subprocess.run(['git', 'ls-tree', '--name-only', f'{ref}:{path}'],
                          capture_output=True, text=True, check=True).stdout.split()

def git_show(path):
    return subprocess.run(['git', 'show', f'{ref}:{path}'],
                          capture_output=True, text=True, check=True).stdout

pairs = [(f'_posts/{name}', 'src/content/blog/' + re.sub(r'\.markdown$', '.md', name))
         for name in git_ls('_posts')]
for name in git_ls('pages'):
    target = {'about.md': 'src/pages/about.md', 'portfolio.md': 'src/pages/portfolio/index.md'}
    pairs.append((f'pages/{name}', target.get(name, f'src/pages/portfolio/{name}')))

def allowed(old, new):
    if old is None:
        return False
    if new is None:
        return re.fullmatch(r'(layout|permalink|show_in_nav):.*', old) is not None
    if old == 'layout: page':
        return re.fullmatch(r'layout: (\.\./)+layouts/Page\.astro', new) is not None
    if re.fullmatch(r'\{% highlight \w+ %\}', old):
        return new == '```' + old.split()[2]
    if old == '{% endhighlight %}':
        return new == '```'
    if old.startswith('date:'):
        return new == 'pubDate:' + old[len('date:'):]
    if old.startswith('summary:'):
        return new == 'description:' + old[len('summary:'):]
    return new != old and re.sub(r'\{\{ ?site\.url ?\}\}', '', old) == new

changed = bad = 0
for old_path, new_path in pairs:
    a = git_show(old_path).split('\n')
    b = pathlib.Path(new_path).read_text(encoding='utf-8').split('\n')
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == 'equal':
            continue
        olds, news = a[i1:i2], b[j1:j2]
        if len(olds) == len(news):
            items = list(zip(olds, news))
        else:
            items = [(x, None) for x in olds] + [(None, y) for y in news]
        for old, new in items:
            changed += 1
            if not allowed(old, new):
                bad += 1
                print(f'NOT ALLOWED in {new_path}: {old!r} -> {new!r}')
    print(f'checked {old_path} -> {new_path}')

print(f'{len(pairs)} files, {changed} changed lines, {bad} outside the whitelist')
sys.exit(1 if bad else 0)
