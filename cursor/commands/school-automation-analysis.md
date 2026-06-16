# school-automation-analysis
This command will be available in chat with /school-automation-analysis

Analyze a school's automation usage based on their JSON export file.

## Context: System vs. User-Defined Automations

**System-Generated Automations:**
- Trigger type: `user-created-updated-group`
- Automatically created by the platform when user group rules are configured
- Example: When you set a user group rule like "Has any of the Tags -> SchoolName",
  the platform creates a system automation that adds users to that group when the tag is applied
- These are NOT manually created by the school admin
- They appear in the automation list but represent user group membership logic, not custom workflows

**User-Defined Automations:**
- All other trigger types (e.g., `user-joined-group`, `tag-added`, `courses-completed`, `assessment-submitted`)
- Manually created by school admins to orchestrate workflows
- Represent actual business logic and learning journey design

## Your Analysis Tasks

### 1. Automation Inventory
Count and categorize all automations by trigger type. Provide:
- Total automation count
- Count per trigger type (sorted by frequency)
- Percentage breakdown
- Identify how many are system-generated vs. user-defined

### 2. Multi-Tenancy Analysis
Look for patterns suggesting per-tenant (e.g., per-school, per-organization, per-cohort) replication:
- Are there many automations with similar patterns but different entity IDs?
- Do automation names suggest repeated patterns? (e.g., "Community Access - [School Name]")
- Estimate how many unique workflow patterns exist vs. per-tenant replications

### 3. Workflow Pattern Identification
Identify the main automation use cases:
- **Access Management:** How do users gain access to content?
- **Learning Journeys:** How are users guided through courses?
- **Community/Social:** How are users added to social spaces?
- **Progress Tracking:** How is completion/progress tracked?
- **Email/Communication:** What email workflows exist?
- **Gamification/Badges:** Any badge or achievement systems?
- **Assessment-Based Logic:** Are quizzes/assessments used as workflow triggers?

### 4. Automation Chain Analysis
For the top 10-15 most common trigger types:
- What actions do they typically trigger?
- Are there sequential automation chains? (e.g., Course A complete -> enroll Course B -> Course B complete -> add tag -> enroll Course C)
- What conditions are commonly used?

### 5. Tag Strategy Analysis
Examine how tags are used:
- What types of tags appear? (access tags, progress tags, organizational tags, role tags, etc.)
- Are tags used as "routing" mechanisms between automations?
- Any patterns in tag naming conventions?

### 6. Unused/Zero-Execution Automations
If execution counts are available:
- What percentage of automations have never fired?
- Why might they exist but not be used? (e.g., prepared for future tenants)

### 7. Operational Insights
Based on the automation patterns, infer:
- What is the school's primary use case? (e.g., B2B2C serving multiple organizations, cohort-based learning, self-paced marketplace)
- What are the likely pain points driving automation complexity?
- Are there workarounds evident in the automation design? (e.g., using assessments for access control)

### 8. Scalability Assessment
- How does automation count scale with the school's apparent size?
- Are there automation patterns that would become unmanageable at scale?
- What would be needed to reduce automation overhead?

## Output Format

Please structure your analysis as follows:

### Executive Summary
- Total automation count and key finding (one paragraph)
- Primary use case of the school
- Headline insight about automation architecture

### Critical Insight: Automation Breakdown
- Table showing trigger types, counts, percentages, and what they represent
- Distinction between system-generated, per-tenant replications, and unique workflows

### Automation Architecture
Describe the main automation patterns:

#### 1. [Use Case Name] (e.g., School Onboarding)
- **Purpose:** Very short description of what problem this solves
- **Automation Pattern:** Trigger -> Conditions -> Actions
- **Scale:** How many instances exist
- **Tags Involved:** Key tags used
- **Workflow Example:** Step-by-step flow

#### 2. [Next Use Case]
[Repeat structure]

### Tag Strategy
- Tag categories identified
- How tags orchestrate workflows
- Naming conventions observed

### Automation Statistics
- Complete trigger type breakdown
- Most common action types
- Condition patterns
- Automation chains identified

### Pain Points & Workarounds
Based on automation patterns, identify:
- What problems might the school be working around?
- What features might be missing that they need?
- Evidence of "hacky" solutions

### Operational Overhead
- Per-tenant setup requirements
- Manual steps likely required
- Scalability challenges

### Key Takeaways for Product Team
- What does this automation usage reveal about product gaps?
- What features could simplify this school's setup?
- Are there scalability or UX issues to address?

### Recommendations
- For the school: How to optimize their automation setup
- For the product team: What features would help this use case

## Batch Processing Workflow (Optional)

