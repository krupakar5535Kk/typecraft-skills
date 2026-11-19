# TYPECRAFT SKILLS

# Resource Schema v1.2

**Document ID:** TCS-RS-001
**Status:** Proposed
**Version:** 1.2
**Supersedes:** Resource Schema v1.1

---

## 1. Purpose

This document defines the canonical resource contract for TypeCraft Skills.

It establishes how typography styles and design templates are:

  - Identified.
  - Documented.
  - Stored.
  - Versioned.
  - Related.
  - Retrieved.
  - Validated.
  - Reviewed and approved.

The resource system uses YAML frontmatter for structured metadata and Markdown for detailed creative knowledge.

The schema must support machine validation, progressive disclosure, extensibility and consistent AI interpretation.

## 2. Resource Architecture

TypeCraft initially defines two primary resource types.

### 2.1 Typography Style

A typography style defines the visual identity and treatment of text.

Its responsibilities include:

  - Typeface direction.
  - Letterform characteristics.
  - Font weight and spacing.
  - Color and visual effects.
  - Typography hierarchy.
  - Composition guidance.
  - Domain-specific applications.

### 2.2 Design Template

A design template defines the composition and arrangement of content.

Its responsibilities include:

  - Layout structure.
  - Text positioning.
  - Content hierarchy.
  - Alignment and spacing.
  - Image and visual placement.
  - Canvas and aspect-ratio adaptation.
  - Customization boundaries.

A typography style and a design template are independent resources.

Neither resource type should absorb the responsibilities of the other.

## 3. Canonical Repository Locations

Typography styles:

skills/typecraft-skills/references/design-styles/

Design templates:

skills/typecraft-skills/references/design-templates/

Each resource must have its own Markdown file.

Example:

skills/typecraft-skills/references/design-styles/example-style.md

skills/typecraft-skills/references/design-templates/example-template.md

### 3.1 Filename Rules

Filenames must:

  - Use lowercase letters.
  - Use hyphens between words.
  - Use the .md extension.
  - Avoid spaces.
  - Avoid special characters.
  - Represent the resource name clearly.
  - Be unique within their resource directory.

Recommended filename pattern:

lowercase-hyphen-separated-name.md

A resource filename may change during a reviewed rename, but its resource ID must remain stable.

## 4. Canonical YAML Frontmatter

Every resource file must begin with YAML frontmatter.

The opening delimiter must be the first line of the file.

The closing delimiter must appear before the Markdown content.

There must be no blank lines or other content before the opening delimiter.

### 4.1 Mandatory Fields

| Field | YAML Type | Requirement |
|---|---|---|
| id | String | Unique permanent identifier |
| name | String | Non-empty resource name |
| resource_type | String | Controlled resource type |
| schema_version | String | Metadata schema version |
| resource_version | String | Semantic resource version |
| status | String | Controlled lifecycle status |
| summary | String | Concise resource description |
| domains | Array of strings | At least one valid domain |
| tags | Array of strings | At least one unique keyword |

### 4.2 Optional Fields

| Field | YAML Type | Purpose |
|---|---|---|
| related_resources | Array of strings | References to other resource IDs |
| category | String | More specific classification |
| limitations | Array of strings | Important limitations |
| attribution | String | Source or asset attribution |

Optional fields should be omitted when they have no meaningful value.

### 4.3 Field Validation Rules

**id**
  - Must be a string.
  - Must match the resource ID pattern.
  - Must be unique across the complete resource library.

**name**
  - Must be a non-empty string.
  - Must be understandable to users and AI agents.

**resource_type**
  - Must be exactly typography_style or design_template.

**schema_version**
  - Must identify the metadata contract used by the resource.
  - Must be a quoted string.
  - Initial value: "1.2".

**resource_version**
  - Must follow MAJOR.MINOR.PATCH semantic versioning.
  - Example: "1.0.0".

**status**
  - Must use one of the approved lifecycle values.

**summary**
  - Must be a concise, non-empty string.
  - Must explain the resource's primary purpose.

**domains**
  - Must be a non-empty array.
  - Every entry must use an approved domain value.
  - Duplicate domain values are prohibited.

**tags**
  - Must be a non-empty array of unique, lowercase descriptive strings.
  - Tags must not contain empty values.

**related_resources**
  - Must contain valid resource identifiers.
  - Duplicate identifiers are prohibited.
  - Empty references are prohibited.

