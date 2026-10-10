from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class MenuSelection:
    root: str
    item: str


class MenuController:
    def __init__(self, menu_tree: Dict[str, List[str]]) -> None:
        self.menu_tree = menu_tree
        self.root_items = list(menu_tree.keys())
        self.active_root_index = 0
        self.active_sub_index = 0
        self.in_submenu = False

    def breadcrumb(self) -> str:
        if not self.in_submenu:
            return "VISION"
        return f"VISION / {self.root_items[self.active_root_index]}"

    def current_items(self) -> List[str]:
        if not self.in_submenu:
            return self.root_items
        root = self.root_items[self.active_root_index]
        return ["< Back"] + self.menu_tree[root]

    def update_hover(self, cursor_xy: Tuple[int, int], origin: Tuple[int, int] = (20, 20)) -> None:
        cx, cy = cursor_xy
        x0, y0 = origin
        if not (x0 <= cx <= x0 + 400):
            return

        if not self.in_submenu:
            i = (cy - (y0 + 50)) // 36
            if 0 <= i < len(self.root_items):
                self.active_root_index = int(i)
            return

        root = self.root_items[self.active_root_index]
        sub_items = ["< Back"] + self.menu_tree[root]
        i = (cy - (y0 + 82)) // 34
        if 0 <= i < len(sub_items):
            self.active_sub_index = int(i)

    def confirm(self) -> Tuple[bool, bool, MenuSelection | None]:
        if not self.in_submenu:
            root = self.root_items[self.active_root_index]
            if root == "EXIT":
                return False, False, None
            self.in_submenu = True
            self.active_sub_index = 0
            return True, False, None

        root = self.root_items[self.active_root_index]
        items = ["< Back"] + self.menu_tree[root]
        item = items[self.active_sub_index]
        if item == "< Back":
            self.in_submenu = False
            return True, True, None

        return True, False, MenuSelection(root=root, item=item)
