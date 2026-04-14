"""
File classifier based on extension and keyword matching.
"""

import os
import mimetypes
from typing import Dict, Any


class IPIPQClassifier:
    """
    File classification engine based on extension and keywords.
    """

    # File type mapping
    FILE_TYPE_MAP = {
        # Images
        "image": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".heic", ".tiff"],
        # Documents
        "document": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".pages"],
        # Spreadsheets
        "spreadsheet": [".xls", ".xlsx", ".csv", ".numbers", ".ods"],
        # Presentations
        "presentation": [".ppt", ".pptx", ".key"],
        # Code
        "code": [".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rs", ".c", ".cpp", ".h", ".sh", ".rb", ".php"],
        # Video
        "video": [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm"],
        # Audio
        "audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
        # Archives
        "archive": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
        # Medical (keyword-driven)
        "medical": ["medical", "health", "diagnosis", "prescription", "patient", "record"],
        # Business (keyword-driven)
        "business": ["contract", "order", "invoice", "client", "meeting", "proposal"],
        # Personal
        "personal": ["personal", "private", "family", "home"],
        # Project
        "project": ["project", "code", "git", "development", "plan", "milestone"],
        # Research
        "research": ["study", "course", "notes", "lecture", "paper", "thesis"],
        # Decision
        "decision": ["decision", "choice", "option", "analysis", "evaluation"],
        # Review
        "review": ["review", "reflection", "summary", "lessons", "experience"],
    }

    @classmethod
    def classify_file(cls, filepath: str) -> Dict[str, Any]:
        """
        Classify a file based on filename keywords and extension.
        Returns dual output (JSON + Markdown).
        """
        filename = os.path.basename(filepath)
        ext = os.path.splitext(filename)[1].lower()
        mime_type = mimetypes.guess_type(filepath)[0] or "unknown"

        # Keyword matching (higher priority than extension)
        # Skip items starting with "." (those are extensions, handled below)
        for category, keywords in cls.FILE_TYPE_MAP.items():
            text_keywords = [kw for kw in keywords if not kw.startswith(".")]
            if any(kw.lower() in filename.lower() for kw in text_keywords):
                target_dir = cls._get_target_dir(category)
                return {
                    "json": {
                        "source": filepath,
                        "filename": filename,
                        "category": category,
                        "target_dir": target_dir,
                        "confidence": 0.95,
                        "matched_by": "keyword",
                    },
                    "markdown": f"**{filename}** → `{target_dir}` (keyword match)",
                }

        # Extension matching
        for category, exts in cls.FILE_TYPE_MAP.items():
            if ext in exts:
                target_dir = cls._get_target_dir(category)
                return {
                    "json": {
                        "source": filepath,
                        "filename": filename,
                        "category": category,
                        "target_dir": target_dir,
                        "confidence": 0.8,
                        "matched_by": "extension",
                    },
                    "markdown": f"**{filename}** → `{target_dir}` (extension match)",
                }

        # Uncategorized
        return {
            "json": {
                "source": filepath,
                "filename": filename,
                "category": "uncategorized",
                "target_dir": "DATA/UNCATEGORIZED/",
                "confidence": 0.3,
                "matched_by": "none",
            },
            "markdown": f"**{filename}** → `DATA/UNCATEGORIZED/` (uncategorized)",
        }

    @staticmethod
    def _get_target_dir(category: str) -> str:
        """Map category to target directory"""
        mapping = {
            "image": "MEDIA/Images/",
            "document": "DOCS/Documents/",
            "spreadsheet": "DOCS/Spreadsheets/",
            "presentation": "DOCS/Presentations/",
            "code": "CODE/",
            "video": "MEDIA/Videos/",
            "audio": "MEDIA/Audio/",
            "archive": "DATA/Archives/",
            "medical": "DATA/Medical/",
            "business": "WORK/Business/",
            "personal": "LIFE/Personal/",
            "project": "WORK/Projects/",
            "research": "KNOWLEDGE/Research/",
            "decision": "KNOWLEDGE/Decisions/",
            "review": "KNOWLEDGE/Reviews/",
            "uncategorized": "DATA/UNCATEGORIZED/",
        }
        return mapping.get(category, "DATA/UNCATEGORIZED/")