# TYPECRAFT SKILLS

# Authoring Standard v1.0

**Document ID:** TCS-AS-001
**Status:** Proposed
**Version:** 1.0
**Applies to:** Core skill, typography styles, design templates, domain references, examples and evaluation resources.

---

## 1. Purpose

This document establishes the technical, creative and structural standards for authoring resources within TypeCraft Skills.

TypeCraft is a typography intelligence system for creative AI agents.

Its resources must enable an AI agent to:

1. Understand a user's creative requirements.
2. Identify the appropriate creative domain.
3. Select or respect typography styles.
4. Select or respect design templates.
5. Combine design resources intelligently.
6. Adapt typography to the intended output medium.
7. Execute designs using available tools.
8. Evaluate the resulting design against defined quality criteria.

Every resource must contribute to this workflow.

## 2. Foundational Principles

All TypeCraft resources must follow these principles.

### 2.1 Tool Independence

Typography knowledge and design principles must not depend on a particular AI vendor or platform.

### 2.2 Tool Awareness

Execution instructions must adapt to the tools and capabilities available in the connected AI environment.

### 2.3 Modularity

Typography styles, design templates and domain-specific guidance must remain independently reusable.

### 2.4 Consistency

Resources serving the same purpose must follow consistent documentation and metadata structures.

### 2.5 User Control

Explicit user selections, content requirements and design constraints must be respected.

### 2.6 Practical Execution

Instructions must translate creative concepts into actionable design decisions.

### 2.7 Progressive Disclosure

Detailed references must be loaded only when relevant to the user's request.

### 2.8 Measurable Quality

Resources must have identifiable quality requirements and testable acceptance criteria.

---

## 3. TypeCraft Resource Architecture

TypeCraft uses the following resource categories.

| Resource | Responsibility |
|---|---|
| Core Skill | Understand requests and coordinate the design workflow |
| Typography Styles | Define visual typography identities |
| Design Templates | Define composition and layout structures |
| Design Principles | Define universal typography and composition knowledge |
| Domain References | Explain domain-specific execution requirements |
| Examples | Demonstrate valid applications |
| Evaluation Resources | Verify design quality and instruction compliance |

Each resource must have one clear primary responsibility.

Avoid duplicating authoritative information across multiple files.

The initial v1.0 library contains 10 typography styles and 10 design templates. Future additions must follow the same authoring and validation standards.

---

## 4. Typography Style Authoring Standard

Every typography style must follow the established style resource structure.

### 4.1 Identity

Each style must define:

- Unique style ID.
- Style name.
- Short description and summary.
- Style category.
- Core visual identity.
- Intended creative applications.

### 4.2 Visual Characteristics

Describe:

- Overall visual appearance.
- Letterform personality.
- Geometric or organic characteristics.
- Typeface proportions.
- Visual weight.
- Texture and material qualities.
- Distinctive visual treatments.

Descriptions must be specific enough to guide an AI agent.

### 4.3 Typography Specifications

Define recommendations for:

- Typeface category.
- Typeface characteristics.
- Font weight.
- Font width.
- Letter spacing.
- Line height.
- Capitalization.
- Text hierarchy.
- Display and supporting text relationships.

Use measurable values where appropriate.

Do not require a specific commercial font when a suitable alternative can achieve the intended result.

### 4.4 Color Specifications

Document:

- Primary color direction.
- Secondary color direction.
- Background treatment.
- Contrast requirements.
- Alternative color combinations.
- Appropriate use of gradients.

### 4.5 Effects and Treatments

Describe relevant treatments, such as:

- Shadows.
- Outlines.
- Gradients.
- Texture.
- Layering.
- Distortion.
- Three-dimensional treatments.
- Lighting and depth.
- Decorative effects.

Explain when each treatment is appropriate.

### 4.6 Composition Guidance

Define:

- Alignment.
- Positioning.
- Scale.
- Proportion.
- Negative space.
- Visual hierarchy.
- Relationship between text and imagery.

### 4.7 Domain Suitability

Evaluate suitability for:

1. Static graphics.
2. Motion graphics.
3. Video typography.
4. Web and UI.
5. Editorial design.

Do not assume that a style is equally suitable for every domain.

### 4.8 Limitations

Identify:

