# -*- coding: utf-8 -*-
import re
from nltk.tokenize import punkt

class Language(punkt.PunktLanguageVars):
    """Used to realign punctuation that should be included in a sentence
    although it follows the period (or ?, !)."""
    re_boundary_realignment = re.compile(u'["“”\')\]}]+?(?:\s+|(?=--)|$)', re.MULTILINE | re.UNICODE)

    """Excludes some characters from starting word tokens"""
    _re_word_start    = u"[^\(\"“”\`{\[:;&\#\*@\)}\]\-,]"

    """Characters that cannot appear within words"""
    _re_non_word_chars   = u"(?:[?!)\"“”;}\]\*:@\'\({\[])"

class SentenceTokenizer(punkt.PunktSentenceTokenizer):
    """ Extend the nltk's punkt sentence tokenizer """
    _re_abbr = re.compile(r'((?:[\w]\.)+[\w]*\.)', re.UNICODE)

    def __init__(self, lang_vars=None, *args, **kwargs):
        if lang_vars is None:
            lang_vars = Language()
        punkt.PunktSentenceTokenizer.__init__(self, lang_vars=lang_vars, *args, **kwargs)

    def _annotate_tokens(self, tokens):
        """ Given a set of tokens augmented with markers for line-start and
        paragraph-start, returns an iterator through those tokens with full
        annotation including predicted sentence breaks. """
        # Make a preliminary pass through the document, marking likely
        # sentence breaks, abbreviations, and ellipsis tokens.
        tokens = self._annotate_first_pass(tokens)

        # Make a second pass through the document, using token context
        # information to change our preliminary decisions about where
        # sentence breaks, abbreviations, and ellipsis occurs.
        tokens = self._annotate_second_pass(tokens)

        tokens = self.annotate_multi_punct_words(tokens)

        return tokens

    def annotate_multi_punct_words(self, tokens):
        """ Detect abbreviations with multiple periods and mark them as abbreviations.
        Basically punkt is failing to count custom abbreviations, like F.B.I.,
        when it is not in the training data, even though they are relatively simple
        to tease out, especially when mixing it with ortho heuristics to detect
        the likelyhood of it being a sentence starter as well an abbreviation."""
        for aug_tok1, aug_tok2 in punkt._pair_iter(tokens):
            if self._re_abbr.search(aug_tok1.tok) is None:
                yield aug_tok1
                continue

            aug_tok1.abbr = True
            aug_tok1.sentbreak = False
            # Is it the last token? We can't do anything then.
            if not aug_tok2:
                continue

            next_typ = aug_tok2.type_no_sentperiod
            tok_is_initial = aug_tok1.is_initial
            # figure out if it's a sentence starter
            # [4.2. Token-Based Reclassification of Abbreviations] If
            # the token is an abbreviation or an ellipsis, then decide
            # whether we should *also* classify it as a sentbreak.
            if (aug_tok1.abbr or aug_tok1.ellipsis) and not tok_is_initial:
                # [4.1.1. Orthographic Heuristic] Check if there's
                # orthogrpahic evidence about whether the next word
                # starts a sentence or not.
                is_sent_starter = self._ortho_heuristic(aug_tok2)
                if is_sent_starter == True:
                    aug_tok1.sentbreak = True
                    yield aug_tok1
                    continue

            # [4.1.3. Frequent Sentence Starter Heruistic] If the
            # next word is capitalized, and is a member of the
            # frequent-sentence-starters list, then label tok as a
            # sentence break.
            if aug_tok2.first_upper and next_typ in self._params.sent_starters:
                aug_tok1.sentbreak = True

            yield aug_tok1

