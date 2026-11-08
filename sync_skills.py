"""
sync_skills.py
==============
Automated Synchronization Engine for Swarm Quant Skills.

Mirrors active quant and agent skills from Anti-Gravity-Core into this
standalone repository, generates manifest metadata, and maintains
canonical versioning.
"""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).resolve().parent
CORE_SKILLS_ACTIVE = Path(r"C:\Anti-Gravity-Core\skills\active")
CORE_AGENT_SKILLS = Path(r"C:\Anti-Gravity-Core\.agent\skills")
DEST_SKILLS = REPO_ROOT / "skills"
DEST_MANIFEST = REPO_ROOT / "manifest.json"


def sync_all_skills(verbose: bool = True) -> int:
    """Syncs skills from Anti-Gravity-Core into this repository."""
    DEST_SKILLS.mkdir(parents=True, exist_ok=True)
    
    # Priority search paths
    search_paths = [CORE_SKILLS_ACTIVE, CORE_AGENT_SKILLS]
    found_skills = {}

    for base_path in search_paths:
        if not base_path.exists():
            continue
        for child in base_path.iterdir():
            if child.is_dir() and (child / "SKILL.md").exists():
                if child.name not in found_skills:
                    found_skills[child.name] = child

    synced_count = 0
    catalog = []

    for skill_name, src_dir in sorted(found_skills.items()):
        dest_dir = DEST_SKILLS / skill_name
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy all contents recursively
        for item in src_dir.rglob("*"):
            if item.is_file():
                rel_path = item.relative_to(src_dir)
                target_file = dest_dir / rel_path
                target_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Check if copy needed
                if not target_file.exists() or item.stat().st_mtime > target_file.stat().st_mtime:
                    shutil.copy2(item, target_file)
        
        # Extract title and description from frontmatter if present
        skill_file = dest_dir / "SKILL.md"
        description = "Quant Swarm Operational Skill"
        if skill_file.exists():
            content = skill_file.read_text(encoding="utf-8", errors="ignore")
            for line in content.splitlines():
                if line.startswith("description:"):
                    description = line.replace("description:", "").strip().strip('"').strip("'")
                    break

        catalog.append({
            "name": skill_name,
            "path": f"skills/{skill_name}/SKILL.md",
            "description": description,
            "synced_at": datetime.utcnow().isoformat() + "Z"
        })
        synced_count += 1
        if verbose:
            print(f"[SYNC] Synced skill: {skill_name}")

    # Write manifest
    manifest_data = {
        "repository": "https://github.com/engpierre/Swarm-gemini-quant-skills.git",
        "last_sync": datetime.utcnow().isoformat() + "Z",
        "total_skills": len(catalog),
        "skills": catalog
    }
    DEST_MANIFEST.write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")
    if verbose:
        print(f"[SYNC] Updated manifest with {len(catalog)} skills -> {DEST_MANIFEST}")

    return synced_count


if __name__ == "__main__":
    count = sync_all_skills(verbose=True)
    print(f"\nSuccessfully synchronized {count} skills into Swarm-gemini-quant-skills.")