- Readability limitations.
- Accessibility concerns.
- Background compatibility issues.
- Scaling limitations.
- Motion-related limitations.
- Situations where the style should not be recommended.

### 4.9 Execution Instructions

Provide actionable guidance for applying the style.

Instructions should distinguish between mandatory visual characteristics and optional creative variations.

### 4.10 Quality Criteria

Define the conditions required for the style to be applied correctly.

### 4.11 References and Attribution

Document relevant design references, historical influences and third-party assets where applicable.

Do not imply endorsement or official affiliation with referenced designers, studios or organizations.

---

## 5. Design Template Authoring Standard

A design template defines composition and information arrangement.

It does not independently define the complete typography style.

Every template must follow the established design template resource structure.

### 5.1 Identity

Each template must define:

- Unique template ID.
- Template name.
- Short description and summary.
- Template category.
- Intended purpose.
- Suitable output domains.

### 5.2 Layout Architecture

Define:

- Canvas or viewport structure.
- Primary content area.
- Secondary content areas.
- Text placement.
- Image placement.
- Alignment.
- Spacing.
- Visual balance.

### 5.3 Content Hierarchy

Define the intended hierarchy:

- Primary headline.
- Secondary headline.
- Supporting text.
- Body content.
- Labels.
- Metadata.
- Call-to-action elements where appropriate.

Not every template requires every content type.

### 5.4 Layout Adaptation

Explain how the layout responds to:

- Different aspect ratios.
- Different canvas dimensions.
- Different screen sizes.
- Different content lengths.
- Different output formats.

### 5.5 Typography Integration

Explain how typography styles can be applied to the template without compromising its composition or hierarchy.

### 5.6 Customization Boundaries

Identify:

- Elements that must remain consistent.
- Elements that can be customized.
- Optional elements.
- Conditions that may require layout changes.

### 5.7 Domain Suitability

Specify how the template can be adapted to static graphics, motion graphics, video, web or editorial applications.

### 5.8 Execution Instructions

Provide practical instructions for generating the composition.

### 5.9 Quality Criteria

Define the conditions required for the template to be applied correctly.

### 5.10 References and Attribution

Document relevant layout references and third-party assets where applicable.

---

## 6. Resource Identification and Metadata

Every design resource must have a stable identifier.

### 6.1 ID Naming Convention

The initial v1.0 resource ranges are:

- Styles: TCS-STYLE-001 through TCS-STYLE-010.
- Templates: TCS-TEMPLATE-001 through TCS-TEMPLATE-010.

Future additions must continue the relevant sequence.

Identifiers must never be reused for unrelated resources.

### 6.2 Required Metadata

Every resource must include the fields required by the TypeCraft Resource Schema.

The current required metadata includes:

- `id`
- `name`
- `resource_type`
- `schema_version`
- `resource_version`
- `version`
- `status`
- `summary`
- `domains`
- `tags`

The resource type must use the established values:

- `typography_style`
- `design_template`

Metadata values must follow the Resource Schema and its validation requirements.

Do not introduce alternative field names or lifecycle values without updating the schema and validator together.

### 6.3 Resource Lifecycle

TypeCraft uses the following resource status values:

| Status | Meaning |
|---|---|
| `draft` | Resource is under development and intended for development or testing only |
| `review` | Resource is being evaluated and is not yet approved for normal production use |
| `approved` | Resource has passed the required review and testing and may be used in normal production workflows |
| `deprecated` | Resource is no longer recommended for automatic selection |

Only approved resources should be treated as finalized production resources.

Review and draft resources must not be presented as approved.

Deprecated resources must not be automatically selected. They may be used when explicitly requested, provided their limitations are disclosed.

### 6.4 Registry Consistency

Every registered resource must have a unique ID and match its resource file.

Registry metadata and resource metadata must remain consistent.

Changes to resource identity, type or lifecycle must be reflected in the registry and validated.

---

## 7. Style and Template Combination Rules

Typography styles and design templates must remain independent.

The selection system must support:

### 7.1 Automatic Selection

The agent selects suitable styles and templates based on the user's request.

### 7.2 Manual Selection

The agent uses the style and template explicitly selected by the user.

### 7.3 Mixed Selection

The user selects one design dimension while the agent determines the other.

### 7.4 Multiple Combinations

Users may combine multiple styles and templates when the composition requires them.

