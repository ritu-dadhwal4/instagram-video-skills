#!/usr/bin/env python3
"""Home board for Trial Reels Studio: one row per reel board with its status.

Usage: build_home.py home.json out_dir first_id_number
home.json: {"title": "...", "takeaway": "...", "reels": [{"name", "url", "status", "step"}]}
status: planned | running | complete
"""
import json, os, sys

COLOR = {"planned": "white", "running": "yellow", "complete": "green"}
WORD = {"planned": "Planned", "running": "Running", "complete": "✓ Complete"}

def main():
    spec = json.load(open(sys.argv[1])); out = sys.argv[2]; nid = [int(sys.argv[3])]
    os.makedirs(out, exist_ok=True)
    for fn in os.listdir(out): os.remove(os.path.join(out, fn))
    E = {}
    def add(d):
        k = f"e{nid[0]}"; nid[0] += 1; E[k] = d; return k
    reels = spec["reels"]
    add({"type": "text", "x": 0, "y": -170, "text": spec.get("title", "Trial Reels Studio"), "size": "title"})
    add({"type": "text", "x": 0, "y": -98, "text": spec.get("takeaway", "Every reel you are testing, and where it stands."), "size": "large"})
    sec = add({"type": "container", "x": 0, "y": 0, "w": 1000, "h": 24 + 40 + max(1, len(reels)) * 80 + 8, "text": f"{len(reels)} reels", "color": "white"})
    for i, t in enumerate(["Reel board", "Status", "Current step"]):
        add({"type": "text", "x": [24, 380, 560][i], "y": 24, "text": f"**{t}**", "size": "small"})
    for i, r in enumerate(reels):
        y = 64 + i * 80
        add({"type": "link", "x": 24, "y": y, "href": r["url"], "title": r["name"], "kind": "whiteboard"})
        add({"type": "shape", "kind": "pill", "x": 380, "y": y + 6, "w": 150, "h": 44, "color": COLOR[r["status"]], "size": "small", "text": f"**{WORD[r['status']]}**", "textAlign": "center"})
        add({"type": "text", "x": 560, "y": y + 16, "text": r.get("step", ""), "size": "body", "wrap": 420})
    order = [sec] + [k for k in E if k != sec]
    json.dump({"v": 1, "title": spec.get("board_title", "Trial Reels Studio"), "order": order}, open(os.path.join(out, "meta.json"), "w"), ensure_ascii=False)
    for k, v in E.items(): json.dump(v, open(os.path.join(out, f"{k}.json"), "w"), ensure_ascii=False)
    print(json.dumps(order))

if __name__ == "__main__":
    main()
