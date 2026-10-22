# QA second-reader brief
You are checking that a quote note's BODY faithfully transcribes its source image. You do NOT edit any file.
Notes live in `D:\Vaults\WisdomCompiler\content\Wisdom Quotes\`; each image is `D:\Vaults\WisdomCompiler\content\Wisdom Quotes\Images\<image_name>` (frontmatter key `image_name`). Read the note, Read the image (webp renders natively), compare.
Pass criteria: every sentence in the body appears in the image with the same words (OCR-artifact fixes and typographic quotes are fine); nothing in the body is absent from the image; for dialogue, each speaker turn is its own paragraph and the questioner's lines are *italic*. A body that deliberately contains only ONE passage from a longer page (quote-only treatment, ShowImage: true) PASSES if that passage is accurate.
Fail examples: invented words, wrong word (e.g. "the" vs "me"), a missing line that is clearly in the image, two speaker turns merged into one paragraph, text from a different page, body says "not legible" but the image is readable.
Report, per note: {"file": "...", "fidelity": "pass|fail|uncertain", "issue": "one line, or null", "severity": "minor|major|null"}