**limitations**
  - Must be an array of non-empty strings when present.

**attribution**
  - Must be a non-empty string when present.

Unknown metadata fields must be reviewed before acceptance rather than silently becoming part of the canonical contract.

## 5. Resource Identifier System

Typography style identifiers:

TCS-STYLE-001
TCS-STYLE-002
TCS-STYLE-003

Design template identifiers:

TCS-TEMPLATE-001
TCS-TEMPLATE-002
TCS-TEMPLATE-003

### 5.1 Identifier Pattern

The required pattern is:

^TCS-(STYLE|TEMPLATE)-[0-9]{3,}$

### 5.2 Identifier Rules

1. Every resource must have a unique ID.
2. IDs must remain stable throughout the resource lifecycle.
3. IDs must never be reused.
4. Renaming a resource must not change its ID.
5. Deprecated IDs remain permanently reserved.
6. References must use resource IDs, not filenames.
7. IDs must not depend on a resource's position or alphabetical order.

The initial release targets 15 typography styles and 15 design templates.

These quantities are initial release targets, not permanent limits on library expansion.

## 6. Controlled Metadata Values

### 6.1 Resource Types

Allowed values:

  - typography_style
  - design_template

### 6.2 Resource Status

Allowed values:

  - draft
  - review
  - approved
  - deprecated

Lifecycle rules:

**draft:** Resource is being developed.

**review:** Resource is undergoing technical or creative review.

**approved:** Resource has passed the required acceptance process.

**deprecated:** Resource is retained for historical or dependency purposes but is no longer recommended for new use.

Only approved resources may be presented as finalized production resources.

Deprecated resources must not be newly recommended by automatic selection.

Existing references to deprecated resources must remain resolvable.

### 6.3 Creative Domains

Allowed values:

  - static_graphics
  - motion_graphics
  - video
  - web_ui
  - editorial

These values must be used consistently throughout the resource library.

### 6.4 Resource Versioning

Use semantic versioning:

MAJOR.MINOR.PATCH

Examples:

  - 1.0.0
  - 1.1.0
  - 1.1.1

A major version represents a breaking resource contract or behavioral change.

A minor version represents a backward-compatible addition or enhancement.

A patch version represents a correction or clarification that does not change the resource contract.

Schema version and resource version represent different things and must not be confused.

## 7. Typography Style Content Contract

Every typography style must contain these sections:

1. Overview
2. Visual Identity
3. Typography Characteristics
4. Font Direction
5. Color Direction
6. Effects and Treatments
7. Composition Guidance
8. Domain Applications
9. Limitations
10. Execution Instructions
11. Quality Criteria
12. References and Attribution

Each section must contain useful information.

If a section is not applicable, document the reason rather than inventing details.

## 8. Design Template Content Contract

Every design template must contain these sections:

1. Overview
2. Intended Purpose
3. Layout Architecture
4. Content Hierarchy
5. Typography Placement
6. Color and Background
7. Spacing and Alignment
8. Responsive Adaptation
9. Customization Boundaries
10. Domain Applications
11. Limitations
12. Execution Instructions
13. Quality Criteria
14. References and Attribution

Each section must have a clear purpose.

## 9. Canonical Resource Examples

The following examples demonstrate the required frontmatter structure.

They are illustrative examples, not finalized TypeCraft styles or templates.

### 9.1 Typography Style Example

A real resource file must begin exactly as follows:

````markdown
---
id: TCS-STYLE-001
name: Example Typography Style
resource_type: typography_style
schema_version: "1.2"
resource_version: "1.0.0"
status: draft
summary: An illustrative typography style resource.
domains:
  - static_graphics
  - video
tags:
  - display
  - typography
  - example
related_resources: []
---

# Example Typography Style

## Overview

An illustrative example demonstrating the resource structure.

## Visual Identity

Describe the intended visual identity.

## Typography Characteristics

Describe the typography characteristics.

## Font Direction

Describe suitable font characteristics.

## Color Direction

Describe the color direction.

## Effects and Treatments

Describe relevant effects.

## Composition Guidance

Describe composition requirements.

## Domain Applications

Explain the supported creative domains.

## Limitations

Document relevant limitations.

## Execution Instructions

Provide actionable instructions.

## Quality Criteria

Define the quality requirements.

