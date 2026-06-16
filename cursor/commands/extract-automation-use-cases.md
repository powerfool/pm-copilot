# extract-automation-use-cases
This command will be available in chat with /extract-automation-use-cases

Extract automation use cases from a school's automation analysis and add them to the identified_automation_use_cases.md catalog.

## Context

You are building a product-focused catalog of **unmet needs** that schools are solving with complex, repeated automations. The goal is to inform future product development by identifying patterns where simple platform features could replace automation workarounds.

## Your Task

1. **Read the attached school analysis file** (e.g., School_5f932_Automation_Analysis.md)
2. **Read the current catalog** at `automations_research/identified_automation_use_cases.md`
3. **Extract significant use cases** from the analysis that represent unmet platform needs
4. **Group use cases into appropriate buckets** (create new buckets if needed, or add to existing ones)
5. **Update the catalog file** with the new school's examples

## What Makes a Use Case "Significant"?

Include use cases that:
- Require **multiple automations** to accomplish a single goal
- Show **replication patterns** (e.g., one automation per course, per organization, per tier)
- Use **workarounds** (e.g., staging tags, tag cleanup, manual steps)
- Have **high execution counts** (indicates real usage, not just prepared automations)
- Reveal **missing platform features** that would eliminate automation complexity

Skip use cases that:
- Are simple, one-off automations with no replication
- Don't suggest a broader product need
- Are edge cases specific to one school's unusual setup

## Catalog Structure

Each use case bucket follows this format:

```markdown
# [Bucket Name - describes the core need]

## Case 1: [Specific scenario from a school]
**Pattern:** [Trigger] -> [Actions]

[Numbered workflow steps showing the automation pattern]

### Unmet Need
- **[Feature name]**: Description of what's missing from the platform
- **[Feature name]**: Another missing capability
- [List 2-5 specific unmet needs this use case reveals]

**Schools where identified:**
- [school_id] - [School Name]
-- Comments: [Key stats, context, execution counts, noteworthy details]

## Case 2: [Another scenario/variation]
[Same structure]

### Unmet Need
[List unmet needs]

**Schools where identified:**
- [another_school_id] - [Another School]
-- Comments: [Different context showing same core need]

---
```

## How to Group Use Cases

**Group by CORE NEED, not by implementation:**

Good grouping:
- Bucket: "Admin Notifications"
  - Case 1: Notify on enrollment
  - Case 2: Notify on completion
  - Case 3: Notify on cancellation
  -> All are the same need: "Tell admins when events happen"

Bad grouping:
- Bucket: "Enrollment Notifications"
- Bucket: "Completion Notifications"
- Bucket: "Cancellation Notifications"
-> These are fragmented by implementation, not unified by need

**Look for cross-school patterns:**
- If 2+ schools solve the same problem differently, that's a strong signal
- Note variations in the "Schools where identified" section
- Highlight if one school's workaround is more sophisticated than another's

## Bucket Examples

Here are the main buckets typically found (create new ones as needed):

1. **Admin Notifications** - Alerting staff about events
2. **Inactivity & Re-engagement** - Bringing back inactive users
3. **Progressive Course Access & Prerequisites** - Sequential unlocking
4. **Exam & Certification Gating** - Complex prerequisite logic
5. **New User Onboarding** - First-time user setup
6. **Seasonal Promotional Tracking** - Campaign attribution
7. **Multi-Tenancy & Organization Management** - B2B2C infrastructure
8. **Automatic Recertification & Compliance** - Certificate expiry/renewal
9. **Subscription Tier & Lifecycle Management** - Managing subscription variants
10. **Certificate Delivery to Third Parties** - B2B2C certificate routing
11. **Structured Tag Taxonomies** - Tag-based business logic
12. **Time-Bound & Scheduled Access** - Cohort/temporal management

## Important Guidelines

1. **Don't duplicate existing entries** - If a school is already listed for a use case, don't add it again (unless it shows a significantly different variation)

2. **Be specific in "Unmet Need" bullets** - Don't just say "better automation." Say "Global notification rules: 'Notify [these people] when [any course / courses matching criteria] completes'"

3. **Include quantitative evidence** - Execution counts, number of automations, percentages (e.g., "44% of actions are tag removals")

4. **Preserve context in comments** - When adding a school, include relevant details like automation count, execution stats, specific tag names, pain point evidence

5. **Look for Pain Points & Workarounds sections** - These explicitly call out missing features

6. **Check Operational Overhead sections** - These show scalability issues

7. **Read Automation Architecture sections** - These explain the patterns in detail

## Output Format
**Important:** Update the catalog silently. Do not provide a summary unless there are conflicts or questions that require my input.

---

Begin extraction now. Remember: Focus on UNMET NEEDS that could become PLATFORM FEATURES, not just describing what schools are doing.
