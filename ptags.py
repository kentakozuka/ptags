#! /usr/bin/env python

# ptags
#
# Create a tags file for Python programs, usable with vi.
# Tagged are:
# - functions (even inside other defs or classes)
# - classes
# - filenames
# Warns about files it cannot open.
# No warnings about duplicate tags.


######################################
# TODO: 変数の定義元も記録するように修正する
######################################
import sys, re, os

tags = []    # Modified global variable!

def main():
    #args = sys.argv[1:]
    #for filename in args:
    #    treat_file(filename)
    xdir = os.walk(sys.argv[1])
    for xpath, dirs, files in xdir:
        for xfile in files:
            fname, ext = os.path.splitext(xfile)
            if '.py' == ext:
               filename = os.path.join(xpath, xfile)
               treat_file(filename)
    if tags:
        fp = open('tags', 'w')
        tags.sort()
        for s in tags: fp.write(s)


expr = '^[ \t]*(def|class)[ \t]+([a-zA-Z0-9_]+)[ \t]*[:\(]'
matcher = re.compile(expr)

def treat_file(filename):
    try:
        fp = open(filename, 'r')
    except:
        sys.stderr.write('Cannot open %s\n' % filename)
        return
    base = os.path.basename(filename)
    if base[-3:] == '.py':
        base = base[:-3]
    s = base + '\t' + filename + '\t' + '1\n'
    tags.append(s)
    while 1:
        line = fp.readline()
        if not line:
            break
        m = matcher.match(line)
        if m:
            content = m.group(0)
            name = m.group(2)
            s = name + '\t' + filename + '\t/^' + content + '/\n'
            tags.append(s)

if __name__ == '__main__':
    main()
