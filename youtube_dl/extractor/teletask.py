from __future__ import unicode_literals

import re
import html
import json

from .common import InfoExtractor
from ..utils import unified_strdate


class TeleTaskIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?tele-task\.de/lecture/video/(?P<id>[0-9]+)'
    _TEST = {
        'url': 'http://www.tele-task.de/lecture/video/9313/',
        'info_dict': {
            'id': '9313',
            'title': 'Dateisysteme',
        },
        'playlist': [{
            'info_dict': {
                'id': '9313-video',
                'ext': 'mp4',
                'title': 'Dateisysteme',
                'upload_date': '20220531',
                'formats': [
                    {
                        'format_id': 'sd',
                    },
                    {
                        'format_id': 'hd',
                    }
                ]
            }
        }, {
            'info_dict': {
                'id': '9313-desktop',
                'ext': 'mp4',
                'title': 'Dateisysteme',
                'upload_date': '20220531',
                'formats': [
                    {
                        'format_id': 'sd',
                    },
                    {
                        'format_id': 'hd',
                    }
                ]
            }
        }]
    }

    def _real_extract(self, url):
        lecture_id = self._match_id(url)
        webpage = self._download_webpage(url, lecture_id)

        title = self._html_search_regex(
            r'<title>([^<]+)</title>', webpage, 'title')
        upload_date = unified_strdate(self._html_search_regex(
            r'Date: ([^<]+) <br>', webpage, 'date', fatal=False))

        player_info = json.loads(html.unescape(self._html_search_regex(
            r'<video-player id=\"player\" configuration=\'([^\']+)\'>', webpage, 'player_info')))

        entry_dict = {}
        for stream_group in player_info["streams"]:
            for stream_type, video_url in stream_group.items():
                content_type, url_type = re.findall(r'\/([^\/]+)\.(mp4|m3u8)$', video_url)[0]
                if content_type not in entry_dict.keys():
                    entry_dict[content_type] = []
                if url_type == 'mp4':
                    entry_dict[content_type].append({
                        'url': video_url,
                        'format_id': stream_type
                    })
        entries = [{
            'id': f'{lecture_id}-{content_type}',
            'title': title,
            'upload_date': upload_date,
            'formats': formats
        } for content_type, formats in entry_dict.items()]

        return self.playlist_result(entries, lecture_id, title)
