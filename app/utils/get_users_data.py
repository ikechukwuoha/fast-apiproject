from typing import Any, Dict
from bson import ObjectId
from pymongo.collection import Collection






async def get_data_by_identifier(collection: Collection, identifier: str, key: str = "email") -> Dict[str, Any]:
    """
    Fetches data from a MongoDB collection by either ObjectId or a specific key (e.g., email).
    
    Args:
        collection (Collection): The MongoDB collection to query.
        identifier (str): The ObjectId or other unique identifier (e.g., email).
        key (str): The field name to use if the identifier is not an ObjectId (default: 'email').

    Returns:
        Dict[str, Any]: A dictionary containing the document details.
    
    Raises:
        ValueError: If no document is found with the provided identifier.
    """
    # Check if the identifier is a valid ObjectId
    if ObjectId.is_valid(identifier):
        data = await collection.find_one({"_id": ObjectId(identifier)})
    else:
        # Treat it as a unique field (e.g., email, username) if not a valid ObjectId
        data = await collection.find_one({key: identifier})
    
    if data is None:
        raise ValueError(f"Document not found with identifier '{identifier}'.")
    
    # Return the document as-is (or modify as needed)
    return data
