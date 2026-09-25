# NEXUS_OMEGA_CURSOR_MCP_INVENTORY_SYNC_FOR_AXIOM_20260925_R0

## HARD

```text
OBJECT = NEXUS_OMEGA_CURSOR_MCP_INVENTORY_SYNC_FOR_AXIOM_20260925_R0
STATE = MCP_INVENTORY_CAPTURED_C1_SYNC_HANDOFF
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CLAIM_PROMOTION = NO
NAMESPACE_COUNT = 16
TOTAL_TOOLS_DISCOVERED = 1393
STATUS_READY = 12
STATUS_ERROR = 2
STATUS_LOADING = 1
STATUS_UNKNOWN = 1
SOURCE = GetDynamicTools_catalog_live
HOSTINGER_MCP = READY_CAPABILITY_ONLY
HOSTINGER_WRITE_AUTHORITY = NO_BY_DEFAULT
GITHUB_MCP = ERROR_NEEDS_AUTH_OR_FIX
GITLAB_MCP = ERROR_NEEDS_AUTH_OR_FIX
NEXUS_NODE_BUS = LOADING_AT_CAPTURE
CURSOR_ACTION = NONE
NEXT = WAIT_AXIOM_ADJUDICATION_OF_FABRIC_RETURN_AND_OPTIONAL_MCP_SYNC_ACK
```

## Epistemische Waende

- MCP-Praesenz != Schreib-/Deploy-Autoritaet
- Hostinger-Toolzahl 402 != Live-Write freigegeben
- PostHog = derived observability (nicht kanonisches Ledger)
- GitHub/GitLab MCP error != Git fehlt (gh/git CLI separat nutzbar)
- nexus-node-bus loading != Bus-Runtime shipped

## Namespace-Tabelle

| Namespace | Status | Tools | Hinweis |
|---|---|---:|---|
| `cursor` | unknown | 16 | Native Cursor first-party tools (AwaitShell, Task, WebFetch, ...) |
| `cursor-app-control` | ready | 8 | Cursor IDE control (workspace root, rename chat, plugins) |
| `cursor-ide-browser` | ready | 16 | Browser automation / CDP / snapshots |
| `cursor-subscriptions` | ready | 11 | Event subscriptions (GitHub/Linear/Slack/Origin) |
| `plugin-github-github` | error | 1 | GitHub MCP — currently ERROR; only mcp_auth visible | This MCP server failed during live tool discovery. Its tools |
| `plugin-gitlab-GitLab` | error | 1 | GitLab MCP — currently ERROR; only mcp_auth visible | This MCP server failed during live tool discovery. Its tools |
| `plugin-hex-hex` | ready | 19 | Hex notebooks / threads / cells |
| `plugin-huggingface-skills-huggingface-skills` | ready | 7 | Hugging Face Hub (auth user NexusOmega reported in session) |
| `plugin-linear-linear` | ready | 69 | Linear issues/projects/releases/diffs |
| `plugin-semgrep-plugin-semgrep` | ready | 8 | Semgrep plugin scan / findings |
| `plugin-supabase-supabase` | ready | 30 | Supabase projects / SQL / edge / branches |
| `project-0-Perfect Final Version-nexus-node-bus` | loading | 1 | NEXUS Node Bus project MCP — LOADING at capture | This MCP server is still loading; tools may not be available |
| `user-amplitude` | ready | 49 | Amplitude analytics / charts / taxonomy |
| `user-hostinger-mcp` | ready | 402 | Hostinger hosting/VPS/mail/domains/ecommerce — CAPABILITY ONLY |
| `user-posthog` | ready | 747 | PostHog analytics / flags / experiments / warehouse |
| `user-semgrep-local-oss` | ready | 8 | Local Semgrep OSS (duplicate surface vs plugin) |

## Hostinger family breakdown (capability inventory)

| Family | Count |
|---|---:|
| hosting | 112 |
| VPS | 64 |
| reach | 52 |
| agency-hosting | 42 |
| domains | 40 |
| mail | 38 |
| ecommerce | 29 |
| billing | 9 |
| DNS | 8 |
| horizons | 6 |
| mcp_auth | 1 |
| v2 | 1 |

## PostHog top name prefixes (inventory density)

