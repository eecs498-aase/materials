"""Tuning values and the stopword list.

Read-only reference material for most tasks: you need the model to know
COMMON_WORDS exists, but almost no change to this program should edit it.
"""

# How many entries `--top` shows when you do not ask for a number.
DEFAULT_TOP_N = 10

# A speaker line looks like "NAME: said something". Anything before the
# first colon, up to this many characters, counts as a speaker name.
SPEAKER_NAME_MAX_LEN = 40

# Characters stripped from the edges of a word before it is counted.
WORD_EDGE_PUNCTUATION = "\"'`.,;:!?()[]{}<>-—–…*_/\\"

# Words that carry no signal in a meeting transcript. Filtered out of the
# frequency table so the top-N is about the meeting, not about English.
COMMON_WORDS = frozenset(
    {
        "a", "able", "about", "above", "actually", "after", "again",
        "against", "all", "almost", "along", "already", "also", "although",
        "always", "am", "among", "an", "and", "another", "any", "anyone",
        "anything", "are", "around", "as", "at", "back", "basically", "be",
        "because", "been", "before", "being", "below", "between", "both",
        "but", "by", "came", "can", "cannot", "come", "could", "did", "do",
        "does", "doing", "done", "down", "during", "each", "either", "else",
        "enough", "even", "ever", "every", "everyone", "everything",
        "exactly", "few", "for", "from", "further", "get", "gets", "getting",
        "go", "goes", "going", "gone", "good", "got", "great", "had", "has",
        "have", "having", "he", "her", "here", "hers", "herself", "him",
        "himself", "his", "how", "however", "i", "if", "in", "instead",
        "into", "is", "it", "its", "itself", "just", "keep", "kind", "know",
        "known", "let", "like", "little", "look", "lot", "made", "make",
        "makes", "making", "many", "may", "maybe", "me", "mean", "means",
        "might", "mine", "more", "most", "much", "must", "my", "myself",
        "need", "needs", "never", "new", "next", "no", "nor", "not",
        "nothing", "now", "of", "off", "often", "oh", "ok", "okay", "on",
        "once", "one", "only", "onto", "or", "other", "others", "otherwise",
        "ought", "our", "ours", "ourselves", "out", "over", "own", "part",
        "per", "perhaps", "pretty", "probably", "put", "quite", "rather",
        "really", "right", "said", "same", "say", "says", "see", "seem",
        "seems", "seen", "several", "shall", "she", "should", "since", "so",
        "some", "someone", "something", "sometimes", "sort", "still", "such",
        "sure", "take", "takes", "than", "that", "the", "their", "theirs",
        "them", "themselves", "then", "there", "these", "they", "thing",
        "things", "think", "this", "those", "though", "through", "thus",
        "to", "together", "too", "took", "toward", "try", "trying", "two",
        "under", "until", "up", "upon", "us", "use", "used", "uses", "using",
        "very", "want", "wants", "was", "way", "we", "well", "went", "were",
        "what", "when", "where", "whether", "which", "while", "who", "whom",
        "whose", "why", "will", "with", "within", "without", "would", "yeah",
        "yes", "yet", "you", "your", "yours", "yourself", "yourselves",
    }
)

# Filler that shows up in speech and nowhere else. Kept separate from
# COMMON_WORDS so a future --keep-filler flag can put it back.
FILLER_WORDS = frozenset(
    {
        "uh", "um", "er", "ah", "hm", "hmm", "mhm", "huh", "eh", "erm",
        "like", "literally", "honestly", "obviously", "anyway", "anyways",
    }
)

# Everything filtered out of the frequency table.
IGNORED_WORDS = COMMON_WORDS | FILLER_WORDS
