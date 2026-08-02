"""Upgrade Impact Analyzer - Compare two Sonata trunk releases.

Compares two versions (e.g., v16.4 vs v16.5) and produces:
- Release Change Analysis (what changed)
- Capability Impact (which modules affected)
- Upgrade Readiness Assessment (risk level)

Uses: Wiki release notes + Jira issues + CART test coverage.

Usage:
    from upgrade_analyzer import analyze_upgrade
    report = analyze_upgrade("v16.4", "v16.5")
"""

import os
import json
from typing import Optional


def analyze_upgrade(
    from_version: str,
    to_version: str,
    client: str = "Royal London",
    include_cart: bool = True,
) -> dict:
    """Compare two trunk releases and produce impact assessment.

    Args:
        from_version: Source version (e.g., "v16.4")
        to_version: Target version (e.g., "v16.5")
        client: Client name for CART scoping
        include_cart: Whether to include CART test coverage

    Returns:
        dict with categorized changes, impact, and recommendations
    """
    from tools.jira_tool import jira_search

    print(f"[Upgrade] Analyzing {from_version} -> {to_version} for {client}")

    # Step 1: Get Jira issues in version range
    issues = _get_version_issues(from_version, to_version)
    print(f"[Upgrade] Found {len(issues)} Jira issues")

    # Step 2: Categorize changes
    categories = _categorize_issues(issues)
    print(f"[Upgrade] Categories: {list(categories.keys())}")

    # Step 3: Get CART coverage (if enabled)
    cart_coverage = {}
    if include_cart:
        cart_coverage = _get_cart_coverage(to_version, client)
        print(f"[Upgrade] CART: {len(cart_coverage)} test sets found")

    # Step 4: Get release notes from wiki
    release_notes = _get_release_notes(from_version, to_version)
    print(f"[Upgrade] Release notes: {len(release_notes)} entries")

    # Step 5: Generate impact assessment
    impact = _assess_impact(categories, cart_coverage, release_notes)

    return {
        "from_version": from_version,
        "to_version": to_version,
        "client": client,
        "summary": {
            "total_changes": len(issues),
            "by_category": {k: len(v) for k, v in categories.items()},
            "cart_tests": len(cart_coverage),
            "risk_level": impact["risk_level"],
        },
        "categories": categories,
        "cart_coverage": cart_coverage,
        "release_notes": release_notes,
        "impact": impact,
    }


def _get_version_issues(from_version: str, to_version: str) -> list:
    """Get all Jira issues between two versions."""
    from tools.jira_tool import jira_search

    # Version mapping (internal names -> release versions)
    VERSION_MAP = {
        "v16.4": "Raglan 14.9 R12",
        "16.4": "Raglan 14.9 R12",
        "v16.5": "Raglan 14.9 R13",
        "16.5": "Raglan 14.9 R13",
    }

    from_v = VERSION_MAP.get(from_version.replace("v", "").strip(), from_version)
    to_v = VERSION_MAP.get(to_version.replace("v", "").strip(), to_version)

    # Query for issues in target version
    jql = f'fixVersion = "{to_v}" ORDER BY issuetype ASC, key DESC'

    try:
        results = jira_search(jql=jql, max_results=200)
        return results
    except Exception as e:
        print(f"[Upgrade] Jira query failed: {e}")
        return []


def _categorize_issues(issues: list) -> dict:
    """Categorize issues into impact areas."""
    categories = {
        "new_features": [],
        "bug_fixes": [],
        "enhancements": [],
        "breaking_changes": [],
        "deprecations": [],
        "infrastructure": [],
        "other": [],
    }

    for issue in issues:
        issue_type = issue.get("type", "").lower()
        summary = issue.get("summary", "").lower()
        key = issue.get("key", "")

        entry = {
            "key": key,
            "summary": issue.get("summary", ""),
            "status": issue.get("status", ""),
            "components": issue.get("components", []),
            "fix_versions": issue.get("fix_versions", []),
        }

        # Categorize by type
        if "defect" in issue_type or "bug" in issue_type:
            categories["bug_fixes"].append(entry)
        elif "story" in issue_type or "feature" in issue_type:
            categories["new_features"].append(entry)
        elif "enhancement" in issue_type or "improvement" in issue_type:
            categories["enhancements"].append(entry)
        elif "task" in issue_type:
            categories["infrastructure"].append(entry)
        else:
            # Check summary for breaking/deprecation signals
            if any(w in summary for w in ["deprecat", "removed", "breaking", " incompatible"]):
                categories["breaking_changes"].append(entry)
            elif any(w in summary for w in ["deprecat", "legacy", "old", "sunset"]):
                categories["deprecations"].append(entry)
            else:
                categories["other"].append(entry)

    return categories