| Prefix | Count |
|---|---:|
| llma | 88 |
| vision | 58 |
| experiment | 40 |
| query | 33 |
| workflows | 30 |
| error | 29 |
| external | 28 |
| data | 21 |
| feature | 21 |
| canvas | 19 |
| inbox | 18 |
| logs | 18 |
| scout | 18 |
| cdp | 16 |
| dashboard | 14 |
| conversations | 13 |
| signals | 13 |
| skill | 12 |
| apm | 11 |
| marketing | 10 |
| endpoint | 9 |
| mcp | 9 |
| notebooks | 9 |
| view | 9 |
| subscriptions | 8 |

## Full tool lists (compact namespaces)

### `cursor` (16)

```text
AwaitShell
ConnectScm
CreateGoal
Delete
EditNotebook
FetchMcpResource
GenerateImage
ReadLints
SearchConversations
SetActiveBranch
SwitchMode
Task
TodoWrite
UpdateGoal
WebFetch
WebSearch
```

### `cursor-app-control` (8)

```text
create_project
cursor_dialog
install_plugin
move_agent_to_cloned_root
move_agent_to_root
open_automation
open_resource
rename_chat
```

### `cursor-ide-browser` (16)

```text
browser_cdp
browser_click
browser_drag
browser_fill
browser_get_bounding_box
browser_highlight
browser_lock
browser_mouse_click_xy
browser_navigate
browser_press_key
browser_scroll
browser_select_option
browser_snapshot
browser_tabs
browser_take_screenshot
browser_type
```

### `cursor-subscriptions` (11)

```text
list_subscriptions
subscribe_github_ci
subscribe_github_pr
subscribe_linear_comment
subscribe_linear_issue
subscribe_origin_ci
subscribe_origin_pr
subscribe_slack_channel
subscribe_slack_new_channels
subscribe_slack_thread
unsubscribe
```

### `plugin-github-github` (1)

```text
mcp_auth
```

### `plugin-gitlab-GitLab` (1)

```text
mcp_auth
```

### `plugin-hex-hex` (19)

```text
continue_thread
create_cell
create_project
create_thread
delete_cell
get_cell
get_cell_image
get_cell_output
get_me
get_project
get_run
get_thread
list_cells
list_data_connections
mcp_auth
run_cell
run_notebook
search_projects
update_cell
```

### `plugin-huggingface-skills-huggingface-skills` (7)

```text
dynamic_space
gr1_z_image_turbo_generate
hf_fs
hf_whoami
hub_repo_details
hub_repo_search
mcp_auth
```

### `plugin-linear-linear` (69)

```text
create_attachment
create_attachment_from_upload
create_issue_label
delete_attachment
delete_comment
delete_diff_comment
delete_status_update
extract_images
get_agent_skill
get_attachment
get_diff
get_diff_threads
get_document
get_issue
get_issue_status
get_milestone
get_notifications
get_project
get_release
get_release_note
get_status_updates
get_team
get_template
get_triage_responsibility
get_user
get_workspace
list_agent_skills
list_comments
list_custom_views
list_cycles
list_diffs
list_documents
list_issue_labels
list_issue_statuses
list_issues
list_milestones
list_project_labels
list_projects
list_release_notes
list_release_pipelines
list_releases
list_teams
list_templates
list_users
mark_notification
mcp_auth
merge_diff
prepare_attachment_upload
resolve_diff_thread
restore_issue_label
restore_project_label
retire_issue_label
retire_project_label
save_comment
save_diff_comment
save_document
save_issue
save_issue_label
save_milestone
save_project
save_project_label
save_release
save_release_note
save_status_update
search_documentation
share_issue
submit_diff_review
unshare_issue
update_diff
```

### `plugin-semgrep-plugin-semgrep` (8)

```text
get_abstract_syntax_tree
get_supported_languages
mcp_auth
semgrep_findings
semgrep_rule_schema
semgrep_scan
semgrep_scan_supply_chain
semgrep_scan_with_custom_rule
```

### `plugin-supabase-supabase` (30)

```text
apply_migration
confirm_cost
create_branch
create_project
delete_branch
deploy_edge_function
execute_sql
generate_typescript_types
get_advisors
get_cost
get_edge_function
get_organization
get_project
get_project_url
get_publishable_keys
list_branches
list_edge_functions
list_extensions
list_migrations
list_organizations
list_projects
list_tables
mcp_auth
merge_branch
pause_project
query_logs
rebase_branch
reset_branch
restore_project
search_docs
```

### `project-0-Perfect Final Version-nexus-node-bus` (1)

```text
mcp_auth
```

### `user-amplitude` (49)