## References and Attribution

Document relevant sources and attribution.
````

### 9.2 Design Template Example

A real resource file must begin exactly as follows:

````markdown
---
id: TCS-TEMPLATE-001
name: Example Design Template
resource_type: design_template
schema_version: "1.2"
resource_version: "1.0.0"
status: draft
summary: An illustrative composition template.
domains:
  - static_graphics
  - web_ui
tags:
  - layout
  - composition
  - example
related_resources: []
---

# Example Design Template

## Overview

An illustrative example demonstrating the template structure.

## Intended Purpose

Explain the purpose of the template.

## Layout Architecture

Describe the layout structure.

## Content Hierarchy

Define the content hierarchy.

## Typography Placement

Describe typography placement.

## Color and Background

Describe color and background direction.

## Spacing and Alignment

Define spacing and alignment.

## Responsive Adaptation

Explain adaptation requirements.

## Customization Boundaries

Identify customizable and fixed elements.

## Domain Applications

Explain suitable creative domains.

## Limitations

Document relevant limitations.

## Execution Instructions

Provide actionable instructions.

## Quality Criteria

Define quality requirements.

## References and Attribution

Document relevant sources and attribution.
````

## 10. Resource Relationship Rules

Resources may reference other resources.

Examples:

  - A typography style may reference suitable templates.
  - A template may reference suitable typography styles.
  - Multiple resources may be combined in one composition.

Rules:

1. Every reference must use a valid resource ID.
2. Every referenced ID must exist in the library.
3. A reference does not automatically imply mandatory compatibility.
4. Compatibility recommendations must be documented explicitly.
5. Deprecated resources must remain identifiable.
6. Missing references must be reported as validation errors.
7. Relationships must not create circular loading dependencies.
8. Explicit user selections take priority over automatic recommendations.

References should describe useful relationships without unnecessarily duplicating content.

## 11. Resource Retrieval and Loading

The core skill must retrieve resources according to the user's request.

Retrieval must consider:

  - Creative domain.
  - User requirements.
  - Explicit style selections.
  - Explicit template selections.
  - Resource status.
  - Relevant resource relationships.
  - Available execution tools.

Examples:

A video title request may require typography styles and video-specific guidance.

A website heading request may require web typography guidance and an appropriate template.

A poster request may require static graphic references.

The agent must not load every resource unnecessarily.

Automatic selection must not override explicit user selections.

## 12. Validation Requirements

Every resource must eventually pass automated structural validation.

### 12.1 YAML Validation

Check:

  - Valid YAML syntax.
  - Frontmatter starts on the first line.
  - Frontmatter has opening and closing delimiters.
  - Metadata values use the correct YAML types.
  - Required fields are present.
  - Unknown fields are reported.

### 12.2 Identifier Validation

Check:

  - Valid identifier pattern.
  - Unique IDs across the entire library.
  - No reuse of reserved identifiers.

### 12.3 Metadata Validation

Check:

  - Valid resource type.
  - Valid status.
  - Valid schema version.
  - Valid semantic resource version.
  - Valid creative domain values.
  - Unique tags.
  - Valid related resource identifiers.

### 12.4 Content Validation

Check:

  - Required headings are present.
  - Required sections are not empty.
  - Resource type matches the required section structure.
  - Markdown structure is valid.

### 12.5 Relationship Validation

Check:

  - Referenced IDs exist.
  - No duplicate references exist.
  - Deprecated resources are handled according to lifecycle rules.
  - Invalid relationships are reported.

### 12.6 Validation and Approval Separation

Passing automated validation does not automatically approve a resource.

Technical validation and creative quality approval are separate processes.

## 13. Creative Quality Review

Every resource must undergo creative review before approval.

The review must consider:

  - Typography accuracy.
  - Visual clarity.
  - Composition quality.
  - Readability.
  - Domain suitability.
  - Accessibility.
  - Execution practicality.
  - Resource originality.
  - Asset licensing.

Creative quality must not be inferred solely from metadata completeness.

## 14. Compatibility With the Agent Skills Specification

This schema governs TypeCraft's internal design resources.

It does not replace the official Agent Skills specification.

The primary installable skill must independently follow the official skill structure and metadata requirements.

Internal resource frontmatter must not be confused with the frontmatter of SKILL.md.

The core skill remains the orchestration and instruction entry point.

