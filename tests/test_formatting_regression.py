"""
test_formatting_regression.py
Regression tests for formatting_checks.check_formatting_elements_type2.

Purpose: guard against task_description (TD) marker detection and
autoformatting (bullet) detection breaking silently after future edits.

Two concerns tested separately, as they are independent checks in the
source function:
- TD detection: substring match of a pedagogical marker.
- Autoformatting detection: whole-text scan for line-start bullet characters.

Note: the text used in each case is not meant to resemble a realistic
student answer. It contains only the minimum needed to exercise the one
flag under test (marker present/absent, bullet lines present/absent),
so that changes to real task descriptions or model solutions never
require editing this file.
"""

from config.formatting_checks import check_formatting_elements_type2


CW8_4_MARKERS = ["please calculate"]


# --- TD detection cases ---

CW8_4_CASE_TD_PRESENT = "please calculate"
CW8_4_CASE_TD_ABSENT = "no marker here"


def test_cw8_4_td_marker_present():
    result = check_formatting_elements_type2(CW8_4_CASE_TD_PRESENT, CW8_4_MARKERS)
    assert result["elements_found"]["task_description"] is True


def test_cw8_4_td_marker_absent():
    result = check_formatting_elements_type2(CW8_4_CASE_TD_ABSENT, CW8_4_MARKERS)
    assert result["elements_found"]["task_description"] is False


# --- Autoformatting detection cases ---

AUTOFORMAT_CASE_NO_BULLETS = """This is a plain sentence.

This is another plain sentence with no list markers at all."""

AUTOFORMAT_CASE_WITH_DASH_BULLETS = """This is a plain sentence.

- first item
- second item"""

AUTOFORMAT_CASE_WITH_BULLET_CHAR = """This is a plain sentence.

- first item
- second item"""

AUTOFORMAT_CASE_WITH_ASTERISK_BULLETS = """This is a plain sentence.

* first item
* second item"""


def test_cw8_4_autoformat_no_bullets():
    result = check_formatting_elements_type2(AUTOFORMAT_CASE_NO_BULLETS, CW8_4_MARKERS)
    assert result["elements_found"]["autoformatting"] is True


def test_cw8_4_autoformat_dash_bullets():
    result = check_formatting_elements_type2(AUTOFORMAT_CASE_WITH_DASH_BULLETS, CW8_4_MARKERS)
    assert result["elements_found"]["autoformatting"] is False


def test_cw8_4_autoformat_bullet_char():
    result = check_formatting_elements_type2(AUTOFORMAT_CASE_WITH_BULLET_CHAR, CW8_4_MARKERS)
    assert result["elements_found"]["autoformatting"] is False


def test_cw8_4_autoformat_asterisk_bullets():
    result = check_formatting_elements_type2(AUTOFORMAT_CASE_WITH_ASTERISK_BULLETS, CW8_4_MARKERS)
    assert result["elements_found"]["autoformatting"] is False
