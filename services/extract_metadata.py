from models.models import Document, Scope, Source
from services.openai import get_chat_completion
import json
from typing import Dict, List


def extract_metadata_from_document(text: str) -> Dict[str, str]:
    sources = Source.__members__.keys()
    sources_string = ", ".join(sources)
    # This prompt is just an example, change it to fit your use case
    messages = [
        {
            "role": "system",
            "content": f"""
            Given a document from a user, try to extract the following metadata:
            - source: string, one of {sources_string}
            - url: string or don't specify
            - created_at: string or don't specify
            - user_id: string or don't specify

            Respond with a JSON containing the extracted metadata in key value pairs. If you don't find a metadata field, don't specify it.
            """,
        },
        {"role": "user", "content": text},
    ]

    completion = get_chat_completion(
        messages, "gpt-4"
    )  # TODO: change to your preferred model name

    print(f"completion: {completion}")

    try:
        metadata = json.loads(completion)
    except:
        metadata = {}

    return metadata

def validate_meatadata(documents: List[Document]):
    for document in documents:
        metadata = document.metadata
        if metadata is not None:
            scope = metadata.scope
            
            # 如果 scope 为 personal，则检查 user_id 是否为空
            if scope == Scope.personal and (metadata.user_id is None or len(metadata.user_id.strip()) == 0):
                # 如果 user_id 为空，将 scope 调整为 其他最高级
                if(metadata.org_id is not None and len(metadata.org_id.strip()) > 0):
                    metadata.scope = Scope.org
                    print("Warn:", "No user_id provided, set the visibility scope to org for doc: ")
                    print(document.text)
                else:
                    metadata.scope = Scope.public
                    print("Warn:", "No user_id provided, set the visibility scope to public for doc: ")
                    print(document.text)
            
            # 如果 scope 为 org，则检查 org_id 是否为空
            elif scope == Scope.org and (metadata.org_id is None or len(metadata.org_id.strip()) == 0):
                # 如果 org_id 为空，将 scope 调整为 其他最高级
                if(metadata.user_id is not None and len(metadata.user_id.strip()) > 0):
                    metadata.scope = Scope.personal
                    print("Warn:", "No org_id provided, set the visibility scope to personal for doc: ")
                    print(document.text)
                else:
                    # 如果 org_id 为空，将 scope 调整为 public
                    metadata.scope = Scope.public
                    print("Warn:", "No org_id provided, set the visibility scope to public for doc: ")
                    print(document.text)