**For analyzing multiple schools efficiently:**

1. **Pre-generate all analysis files:**
```bash
cd <YOUR_WORKSPACE_PATH>/automations_research

for file in source_data/*.json; do
    school_id=$(basename "$file" .json | sed 's/_combined$//')
    if [[ "$file" == *_combined.json ]]; then
        continue
    fi
    if ls source_data_split/${school_id}_part*.json 1> /dev/null 2>&1; then
        echo "Processing split files for $school_id..."
        python3 combine_split_files.py ${school_id}
        cd automation_explorer
        python3 automation_analyzer_lib.py ../source_data/${school_id}_combined.json
        cd ..
        rm source_data/${school_id}_combined.json
    else
        echo "Processing $file..."
        cd automation_explorer
        python3 automation_analyzer_lib.py "../$file"
        cd ..
    fi
done
```

2. **Then use this command to create reports on-demand:**
   - Simply reference the school ID when invoking this command
   - The analysis file will already exist in `analyzed_automations/`
   - Report generation becomes instant

---

## Your Analysis Process

### Step 0: Check for Existing Report

**Before starting, check if a report already exists:**

Look in `<YOUR_WORKSPACE_PATH>/automations_research/reports/` for `{school_id}_report.md`.

**If report exists:**
- STOP - Report already completed
- Inform the user: "Report already exists at `reports/{school_id}_report.md`"
- Ask: "Would you like to regenerate this report?"
- If NO -> End here
- If YES -> Proceed to Step 1

**If report does NOT exist:**
- Proceed to Step 1

### Step 1: Locate or Generate Analysis Data

**Check if analysis already exists:**

Look in `<YOUR_WORKSPACE_PATH>/automations_research/analyzed_automations/` for a file matching the pattern `{school_id}_analysis.json`.

**If analysis file exists:** Skip to Step 2.

**If analysis file does NOT exist:**

**First, locate the source data file(s):**

1. **Check for split files** in `source_data_split/`:
   - Look for files matching pattern: `{school_id}_part*.json`
   - If split files exist, they need to be combined before analysis

2. **Check for original file** in `source_data/`:
   - Look for: `{school_id}.json`
   - If file exists and is < 1MB, use it directly

**Processing options:**

**Option A: Split files exist (recommended for large files)**
```bash
cd <YOUR_WORKSPACE_PATH>/automations_research
python3 combine_split_files.py <school_id>
cd automation_explorer
python3 automation_analyzer_lib.py ../source_data/<school_id>_combined.json
rm ../source_data/<school_id>_combined.json
```

**Option B: Original file exists and is < 1MB**
```bash
cd <YOUR_WORKSPACE_PATH>/automations_research/automation_explorer
python3 automation_analyzer_lib.py ../source_data/<school_id>.json
```

### Step 2: Review Analysis Data

Read `<YOUR_WORKSPACE_PATH>/automations_research/analyzed_automations/{school_id}_analysis.json`.

The analysis file includes:
- `school_id` and `source_file` metadata for traceability
- Complete statistics, tag analysis, organization patterns, chains, subscriptions, and execution data

### Step 3: Generate Custom Analysis (When Needed)

**You ARE permitted to create custom Python scripts** when standard analysis is insufficient.

**Examples of when to write custom code:**
- Novel pattern detection specific to this school
- Complex workflow mapping requiring custom logic
- Comparative analysis with previous schools
- Statistical analysis beyond basic counts
- Domain-specific pattern detection

### Step 4: Write Intelligent Report

**YOU (the AI) write the markdown analysis** using the data. The library provides facts; you provide insights, strategic thinking, and recommendations.

**Report Output Requirements:**
- **Filename:** `{school_id}_report.md`
- **Location:** `<YOUR_WORKSPACE_PATH>/automations_research/reports/`

**At the end of the report, add metadata:**
```markdown
---
## Report Metadata
- **School ID:** {school_id}
- **Source File:** {source_file}
- **Analysis File:** `analyzed_automations/{school_id}_analysis.json`
- **Report Generated:** {current_date}
```

---

## Input Information

**School ID to Analyze:** [Provide the school ID]

The command will automatically:
1. **Check if report already exists** in `reports/` -> If yes, ask to regenerate
2. Check if the analysis file exists in `analyzed_automations/`
3. If not found, locate source data (split files first, then original)
4. Generate analysis from the appropriate source file(s)
5. Use the analysis data to create an intelligent report

## Additional Context (if available)
- School description and use case
- Number of users/enrollments
- Programs/courses offered
- Any documentation about their setup
- Interview transcripts or support tickets
- Business model (B2C, B2B, B2B2C)

---

Begin your analysis now.
