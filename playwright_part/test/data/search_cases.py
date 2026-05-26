# pylint: disable = C0301

"""module for search queries and expected results on different languages"""

SEARCH_CASE = {
    "RU": {
        "query": '"второй по значимости дивизион профессионального футбола в России" википедия',
        "expected": [
            "https://ru.wikipedia.org/wiki/%D0%9F%D0%B5%D1%80%D0%B2%D0%B0%D1%8F_%D0%BB%D0%B8%D0%B3%D0%B0_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8_%D0%BF%D0%BE_%D1%84%D1%83%D1%82%D0%B1%D0%BE%D0%BB%D1%83",
            "https://ru.wikipedia.org/wiki/Первая_лига_России_по_футболу",
        ],
    },
    "EN": {
        "query": '"the second level of the Russian football league system" wikipedia',
        "expected": ["https://en.wikipedia.org/wiki/Russian_First_League"],
    },
    "CN": {
        "query": '"是俄羅斯足球聯賽系統的第二級別" 維基百科',
        "expected": [
            "https://zh.wikipedia.org/wiki/%E4%BF%84%E7%BE%85%E6%96%AF%E7%94%B2%E7%B5%84%E8%B6%B3%E7%90%83%E8%81%AF%E8%B3%BD",
            "https://zh.wikipedia.org/zh-tw/%E4%BF%84%E7%BE%85%E6%96%AF%E7%94%B2%E7%B5%84%E8%B6%B3%E7%90%83%E8%81%AF%E8%B3%BD",
            "https://zh.wikipedia.org/wiki/俄羅斯甲組足球聯賽",
            "https://zh.wikipedia.org/zh-tw/俄羅斯甲組足球聯賽",
        ],
    },
}