## 15. Future Validation Infrastructure

The resource library will initially use Markdown files with YAML frontmatter.

The validation implementation may use:

  - YAML parsing.
  - JSON Schema or an equivalent validation definition.
  - Resource ID uniqueness checks.
  - Required-field checks.
  - Controlled vocabulary checks.
  - Required-section checks.
  - Relationship integrity checks.
  - Automated regression tests.

The implementation must follow this canonical contract.

Validation rules must not be independently duplicated in conflicting scripts or documents.

## 16. Schema Evolution

Changes to the resource contract must be reviewed.

### Backward-Compatible Changes

Examples:

  - Adding an optional metadata field.
  - Clarifying an existing field description.
  - Adding an approved tag convention.

### Breaking Changes

Examples:

  - Renaming a mandatory field.
  - Changing an existing field's type.
  - Removing a required section.
  - Changing identifier semantics.

Breaking changes require a major schema version update and a documented migration strategy.

Existing resources must not be silently invalidated.

## 17. Acceptance Criteria

A resource may proceed to creative review only when:

  - [ ] It has a unique permanent ID.
  - [ ] Its filename follows naming rules.
  - [ ] Its YAML frontmatter is valid.
  - [ ] All mandatory metadata fields are present.
  - [ ] All metadata types are correct.
  - [ ] Controlled values are valid.
  - [ ] Its resource version follows semantic versioning.
  - [ ] Required content sections are complete.
  - [ ] Related resource IDs are valid.
  - [ ] Limitations are documented.
  - [ ] Quality criteria are defined.
  - [ ] Asset licensing has been considered.
  - [ ] The resource follows the authoring standard.

Final approval requires both technical validation and creative review.

## 18. Core Schema Philosophy

Structured metadata.

Rich creative knowledge.

Stable identifiers.

Independent reusable resources.

Reliable retrieval.

Automated validation.

Human creative judgment.

One expandable resource system.


---

## 19. Normative Validation Contract

**Contract version:** 1.2

This section defines the precise validation behavior required for Resource
Schema v1.2. Where an earlier section is less specific or conflicts with
this section, the rules in this section take precedence.

### 19.1 Validation Modes

The validator must support two modes:

**Development mode**
- Intended for resources under development.
- Unknown metadata fields produce warnings.
- Other structural and metadata violations remain errors.
- Does not approve or change the lifecycle status of a resource.

**Acceptance mode**
- Intended for resources submitted for acceptance.
- Unknown metadata fields are errors.
- All required structural and metadata checks must pass.
- Does not automatically set status to approved.

### 19.2 Schema Version

- The only supported schema version in this release is the string `"1.2"`.
- The YAML value must be parsed as a string, not a number.
- Unsupported schema versions are validation errors.
- Future schema versions require an explicit schema and validator update.

### 19.3 String Validation

- Required strings must contain at least one non-whitespace character.
- Leading and trailing whitespace must not be used to disguise empty values.
- The validator must not silently rewrite resource content.
- `id`, `name`, `resource_type`, `schema_version`, `resource_version`,
  `status`, and `summary` must be strings.

### 19.4 Identifier Validation

- IDs must match `^TCS-(STYLE|TEMPLATE)-[0-9]{3,}$`.
- ID comparisons are case-sensitive.
- IDs must be unique across the complete resource library.
- Deprecated IDs remain permanently reserved.
- IDs must never be reused.
- A resource must not reference its own ID.
- Duplicate IDs must be reported with the conflicting resource locations.

### 19.5 Resource Version Validation

- Resource versions must contain exactly three numeric components:
  `MAJOR.MINOR.PATCH`.
- Each component must be a non-negative integer.
- Leading zeroes are prohibited except for the value `0`.
- Prerelease identifiers and build metadata are not supported in v1.2.
- Examples of valid values: `0.1.0`, `1.0.0`, `1.2.3`.
- Examples of invalid values: `1.0`, `01.0.0`, `1.0.0-beta`,
  `1.0.0+build`.

### 19.6 Domain and Tag Validation

The only permitted domain values are:

- `static_graphics`
- `motion_graphics`
- `video`
- `web_ui`
- `editorial`

Domain matching is exact and case-sensitive.

Tags must:
- Be lowercase strings.
- Match `^[a-z0-9]+(?:-[a-z0-9]+)*$`.
- Contain no empty values.
- Be unique within the resource.
- Use exact, case-sensitive duplicate comparison.

