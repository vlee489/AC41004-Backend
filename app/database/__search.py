"""Handles Searching"""
from __future__ import annotations
from typing import TYPE_CHECKING, List, Union, Optional

if TYPE_CHECKING:
    from .__init__ import DBConnector
from bson import ObjectId
from bson.errors import InvalidId

from app.database.models import SearchResource


async def search_account_id_resources(self: 'DBConnector', query: str, account_id: Union[ObjectId, str]) ->\
        List[SearchResource]:
    try:
        # If ID is a string turn it into an ObjectID
        if type(account_id) is str:
            account_id = ObjectId(account_id)
        return_list = []
        search_cursor = self._db.resources.aggregate([
            {
                '$search': {
                    'index': 'resourceSearch',
                    'text': {
                        'query': query,
                        'path': [
                            'name', 'reference', 'metadata.Tags.Value', 'metadata.name'
                        ]
                    }
                }
            }, {
                '$match': {
                    'account_id': account_id
                }
            }, {
                '$project': {
                    'score': {
                        '$meta': 'searchScore'
                    },
                    '_id': 1,
                    'name': 1,
                    'reference': 1,
                    'last_updated': 1
                }
            }, {
                '$sort': {
                    'score': -1
                }
            }
        ])
        async for search in search_cursor:
            return_list.append(SearchResource(search))
        return return_list
    except InvalidId:
        return []
