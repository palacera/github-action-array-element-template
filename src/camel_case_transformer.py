import re

from src.string_utilities import separate_words, replace_word_delimiters


class CamelCaseTransformer:

    @staticmethod
    def _to_camel_case(segment, is_lower=True):
        words = segment.strip().lower().split()
        if not words:
            return ""

        camel_case_segment = (words[0] +
                              ''.join(x.capitalize() for x in words[1:]))
        if not is_lower:
            camel_case_segment = (camel_case_segment[0].upper() +
                                  camel_case_segment[1:])
        return camel_case_segment

    @staticmethod
    def transform(s, is_lower=True):

        s = separate_words(s, ' ')
        s = replace_word_delimiters(s, ' ')

        delimiter_search = re.findall(r"[^a-zA-Z0-9\s]+", s)
        delimiter = ''

        if delimiter_search:
            delimiter = delimiter_search[0]
            segments = s.split(delimiter)
        else:
            segments = [s]

        transformed_segments = \
            [CamelCaseTransformer._to_camel_case(segment, is_lower)
             for segment in segments]

        return delimiter.join(transformed_segments) \
            if delimiter_search else transformed_segments[0]

    @staticmethod
    def lower(s):
        return CamelCaseTransformer.transform(s, is_lower=True)

    @staticmethod
    def upper(s):
        return CamelCaseTransformer.transform(s, is_lower=False)
