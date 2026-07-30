"""
NOX Project Manager — "Chief Designer Mode"
=============================================
แก้ปัญหาหลัก: Chief ไม่รู้ว่าไฟล์ไหน "เสร็จแล้ว" เลยเดาสุ่มว่าต้องทำอะไรต่อ
วิธีแก้: สร้าง "Project Index" (ไฟล์ .index.json ในโฟลเดอร์โปรเจกต์) เก็บสถานะ
ของทุกไฟล์ไว้ แล้วให้ Chief เช็ค index นี้ก่อนตอบทุกครั้ง ไม่ใช่เดาจากชื่อไฟล์

Workflow: Draft -> Review -> Approved -> Locked
เฉพาะไฟล์ที่ "Locked" เท่านั้นที่ถือว่าเสร็จ ห้ามแก้/ห้ามสร้างซ้ำ
"""

import json
import re
import difflib
from pathlib import Path
from datetime import datetime

INDEX_FILENAME = ".project_index.json"
STATUSES = ["Draft", "Review", "Approved", "Locked"]

# กำหนดว่าเอกสารแต่ละประเภทต้อง "มีหัวข้อ" อะไรบ้างถึงจะถือว่าเขียนครบ (Definition of Done)
DOC_TYPE_REQUIREMENTS = {
    "character_bible": ["Appearance", "Personality", "Backstory", "Voice & Speech Pattern", "Relationships"],
    "world_bible": ["Geography", "History", "Culture", "Rules & Magic System", "Factions"],
}


CONFIG_FILE = Path(__file__).parent / "nox_projects.json"


def load_project_paths() -> dict:
    if not CONFIG_FILE.exists():
        return {}
    return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))


def save_project_path(name: str, path: str):
    paths = load_project_paths()
    paths[name] = path
    CONFIG_FILE.write_text(json.dumps(paths, indent=2, ensure_ascii=False), encoding="utf-8")


def resolve_project_path(name_or_path: str):
    """รับได้ทั้งชื่อย่อที่เคยผูกไว้ (/link-project) หรือ path เต็มตรงๆ"""
    p = Path(name_or_path)
    if p.exists() and p.is_dir():
        return p
    paths = load_project_paths()
    if name_or_path in paths:
        candidate = Path(paths[name_or_path])
        if candidate.exists():
            return candidate
    return None


def guess_doc_type(filename: str) -> str:
    name = filename.lower()
    if "character" in name:
        return "character_bible"
    if "world" in name:
        return "world_bible"
    return "generic"


def extract_headers(filepath: Path) -> list[str]:
    """ดึงหัวข้อ ## ทั้งหมดจากไฟล์ markdown"""
    text = filepath.read_text(encoding="utf-8")
    return re.findall(r"^##\s+(.+)$", text, flags=re.MULTILINE)


def load_index(project_dir: Path) -> dict:
    idx_path = project_dir / INDEX_FILENAME
    if not idx_path.exists():
        return {"project": project_dir.name, "documents": {}}
    return json.loads(idx_path.read_text(encoding="utf-8"))


def save_index(project_dir: Path, index: dict):
    idx_path = project_dir / INDEX_FILENAME
    idx_path.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")


def scan_project(project_dir: Path) -> dict:
    """
    สแกนโฟลเดอร์จริง เทียบกับ index เดิม:
    - ไฟล์ใหม่ที่ไม่เคยเห็น -> เพิ่มเข้า index สถานะ Draft
    - ไฟล์เดิม -> อัปเดตแค่ headers ที่พบ ไม่แตะสถานะที่คนตั้งไว้แล้ว
    """
    index = load_index(project_dir)
    docs = index["documents"]

    md_files = sorted(project_dir.glob("*.md"))
    for f in md_files:
        headers = extract_headers(f)
        doc_type = guess_doc_type(f.name)
        if f.name not in docs:
            docs[f.name] = {
                "status": "Draft",
                "doc_type": doc_type,
                "headers_found": headers,
                "last_scanned": datetime.now().isoformat(timespec="seconds"),
            }
        else:
            docs[f.name]["headers_found"] = headers
            docs[f.name]["last_scanned"] = datetime.now().isoformat(timespec="seconds")

    index["documents"] = docs
    save_index(project_dir, index)
    return index


