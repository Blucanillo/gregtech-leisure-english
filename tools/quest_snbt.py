"""Read FTB Quests' comma-optional SNBT without losing numeric types or layout."""

from __future__ import annotations

import json
import re
from typing import NamedTuple


class Literal(NamedTuple):
    token: str


TOKEN = re.compile(
    r'\s+|//[^\n]*|\#[^\n]*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''
    r'|[{}\[\]:,;]|[^\s{}\[\]:,;]+'
)


class Document:
    def __init__(self, text: str):
        self.text = text
        self.tokens = []
        self.spans = {}
        end = 0
        for match in TOKEN.finditer(text):
            if match.start() != end:
                raise ValueError(f"Unparsed SNBT at character {end}")
            end = match.end()
            value = match.group()
            if not value.isspace() and not value.startswith(("//", "#")):
                self.tokens.append((value, match.start(), match.end()))
        if end != len(text):
            raise ValueError(f"Unparsed SNBT at character {end}")
        self.pos = 0
        self.value = self._value(()) if self.tokens else None
        if self.pos != len(self.tokens):
            raise ValueError("Unexpected trailing SNBT tokens")

    def _take(self, expected=None):
        if self.pos >= len(self.tokens):
            raise ValueError("Unexpected end of SNBT")
        token = self.tokens[self.pos]
        self.pos += 1
        if expected is not None and token[0] != expected:
            raise ValueError(f"Expected {expected!r}, found {token[0]!r}")
        return token

    @staticmethod
    def _string(token):
        if token.startswith('"'):
            return json.loads(token)
        return token[1:-1].replace("\\'", "'").replace("\\\\", "\\")

    def _value(self, path):
        token, start, end = self._take()
        if token == "{":
            result = {}
            while self.pos < len(self.tokens) and self.tokens[self.pos][0] != "}":
                if self.tokens[self.pos][0] == ",":
                    self.pos += 1
                    continue
                key = self._take()[0]
                key = self._string(key) if key.startswith(('"', "'")) else key
                if key in result:
                    raise ValueError(f"Duplicate SNBT key {key!r}")
                self._take(":")
                result[key] = self._value(path + (key,))
            self._take("}")
            return result
        if token == "[":
            result = []
            while self.pos < len(self.tokens) and self.tokens[self.pos][0] != "]":
                if self.tokens[self.pos][0] == ",":
                    self.pos += 1
                    continue
                result.append(self._value(path + (len(result),)))
            self._take("]")
            return result
        if token.startswith(('"', "'")):
            self.spans[path] = (start, end)
            return self._string(token)
        return Literal(token)

    def replace_strings(self, replacements):
        edits = []
        for path, value in replacements.items():
            if not isinstance(value, str):
                raise TypeError("Only text strings can be replaced")
            start, end = self.spans[path]
            edits.append((start, end, json.dumps(value, ensure_ascii=False)))
        text = self.text
        for start, end, value in sorted(edits, reverse=True):
            text = text[:start] + value + text[end:]
        return text


TEXT_FIELDS = {"title", "subtitle", "description"}


def without_display_text(value):
    if isinstance(value, dict):
        return {k: without_display_text(v) for k, v in value.items() if k not in TEXT_FIELDS}
    if isinstance(value, list):
        return [without_display_text(v) for v in value]
    return value


def without_component_text(value):
    if isinstance(value, dict):
        return {k: without_component_text(v) for k, v in value.items() if k != "text"}
    if isinstance(value, list):
        return [without_component_text(v) for v in value]
    return value


def display_fields(value, path=(), scope="root"):
    if isinstance(value, dict):
        scope = value.get("id", scope)
        for key, child in value.items():
            if key in TEXT_FIELDS:
                if isinstance(child, str):
                    yield scope, key, path + (key,), child
                elif isinstance(child, list):
                    for i, text in enumerate(child):
                        if isinstance(text, str):
                            yield scope, key, path + (key, i), text
            elif isinstance(child, (dict, list)):
                yield from display_fields(child, path + (key,), scope)
    elif isinstance(value, list):
        for i, child in enumerate(value):
            yield from display_fields(child, path + (i,), scope)


def lookup(value, path):
    for key in path:
        value = value[key]
    return value