For example, a design may use one display typography treatment for its headline and a different supporting typography treatment for secondary information.

### 7.5 Conflict Resolution

When a combination creates visual or functional conflicts:

1. Preserve explicit user requirements.
2. Identify the specific conflict.
3. Explain the design limitation.
4. Propose a compatible alternative.
5. Do not silently replace user-selected resources.

### 7.6 Selection Transparency

When useful, the agent should briefly explain why it selected a particular style or template.

---

## 8. Creative Domain Adaptation Standard

The same typography identity may require different execution methods across different media.

### 8.1 Static Graphics

Consider:

- Canvas dimensions.
- Aspect ratio.
- Text hierarchy.
- Typography scale.
- Alignment.
- Export requirements.

### 8.2 Motion Graphics

Consider:

- Animation behavior.
- Timing.
- Easing.
- Entrance and exit transitions.
- Movement direction.
- Readability during animation.
- Motion consistency.

### 8.3 Video Typography

Support relevant applications including:

- Opening titles.
- Closing titles.
- Lower thirds.
- Text overlays.
- Captions.
- Credits.
- Chapter titles.
- Branded title sequences.

Consider video resolution, safe areas, contrast, timing and viewing conditions.

### 8.4 Web and UI Typography

Consider:

- Responsive typography.
- Screen sizes.
- Font loading.
- Performance.
- Accessibility.
- Component hierarchy.
- Interactive states.
- Design-system consistency.

### 8.5 Editorial Design

Consider:

- Page dimensions.
- Grid systems.
- Reading flow.
- Line length.
- Paragraph hierarchy.
- Headlines.
- Captions.
- Publication consistency.

Domain-specific instructions must be maintained separately from universal typography principles when their requirements differ.

---

## 9. Core Skill Decision Workflow

The core skill must follow a consistent decision-making process.

### Stage 1: Request Understanding

Identify:

- User's objective.
- Intended audience.
- Content.
- Creative domain.
- Desired output.
- Explicit design preferences.
- Technical constraints.

### Stage 2: Requirement Classification

Separate:

- Mandatory requirements.
- User preferences.
- Optional creative choices.
- Technical limitations.

### Stage 3: Design Selection

Determine the appropriate selection mode:

- Automatic.
- Manual.
- Mixed.

Respect explicit user selections.

### Stage 4: Resource Retrieval

Load only the relevant typography styles, templates and domain references.

Avoid loading the entire knowledge library for every request.

### Stage 5: Design Planning

Determine:

- Typography hierarchy.
- Composition.
- Color direction.
- Layout.
- Effects.
- Domain-specific adaptations.

### Stage 6: Capability Assessment

Check which tools are actually available.

Determine whether the requested output can be generated directly, requires another tool or requires providing instructions.

Never claim that an unavailable tool has executed an operation.

### Stage 7: Execution

Produce the design or the most useful actionable execution instructions supported by the environment.

### Stage 8: Quality Verification

Evaluate the result against the relevant quality criteria.

### Stage 9: Final Delivery

Provide the result in the requested format, explaining important limitations when necessary.

---

## 10. AI Instruction Writing Standards

All instructions must:

- Use clear and direct language.
- Specify the intended action.
- Separate mandatory requirements from recommendations.
- Avoid contradictory instructions.
- Avoid vague descriptions where measurable guidance is possible.
- Preserve exact user-provided text unless editing is requested.
- Respect explicit design selections.
- Avoid unsupported tool assumptions.
- Avoid unnecessary repetition.
- Use consistent terminology.

Instructions must be understandable without relying on undocumented conversation history.

---

## 11. Accessibility and Readability Standards

Every applicable resource must consider:

- Text/background contrast.
- Readable font sizes.
- Appropriate line spacing.
- Clear visual hierarchy.
- Legibility at the intended viewing size.
- Responsive readability.
- Motion sensitivity.
- Text visibility over images and video.

Decorative effects must never compromise essential information.

Where applicable, recommend WCAG-aligned contrast practices for digital interfaces.

Accessibility requirements should be adapted to the intended output medium.

---

## 12. Asset and Intellectual Property Standards

All external assets must have documented usage rights.

This includes:

- Fonts.
- Images.
- Illustrations.
- Textures.
- Icons.
- Videos.
- Audio.
- Other third-party creative resources.