def _get_cart_coverage(version: str, client: str) -> dict:
    """Get CART test coverage for a version."""
    from tools.jira_tool import jira_search

    # Query CART filter
    jql = 'filter=103721 ORDER BY key DESC'

    try:
        results = jira_search(jql=jql, max_results=100)
        coverage = {}

        for test in results:
            components = test.get("components", [])
            status = test.get("status", "")
            key = test.get("key", "")

            for comp in components:
                if comp not in coverage:
                    coverage[comp] = []
                coverage[comp].append({
                    "key": key,
                    "summary": test.get("summary", ""),
                    "status": status,
                })

        return coverage
    except Exception as e:
        print(f"[Upgrade] CART query failed: {e}")
        return {}


def _get_release_notes(from_version: str, to_version: str) -> list:
    """Get release notes from wiki (placeholder - needs wiki integration)."""
    # TODO: Fetch from wiki using wiki_tool
    # For now, return placeholder
    return [
        {
            "version": to_version,
            "note": f"Release notes for {to_version} (wiki integration pending)",
            "source": "wiki",
        }
    ]


def _assess_impact(categories: dict, cart_coverage: dict, release_notes: list) -> dict:
    """Assess overall upgrade impact and risk."""
    total_changes = sum(len(v) for v in categories.values())
    breaking = len(categories.get("breaking_changes", []))
    bug_fixes = len(categories.get("bug_fixes", []))
    features = len(categories.get("new_features", []))

    # Determine risk level
    if breaking > 0:
        risk_level = "HIGH"
        risk_reason = f"{breaking} breaking changes detected"
    elif bug_fixes > 10:
        risk_level = "MEDIUM"
        risk_reason = f"{bug_fixes} bug fixes (review recommended)"
    elif total_changes > 20:
        risk_level = "MEDIUM"
        risk_reason = f"{total_changes} total changes (thorough testing needed)"
    else:
        risk_level = "LOW"
        risk_reason = f"{total_changes} changes, no breaking changes"

    # Components affected
    affected_components = set()
    for cat_issues in categories.values():
        for issue in cat_issues:
            for comp in issue.get("components", []):
                affected_components.add(comp)

    return {
        "risk_level": risk_level,
        "risk_reason": risk_reason,
        "total_changes": total_changes,
        "breaking_changes": breaking,
        "affected_components": list(affected_components),
        "cart_coverage_summary": {
            "modules_tested": list(cart_coverage.keys()),
            "total_tests": sum(len(v) for v in cart_coverage.values()),
        },
        "recommendations": _generate_recommendations(categories, cart_coverage, risk_level),
    }


def _generate_recommendations(categories: dict, cart_coverage: dict, risk_level: str) -> list:
    """Generate upgrade recommendations."""
    recs = []

    if categories.get("breaking_changes"):
        recs.append({
            "priority": "HIGH",
            "action": "Review breaking changes before upgrade",
            "detail": f"{len(categories['breaking_changes'])} breaking changes require attention",
        })

    if categories.get("bug_fixes"):
        recs.append({
            "priority": "MEDIUM",
            "action": "Review bug fixes for relevant modules",
            "detail": f"{len(categories['bug_fixes'])} bugs fixed - check if any affect current operations",
        })

    if not cart_coverage:
        recs.append({
            "priority": "HIGH",
            "action": "Run CART tests before upgrade",
            "detail": "No CART coverage found - manual testing required",
        })

    if risk_level == "LOW":
        recs.append({
            "priority": "LOW",
            "action": "Standard upgrade process",
            "detail": "Low risk - proceed with normal testing",
        })

    return recs


def format_report(analysis: dict) -> str:
    """Format analysis as readable markdown report."""
    report = []
    report.append(f"# Upgrade Impact Report: {analysis['from_version']} -> {analysis['to_version']}")
    report.append(f"**Client:** {analysis['client']}")
    report.append(f"**Risk Level:** {analysis['impact']['risk_level']}")
    report.append("")

    # Summary
    s = analysis["summary"]
    report.append("## Summary")
    report.append(f"- Total changes: {s['total_changes']}")
    for cat, count in s["by_category"].items():
        if count > 0:
            report.append(f"  - {cat.replace('_', ' ').title()}: {count}")
    report.append("")

    # Impact
    impact = analysis["impact"]
    report.append("## Impact Assessment")
    report.append(f"**Risk:** {impact['risk_level']} - {impact['risk_reason']}")
    report.append(f"**Affected components:** {', '.join(impact['affected_components']) or 'None identified'}")
    report.append("")

    # Recommendations
    if impact["recommendations"]:
        report.append("## Recommendations")
        for rec in impact["recommendations"]:
            report.append(f"- [{rec['priority']}] {rec['action']}: {rec['detail']}")
    report.append("")

    # Detailed changes by category
    for cat_name, cat_issues in analysis["categories"].items():
        if cat_issues:
            report.append(f"## {cat_name.replace('_', ' ').title()} ({len(cat_issues)})")
            for issue in cat_issues[:10]:  # Limit to 10 per category
                comps = ", ".join(issue.get("components", []))
                report.append(f"- **{issue['key']}**: {issue['summary']} [{comps}]")
            if len(cat_issues) > 10:
                report.append(f"- ... and {len(cat_issues) - 10} more")
            report.append("")

    return "\n".join(report)
