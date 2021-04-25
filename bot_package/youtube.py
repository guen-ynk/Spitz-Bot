import json
import urllib.parse

import requests


class YoutubeSearch:
    def __init__(self, search_terms: str, max_results=5):
        self.search_terms = search_terms
        self.max_results = max_results
        self.videos = self._search()

    def _search(self):
        encoded_search = urllib.parse.quote_plus(self.search_terms)
        url = f"https://youtube.com/results?search_query={encoded_search}"
        response = requests.get(url).text
        while "ytInitialData" not in response:
            response = requests.get(url).text
        results = self._parse_html(response)
        return results

    def _parse_html(self, response):
        results = []
        start = (
                response.index("ytInitialData")
                + len("ytInitialData")
                + 3
        )
        end = response.index("};", start) + 1
        json_str = response[start:end]
        data = json.loads(json_str)

        videos = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
            "sectionListRenderer"
        ]["contents"][0]["itemSectionRenderer"]["contents"]

        for video in videos[: max(len(results), self.max_results)]:
            res = {}
            if "videoRenderer" in video.keys():
                video_data = video.get("videoRenderer", {})
                res["url"] = "https://www.youtube.com/watch?v=" + str(video_data.get("videoId", None))
                res["title"] = video_data.get("title", {}).get("runs", [[{}]])[0].get("text", None)
                results.append(res)
        return results