Requirements:

1. Do not distribute copyrighted assets without permission.
2. Record relevant license information.
3. Include required attribution.
4. Distinguish original assets from third-party assets.
5. Verify redistribution rights before including assets.
6. Do not assume that publicly accessible assets are free to redistribute.

MIT licensing of the project source code does not automatically grant rights to third-party assets.

---

## 13. Testing and Evaluation Standards

Each approved resource must have testable acceptance criteria.

Testing should cover:

### 13.1 Instruction Compliance

Does the agent follow the resource instructions?

### 13.2 Design Accuracy

Does the result reflect the intended visual identity or layout?

### 13.3 Selection Accuracy

Does the agent choose appropriate resources and respect user selections?

### 13.4 Domain Adaptation

Does the resource work appropriately in its intended creative domain?

### 13.5 Readability

Is the essential text legible?

### 13.6 Capability Honesty

Does the agent accurately represent what it can and cannot execute?

### 13.7 Regression Testing

Do changes to the resource cause previously working examples to fail?

Every test case should document:

- Test ID.
- Input request.
- Expected behavior.
- Evaluation criteria.
- Actual result.
- Pass or fail status.

A resource must not be marked approved solely because its documentation is complete.

---

## 14. Quality Evaluation Framework

TypeCraft should evaluate outputs using the following dimensions.

| Dimension | Evaluation |
|---|---|
| Intent accuracy | Correct understanding of the request |
| Typography accuracy | Appropriate typography characteristics |
| Layout accuracy | Correct composition and hierarchy |
| Readability | Clear and legible text |
| Domain suitability | Appropriate medium-specific adaptation |
| User control | Respect for explicit selections |
| Execution accuracy | Correct use of available tools |
| Accessibility | Appropriate accessibility considerations |
| Consistency | Compliance with selected design resources |

Evaluation scores and acceptance thresholds must be defined in the testing specification before being used as release criteria.

Do not claim objective quality scores without an established evaluation method.

---

## 15. Versioning and Change Management

All resources must have version histories.

Changes should be reviewed according to their impact.

### 15.1 Minor Changes

Corrections, clarifications and non-breaking improvements.

### 15.2 Major Changes

Changes that modify resource structure, selection behavior, execution requirements or compatibility expectations.

### 15.3 Lifecycle Changes

Changes to resource status must follow the defined lifecycle and review requirements.

A resource must not be marked approved without the required review and testing.

Deprecated resources must not be silently deleted if other resources depend on them.

Related references, examples and registry entries must be reviewed whenever a resource changes.

---

## 16. Documentation and Progressive Disclosure

The primary skill entry point must remain concise and operational.

Detailed knowledge must be stored in appropriate reference files.

Examples must demonstrate practical applications rather than duplicate entire reference documents.

Supporting resources should be loaded according to task relevance.

The repository must maintain one authoritative version of each resource.

The Resource Schema and validator must be updated together whenever the resource structure or metadata requirements change.

---

## 17. Final Authoring Acceptance Checklist

A resource may be considered ready for approval only after reviewing the following:

- [ ] Resource has a unique identifier.
- [ ] Resource follows the required documentation structure.
- [ ] Its purpose and responsibilities are clear.
- [ ] Required metadata is complete and valid.
- [ ] Instructions are actionable.
- [ ] Typography hierarchy is defined where applicable.
- [ ] Composition is defined where applicable.
- [ ] Relevant creative domains are identified.
- [ ] Limitations are documented.
- [ ] User-selection rules are respected.
- [ ] Accessibility and readability are considered.
- [ ] Asset licensing has been reviewed.
- [ ] Related resources are correctly referenced.
- [ ] Test cases have been defined.
- [ ] Required validation checks pass.
- [ ] No unsupported AI capabilities are claimed.
- [ ] The resource is consistent with the TypeCraft architecture.

Approval must be based on review and testing, not merely completion of the document.

---

## 18. Foundational Authoring Philosophy

One consistent authoring standard.

Independent reusable design resources.

Clear typography intelligence.

Flexible design combinations.

Tool-aware execution.

Measurable quality.

Responsible asset usage.

One coherent creative system.

**TYPECRAFT SKILLS — One library. Every creative developer. Beautiful typography without boundaries.**