```text
create_group_types
create_properties
delete_event_properties
delete_user_properties
get_agent_results
get_amp_session_replay_info
get_amp_taxonomy
get_amp_user_data
get_amplitude_agent_analytics_info
get_amplitude_charts
get_amplitude_context
get_data_warehouse_destinations
get_from_url
get_group_types
get_session_replay_duration
get_session_replay_stream
get_session_replay_timeline
get_tracking_plan_sources
get_transformations
manage_amp_context
manage_amp_entities
manage_amp_events
manage_amp_taxonomy
mcp_auth
query_amplitude_data
rename_chart
render_amp_session_replay
render_amplitude_chart
restore_event_properties
restore_user_properties
save_chart_edits
search_amp_data_taxonomy
search_amp_entities
share_amp_entities
track_ui_render_response
update_properties
use_amp_ai_visibility
use_amp_comments
use_amp_dashboards
use_amp_experiments
use_amp_flags
use_amp_guides_surveys
use_amp_notebooks
use_amp_skill
use_amplitude_ai_feedback
use_amplitude_chart_monitors
use_amplitude_cohorts
use_amplitude_data_connections
use_amplitude_metrics
```

### `user-hostinger-mcp` (402) — FULL LIST IN MCP_INVENTORY.json

```text
DNS_deleteDNSRecordsV1
DNS_getDNSRecordsV1
DNS_getDNSSnapshotListV1
DNS_getDNSSnapshotV1
DNS_resetDNSRecordsV1
DNS_restoreDNSSnapshotV1
DNS_updateDNSRecordsV1
DNS_validateDNSRecordsV1
VPS_activateFirewallV1
VPS_attachPublicKeyV1
VPS_createFirewallRuleV1
VPS_createNewFirewallV1
VPS_createNewProjectV1
VPS_createPTRRecordV1
VPS_createPostInstallScriptV1
VPS_createPublicKeyV1
VPS_createSnapshotV1
VPS_deactivateFirewallV1
VPS_deleteFirewallRuleV1
VPS_deleteFirewallV1
VPS_deletePTRRecordV1
VPS_deletePostInstallScriptV1
VPS_deleteProjectV1
VPS_deletePublicKeyV1
VPS_deleteSnapshotV1
VPS_getActionDetailsV1
VPS_getActionsV1
VPS_getAttachedPublicKeysV1
VPS_getBackupsV1
VPS_getDataCenterListV1
...
reach_listSegmentFilterAttributesV1
reach_listSegmentsV1
reach_previewContactsMatchingConditionsV1
reach_removeAContactFromATagV1
reach_removeContactsFromATagV1
reach_renameATagV1
reach_updateAContactFieldV1
reach_updateAContactV1
reach_updateAProfileSegmentV1
v2_getDomainVerificationsDIRECT
```

### `user-posthog` (747) — FULL LIST IN MCP_INVENTORY.json

```text
action-create
action-delete
action-get
action-update
actions-get-all
agent-feedback
alert-create
alert-delete
alert-destinations-create
alert-destinations-delete
alert-get
alert-simulate
alert-update
alerts-list
annotation-create
annotation-delete
annotation-retrieve
annotations-list
annotations-partial-update
apm-attribute-breakdown
apm-attribute-values-list
apm-attributes-list
apm-services-list
apm-spans-aggregate
apm-spans-count
apm-spans-duration-histogram
apm-spans-latency-heatmap
apm-spans-sparkline
apm-spans-tree
apm-trace-get
...
workflows-publish
workflows-restore-revision
workflows-run-batch
workflows-schedule-create
workflows-show-email-template
workflows-stats
workflows-test-run
workflows-update
workflows-update-email-template
workflows-update-schedule
```

### `user-semgrep-local-oss` (8)

```text
get_abstract_syntax_tree
get_supported_languages
mcp_auth
semgrep_findings
semgrep_rule_schema
semgrep_scan
semgrep_scan_supply_chain
semgrep_scan_with_custom_rule
```

## Non-MCP local tools (sync note)

Nicht in MCP-Namespaces, aber in dieser Cursor-Session verfuegbar: Shell, Grep, Read, Write, StrReplace, Glob, GetDynamicTools, CallDynamicTool.

## SOFT (fuer AXIOM)

Dies ist ein Sync-Snapshot der Cursor-MCP-Oberflaeche zum Abgleich mit AXIOM. Er autorisiert keine Hostinger-/www-Writes, keine Claim-Promotion und kein Fabric-Live-Deploy. Fehlerhafte GitHub/GitLab-MCPs bedeuten Auth/Discovery-Gap, nicht Abwesenheit von Git-Transport via CLI. Node-Bus war zum Capture-Zeitpunkt noch im Laden.