### 19.7 Optional Field Validation

**related_resources**
- Must be an array of strings when present.
- Every value must match the resource ID pattern.
- Empty values and duplicate references are prohibited.
- Self-references are prohibited.
- Every referenced ID must exist in the library.

**category**
- Must be a non-empty string when present.
- It must describe a meaningful classification.
- Whitespace-only values are invalid.

**limitations**
- Must be an array of strings when present.
- Every entry must be non-empty after whitespace trimming.

**attribution**
- Must be a non-empty string when present.
- Multiple attribution sources must be documented in this string
  in v1.2. The field is not an array in this schema version.

### 19.8 Relationship and Lifecycle Validation

- Mutual references between resources are permitted.
- A reference does not imply automatic compatibility.
- Compatibility claims must be explicitly documented.
- Circular loading dependencies are prohibited.
- Circular references alone are not loading dependencies and are permitted.
- References to deprecated resources remain valid.
- References to deprecated resources produce a warning.
- Deprecated resources must not be newly recommended by automatic selection.
- Missing references are errors.

### 19.9 Unknown Metadata Fields

- Known fields are the mandatory and optional fields defined in Section 4.
- Unknown fields must never be silently accepted.
- Development mode reports unknown fields as warnings.
- Acceptance mode reports unknown fields as errors.
- Adding a new canonical field requires a schema revision.

### 19.10 YAML and Content Validation

The validator must check:

- Valid YAML syntax.
- Opening frontmatter delimiter on the first line.
- A valid closing frontmatter delimiter before Markdown content.
- Correct YAML types for all known fields.
- Required metadata presence and non-empty values.
- Required headings for the declared resource type.
- Non-empty required content sections.
- Valid resource-type-specific content structure.

The validator must report the resource path and relevant field or section
for every detected issue.

### 19.11 Validation Results

Every validation run must produce:

- Overall result: PASS or FAIL.
- Validation mode: development or acceptance.
- Error count.
- Warning count.
- Specific issue descriptions.
- Resource path for each reported issue.

A resource passes a validation run only when that run contains no errors.

Warnings do not independently cause validation failure.

### 19.12 Validation and Approval Separation

Validation is a technical quality gate, not an approval mechanism.

- Passing validation does not change resource status.
- Failing validation does not automatically rewrite resource content.
- Creative review remains a separate acceptance requirement.
- Only the established acceptance process may change a resource to `approved`.
- The validator must never modify lifecycle status automatically.


### 19.13 Permanent Resource ID Registry

The project must maintain a permanent registry of every resource ID ever
assigned.

The canonical registry location is:

`registry/resource-ids.yaml`

The registry must retain identifiers even when their resource files are
renamed, moved, deprecated, or retired.

Each registry entry must record:

- `id`: The permanent resource identifier.
- `resource_type`: The assigned resource type.
- `registry_status`: The registry lifecycle state.

Allowed registry states:

Registry status mapping:

- Resources with lifecycle status `draft`, `review`, or `approved` use
  registry status `active`.
- Resources with lifecycle status `deprecated` use registry status
  `deprecated`.
- Registry status `retired` is used only after the resource file has
  been removed. Its ID remains permanently reserved.


- `active`: The resource currently exists in the library.
- `deprecated`: The resource remains in the library but is no longer
  recommended for new use.
- `retired`: The resource has been removed, but its identifier remains
  permanently reserved.

Registry rules:

1. Every resource in the library must have exactly one registry entry.
2. Every registry ID must be unique.
3. An ID must never be assigned to a different resource.
4. Retired IDs must never be reused.
5. A resource ID must match its resource type:
   - `typography_style` requires the `TCS-STYLE-` prefix.
   - `design_template` requires the `TCS-TEMPLATE-` prefix.
6. The registry resource type must match the resource frontmatter.
7. Active and deprecated registry entries must resolve to an existing
   resource file.
8. Retired registry entries must not resolve to an active resource file.
9. Removing a resource file must not remove its registry entry.
10. Renaming or moving a resource must not change its ID.

The validator must check both the resource library and the permanent registry.

A duplicate, missing, or inconsistent registry entry is an acceptance error.

The registry records identity and reservation. It does not replace resource
frontmatter or determine creative approval.
