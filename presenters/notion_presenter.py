from notion_client import Client
from config import NOTION_API_KEY, NOTION_DATABASE_ID

notion = Client(auth=NOTION_API_KEY)

def create_notion_page(title, items):
    children = [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "text": [{"type": "text", "text": {"content": title}}]
            }
        }
    ]

    for item in items:
        children.extend([
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "text": [{"type": "text", "text": {"content": item['title']}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "text": [{"type": "text", "text": {"content": item['summary']}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "text": [
                        {
                            "type": "text",
                            "text": {"content": "Source: "},
                        },
                        {
                            "type": "text",
                            "text": {"content": item['source']},
                            "annotations": {"italic": True}
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "text": [
                        {
                            "type": "text",
                            "text": {"content": "Read more: "},
                        },
                        {
                            "type": "text",
                            "text": {"content": item['link']},
                            "href": item['link']
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            }
        ])

    notion.pages.create(
        parent={"database_id": NOTION_DATABASE_ID},
        properties={
            "title": {"title": [{"text": {"content": title}}]},
        },
        children=children
    )