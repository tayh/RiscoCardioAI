REGEX_HB_GLIC = r'hemoglobina glicada\s*[<>:=-]?\s*\d+(?:[.,]\d+)?|hemoglobina glicolisada\s*[<>:=-]?\s*\d+(?:[.,]\d+)?|hb glicada\s*[<>:=-]?\s*\d+(?:[.,]\d+)?|hb glicolisada\s*[<>:=-]?\s*\d+(?:[.,]\d+)?|hemoglobina glic\s*[<>:=-]?\s*\d+(?:[.,]\d+)?|hb glic\s*[<>:=-]?\s*\d+(?:[.,]\d+)?|HBA1C\s*[<>:=-]?\s*\d+(?:[.,]\d+)?|hb gli\s*[<>:=-]?\s*\d+(?:[.,]\d+)?|GLICOHG\s*[<>:=-]?\s*\d+(?:[.,]\d+)?|a1c\s*[<>:=-]?\s*\d+(?:[.,]\d+)?'

REGEX_GLUCOSE = r"glicemia\s*[<>:=-]?\s*\d+(?:[.,]\d+)?|glicose\s*[<>:=-]?\s*\d+(?:[.,]\d+)?|glic\s*[<>:=-]?\s*\d+(?:[.,]\d+)?|GJ\s*[<>:=-]?\s*\d+(?:[.,]\d+)?|GJ\s*[<>:=-]?\s*\d+(?:[.,]\d+)?|gli\s*[<>:=-]?\s*\d+(?:[.,]\d+)?"

REGEX_TRIGLIC = r"\b(triglicerideos|trigls|TGL|triglicerides|trigl|triglic|trig)\b\s?(\=?\:?\-?)\s?(\d+\.?,?\d+)"

REGEX_COLESTEROL = (
    r"\b(COL|Colesterol total|colesterol|COL T|CT)\b\s?(\=?\:?\-?)\s?(\d+\.?,?\d+)"
)

REGEX_LDL = r"\b(ldl|ldls)(\*\*)?\;?\s?(\=?\:?\-?)\s?(\d+\.?,?\d+)"

REGEX_HDL = r"\b(hdl|hdls)(\*\*)?\;?\s?(\=?\:?\-?)\s?(\d+\.?,?\d+)"

REGEX_NUMBERS_FLOAT = r'\d+,\d*|\d+\,\d*|\d{2,}|\d+\s*\,\s*\d*|\d{2,}'

REGEX_CLEAN_FLOAT = r'(\d+)\s*,?.?\s*(\d+)'