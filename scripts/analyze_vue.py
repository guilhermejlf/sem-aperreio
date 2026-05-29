#!/usr/bin/env python3
"""Analisa complexidade dos componentes Vue para migração Options API -> Composition API"""
import pathlib

files = sorted(pathlib.Path('frontend/src').rglob('*.vue'))
rows = []
for f in files:
    content = f.read_text(encoding='utf-8')
    lines = len(content.splitlines())
    has_data = 'data()' in content or 'data ()' in content
    has_methods = 'methods:' in content
    has_computed = 'computed:' in content
    has_watch = 'watch:' in content
    has_mixins = 'mixins:' in content
    has_lifecycle = any(x in content for x in ['mounted()', 'created()', 'beforeUnmount()', 'beforeMount()'])
    refs_count = content.count('$refs')
    emit_count = content.count('$emit')
    toast_count = content.count('$toast')
    router_count = content.count('$router') + content.count('$route')
    score = sum([has_data, has_methods, has_computed, has_watch, has_mixins, has_lifecycle,
                 refs_count > 0, emit_count > 0, toast_count > 0, router_count > 0])
    rows.append((str(f.relative_to('frontend/src')), lines, score,
                 has_data, has_methods, has_computed, has_watch, has_mixins,
                 refs_count, emit_count, toast_count, router_count))

print(f'{"File":<50} {"Lines":>5} {"Score":>5} | data meth comp watch mixins | refs emit toast router')
print('-'*120)
for r in sorted(rows, key=lambda x: (x[2], x[1])):
    path, lines, score, *flags = r
    d, m, c, w, mi, rf, em, to, ro = flags
    ds = 'Y' if d else '.'
    ms = 'Y' if m else '.'
    cs = 'Y' if c else '.'
    ws = 'Y' if w else '.'
    mis = 'Y' if mi else '.'
    print(f'{path:<50} {lines:>5} {score:>5} |  {ds}   {ms}   {cs}   {ws}   {mis}  |  {rf:>3} {em:>3} {to:>4} {ro:>5}')
print(f'Total: {len(rows)} components')
