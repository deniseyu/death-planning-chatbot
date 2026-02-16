import json
from unittest.mock import patch, MagicMock
from app.documents import render_advance_directive
from app.chat import extract_structured_data

SAMPLE_DATA = {
    "full_name": "Jane Doe",
    "date_of_birth": "1955-03-12",
    "healthcare_wishes": {
        "resuscitation": "Do not resuscitate",
        "life_support": "No mechanical ventilation",
        "feeding_tubes": "No artificial nutrition",
        "organ_donation": "Yes, all organs and tissues",
    },
    "funeral_preferences": {
        "method": "Cremation",
        "service_type": "Small memorial gathering",
        "specific_wishes": "Play 'What a Wonderful World' by Louis Armstrong",
    },
    "messages_for_loved_ones": [
        {"recipient": "My daughter Sarah", "message": "I am so proud of you."},
        {"recipient": "My friend Tom", "message": "Thank you for everything."},
    ],
    "asset_notes": "Life insurance policy with Acme Corp, policy #12345. Safe deposit box at First National Bank.",
}


def test_render_advance_directive_contains_name():
    md = render_advance_directive(SAMPLE_DATA)
    assert "Jane Doe" in md


def test_render_advance_directive_contains_healthcare_wishes():
    md = render_advance_directive(SAMPLE_DATA)
    assert "Do not resuscitate" in md
    assert "No mechanical ventilation" in md
    assert "all organs and tissues" in md


def test_render_advance_directive_contains_funeral_preferences():
    md = render_advance_directive(SAMPLE_DATA)
    assert "Cremation" in md
    assert "Small memorial gathering" in md
    assert "Wonderful World" in md


def test_render_advance_directive_contains_messages():
    md = render_advance_directive(SAMPLE_DATA)
    assert "My daughter Sarah" in md
    assert "I am so proud of you." in md
    assert "My friend Tom" in md


def test_render_advance_directive_contains_asset_notes():
    md = render_advance_directive(SAMPLE_DATA)
    assert "Life insurance policy" in md
    assert "Safe deposit box" in md


def test_render_advance_directive_contains_disclaimer():
    md = render_advance_directive(SAMPLE_DATA)
    assert "not a legal document" in md.lower() or "not** a legal document" in md


def test_render_with_missing_data():
    minimal = {
        "full_name": None,
        "date_of_birth": None,
        "healthcare_wishes": {
            "resuscitation": None,
            "life_support": None,
            "feeding_tubes": None,
            "organ_donation": None,
        },
        "funeral_preferences": {
            "method": None,
            "service_type": None,
            "specific_wishes": None,
        },
        "messages_for_loved_ones": [],
        "asset_notes": None,
    }
    md = render_advance_directive(minimal)
    assert "Not provided" in md
    assert "Not discussed" in md
    assert "No messages recorded" in md


def test_extract_structured_data_parses_json():
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=json.dumps(SAMPLE_DATA))]

    with patch("app.chat.sessions", {"test-session": [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"},
    ]}):
        with patch("app.chat.client") as mock_client:
            mock_client.messages.create.return_value = mock_response
            result = extract_structured_data("test-session")

    assert result["full_name"] == "Jane Doe"
    assert result["healthcare_wishes"]["resuscitation"] == "Do not resuscitate"
    assert len(result["messages_for_loved_ones"]) == 2
