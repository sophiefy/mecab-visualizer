import fugashi


UNIDIC_KEYS = ['pos1', 'pos2', 'pos3', 'pos4',
               'cType', 'cForm', 'lForm', 'lemma', 'orth', 'pron', 'orthBase', 'pronBase',
               'goshu', 'iType', 'iForm', 'fType', 'fForm', 'iConType', 'fConType',
               'type', 'kana', 'kanaBase', 'form', 'formBase', 'aType', 'aConType', 'aModType',
               'lid', 'lemma_id']


class MecabTagger(object):
    """MeCab Tagger
    """

    def __init__(self):
        """Initialize tagger.
        """

        self.dic_keys = UNIDIC_KEYS
        self.tagger = fugashi.Tagger()

    def parse(self, text: str) -> list:
        """Parse input text into words.

        Args:
            text (str): Text.

        Returns:
            list: Features.
        """

        features_list = self.parse_nbest(text, num=1)

        return features_list[0]

    def parse_nbest(self, text: str, num=1) -> list:
        """Parse input text into words, returning the best N results.

        Args:
            text (str): Text.
            num (int, optional): N. Defaults to 1.

        Returns:
            list: N list of features.
        """

        features_list = []
        results_list = self.tagger.nbestToNodeList(text, num=num)
        for results in results_list:
            # 每个lattice  
            features = []
            for result in results:
                # lattice中的分词结果
                feature = {
                    "surface": result.surface,
                    "word_cost": result.wcost,
                    "cost": result.cost,
                }
                for i, key in enumerate(self.dic_keys):
                    try:
                        feature[key] = result.feature[i]
                    except IndexError:
                        feature[key] = "*"

                features.append(feature)
            features_list.append(features)

        return features_list