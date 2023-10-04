import json
from google.cloud import vision


def detect_explicit_image_content(path):
    """Detects unsafe features in the file."""

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.safe_search_detection(image=image)
    json_response = json.loads(response.to_json())

    # Get the SafeSearchAnnotation object.
    safe_search_annotation = json_response["responses"][0]["safeSearchAnnotation"]

    # Filter positive annotations
    result = {k: v for k, v in safe_search_annotation.items() if v == 'VERY_LIKELY'}
    return result