def check_definition_of_done(doc_name: str, index: dict) -> tuple[bool, list[str]]:
    doc = index["documents"][doc_name]
    required = DOC_TYPE_REQUIREMENTS.get(doc["doc_type"], [])
    if not required:
        return True, []
    missing = [h for h in required if h not in doc["headers_found"]]
    return (len(missing) == 0), missing


def check_duplicates(new_title: str, index: dict, threshold: float = 0.72) -> str | None:
    """เช็คว่าชื่อไฟล์/หัวข้อใหม่คล้ายของเดิมที่ Locked/Approved ไปแล้วไหม (กันสร้างซ้ำ)"""
    for name, doc in index["documents"].items():
        if doc["status"] in ("Locked", "Approved"):
            existing_title = name.rsplit(".", 1)[0]
            ratio = difflib.SequenceMatcher(None, new_title.lower(), existing_title.lower()).ratio()
            if ratio >= threshold:
                return name
    return None


def next_action(project_dir: Path) -> str:
    """
    Logic หลักของ 'Chief Designer Mode' — ตอบว่าควรทำอะไรต่อ
    ตรงกับ flow ที่ user ออกแบบไว้: scan -> DoD check -> duplicate check -> next doc
    """
    index = scan_project(project_dir)
    docs = index["documents"]
    lines = [f"📂 Scanning {project_dir.name}...\n"]

    # เรียงไฟล์ตามชื่อ (เลขนำหน้า 01_, 02_ กำหนดลำดับ pipeline)
    ordered_names = sorted(docs.keys())

    current_doc = None
    for name in ordered_names:
        doc = docs[name]
        ok, missing = check_definition_of_done(name, index)
        status_icon = "✓" if doc["status"] == "Locked" else ("🔸" if ok else "○")
        detail = f"{doc['status']}"
        if doc["status"] != "Locked" and missing:
            detail += f" — ขาด: {', '.join(missing)}"
        lines.append(f"{status_icon} {name} = {detail}")

        if doc["status"] != "Locked" and current_doc is None:
            current_doc = name

    lines.append("")

    if current_doc is None:
        lines.append("🎉 ทุกไฟล์ Locked ครบแล้ว — พร้อมเริ่มเอกสารถัดไป (ยังไม่มีในโฟลเดอร์)")
        return "\n".join(lines)

    doc = docs[current_doc]
    ok, missing = check_definition_of_done(current_doc, index)

    lines.append(f"Next document: {current_doc}")
    if not ok:
        lines.append(f"Step: เขียนหัวข้อที่ขาด → {missing[0]}")
    else:
        lines.append("ครบทุกหัวข้อแล้ว รอ Review → Approve → Lock")

    return "\n".join(lines)


def set_status(project_dir: Path, doc_name: str, new_status: str) -> str:
    if new_status not in STATUSES:
        return f"❌ สถานะต้องเป็นหนึ่งใน {STATUSES}"
    index = load_index(project_dir)
    if doc_name not in index["documents"]:
        return f"❌ ไม่พบไฟล์ {doc_name} ใน index (ลอง scan ก่อน)"
    index["documents"][doc_name]["status"] = new_status
    save_index(project_dir, index)
    return f"✅ {doc_name} → {new_status}"


if __name__ == "__main__":
    project_path = Path(__file__).parent / "NOX_Studio"

    print("=" * 60)
    print("รอบที่ 1 — ยังไม่ได้ Lock อะไรเลย")
    print("=" * 60)
    print(next_action(project_path))

    print("\n" + "=" * 60)
    print("สั่ง Lock ไฟล์ Character Bible (สมมติ Approve แล้ว)")
    print("=" * 60)
    print(set_status(project_path, "01_Character_Bible.md", "Locked"))

    print("\n" + "=" * 60)
    print("รอบที่ 2 — หลัง Lock Character Bible แล้ว สั่ง 'ไปต่อ' อีกครั้ง")
    print("=" * 60)
    print(next_action(project_path))

    print("\n" + "=" * 60)
    print("ทดสอบ Duplicate Detection — ลองสร้างไฟล์ชื่อคล้ายของเดิม")
    print("=" * 60)
    dup = check_duplicates("Character_Bible_2", load_index(project_path))
    if dup:
        print(f"⚠️ พบว่าคล้ายกับไฟล์ที่ Locked แล้ว: {dup} — ห้ามสร้างใหม่ ให้แก้ไฟล์เดิมแทน")
    else:
        print("ไม่พบไฟล์ซ้ำ สร้างใหม่ได้")
