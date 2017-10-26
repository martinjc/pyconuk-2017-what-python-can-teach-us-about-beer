"""
Beer taxonomy.
"""


import codecs
import functools32
import collections
import numpy as np


@functools32.lru_cache(None)
def load_taxonomy_geo():
    """
    Loads the taxonomy of beer styles. Taxonomy of styles (predominantly) by
    historical geographic origin. "German Lager", etc. This is based on
    BeerAdvocate, Untappd, and Cicerone's categorisation.
    """
    fpath ='./dat_taxonomy/beeradv_with_UT_v2.txt'
    lines = codecs.open(fpath, 'r', 'utf-8').read().split('\n')
    lines = filter(lambda x: x != '', lines)

    tag2styles = {}
    style2tier1 = {}  # top level; e.g., 'ale', 'lager', etc.
    style2tier2 = {}  # fully qualifier level 2; e.g., 'ale-Belgian/FrenchAles'
    style2tier3 = {}  # fully qualifier level 3 / the leaf; e.g., 'ale-Belgian/FrenchAles:Belgian Brown Ale'

    for line in lines:
        if line.startswith('='):
            tag = line.replace('=', '')
            assert '-' in tag
            tag = tag.replace('-', ':')
            tag2styles[tag] = []
        else:
            tag2styles[tag].append(line)
            
            # validate hierarchy
            if line in style2tier2:
                assert style2tier2[line] == tag
                
            # save lookup into hierarchy
            style2tier1[line] = tag.split(':')[0]
            style2tier2[line] = tag
            leaf = line.strip()
            style2tier3[line] = "%s:%s" % (tag, line)
    assert set(style2tier1.keys()) == set(style2tier2.keys())
    #tag2styles, style2tier1, style2tier2, style2tier3 = load_taxonomy()
    #for style in style2tier1.keys():
    #    print "%-30s\n\t%s // %s // %s" % (style, style2tier1[style], style2tier2[style], style2tier3[style])
    return tag2styles, style2tier1, style2tier2, style2tier3


def taxonomy_counts(checkins, beerstyle2cat, bid2beer):
    """
    Aggregate beer checkins `checkins` list to given taxonomy `beerstyle2cat`.
    `beerstyle2cat` is a dictionary mapping an Untappd beer style string
    to a taxonomic category.
    """
    counts = collections.Counter()
    for c in checkins:
        beer = bid2beer[c['beer']]
        bstyle = beer['beer_style']
        cls = beerstyle2cat[bstyle]
        counts[cls] += 1
    return counts


def vectorise_taxonomy_counts(cat_counts, all_categories):
    """
    `all_categories`: List of categories. Vectorisation will follow this
    ordering.
    """
    vec = np.zeros([1, len(all_categories)], dtype=np.float64)
    cat2index = dict(zip(all_categories, xrange(len(all_categories))))
    for cat, cnt in cat_counts.iteritems():
        vec[0, cat2index[cat]] = cnt
    return vec

