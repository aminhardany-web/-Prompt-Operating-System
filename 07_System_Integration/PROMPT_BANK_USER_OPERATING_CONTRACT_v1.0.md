# Prompt Bank — User Operating Contract v1.0

Status: PROPOSED / CONTROLLED
Purpose: make Prompt Bank usable as a simple application from natural-language requests without requiring the user to know PB-IDs, registries, hashes, folders or lifecycle terminology.

## 1. Retrieval is intent-first
The user does not need to know a prompt ID.

Examples:
- «بهترین پرامپت برای استخراج و جمع‌بندی پروژه را بده.»
- «همه پرامپت‌های شورا را پیدا کن.»
- «پرامپت‌های مشابه این را پیدا کن و بهترین نسخه را بده.»
- «این پرامپت را ممیزی کن.»
- «نسخه بهتر این پرامپت را پیدا کن.»
- «یادداشت‌های مربوط به این موضوع را هم کنار Promptها بیاور.»

The runtime must resolve intent, search canonical source records and controlled candidates, rank by semantic job/goal, and return the full usable prompt text. IDs and provenance are secondary metadata, not a prerequisite for use.

## 2. New Prompt intake is automatic by default
When a user supplies a structured prompt, the runtime should automatically perform:

DETECT → CAPTURE EXACT SOURCE → HASH → PROVENANCE → EXACT DUPLICATE CHECK → STRUCTURAL CLASSIFICATION → NEAR-DUPLICATE / SAME-JOB CHECK → CANONICAL OR CANDIDATE DECISION → QUEUE VALIDATION → INDEX

The user should not have to separately say «ثبت کن»، «شناسنامه بده»، «ایندکس کن» or «آرشیو کن» after supplying a prompt when the active context is Prompt Bank.

## 3. Prompt and Note are different record types
A Prompt is executable instruction text. A Note is knowledge, observation, decision, source, requirement, idea or project memory. They may be cross-linked but must not be silently converted into one another.

Note intake:
CAPTURE → SOURCE/DATE → PROJECT/TOPIC → CLASSIFY → LINK → INDEX → RETRIEVE

## 4. Similarity handling
The runtime must distinguish:
- exact duplicate;
- near duplicate;
- same-job variant;
- refinement;
- specialization;
- complementary prompt;
- conflict;
- unrelated.

Similarity alone never authorizes merging. SOURCE_CANONICAL is immutable.

## 5. Quality handling
A prompt may be retrieved even when not validated, but its status must be visible. The runtime must never represent NOT_TESTED or NOT_VALIDATED as VERIFIED or RELEASED.

Quality comparison should consider, where relevant:
clarity, task/success criteria, scope/right-sizing, context boundaries, output contract, examples, positive instructions, uncertainty/error handling, reuse, and regression evidence.

## 6. Best-version behavior
When several prompts solve substantially the same job, return:
1. best currently supported option;
2. alternatives when materially different;
3. source status;
4. short reason for ranking.

If no evidence supports a «better» claim, say so.

## 7. Source preservation
Historical prompt text must never be overwritten, silently normalized, summarized in place, or merged into another source. Optimized prompts belong in DERIVED_OPTIMIZED with parent linkage.

## 8. ChatGPT host boundary
This contract does not claim native automatic access to every hidden ChatGPT conversation, Project, Canvas, Notebook or archive page. Automatic behavior is only valid where the host environment exposes the relevant connected resource/tool/context. ChatGPT native search remains a user-facing discovery path; the Prompt Bank runtime may use accessible archive/index/library resources.

## 9. Default user experience
The user should be able to say one natural sentence describing the desired result. The system handles retrieval, comparison and status internally and returns the prompt itself first.

Example:
«یک پرامپت برای استخراج و جمع‌بندی کامل یک پروژه می‌خواهم که هیچ تصمیم، فایل، اقدام، وابستگی و کار ناتمامی جا نماند.»

Expected behavior:
- search canonical and controlled candidate corpus;
- identify same-job families;
- select the strongest supported source/variant;
- return the complete prompt text;
- show status and provenance briefly;
- offer optimized/tested variant only when evidence exists.

## 10. Release boundary
This contract improves user interaction and retrieval semantics. It does not by itself authorize production release of the 530 canonical records. Semantic validation, runtime evaluation and regression remain independent release gates.
